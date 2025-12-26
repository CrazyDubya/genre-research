const runCheckButton = document.getElementById("runCheck");
const resultsList = document.getElementById("resultsList");
const resultsCount = document.getElementById("resultsCount");
const styleGuideSelect = document.getElementById("styleGuide");
const customOptions = document.getElementById("customOptions");
const customOxford = document.getElementById("customOxford");
const customFragments = document.getElementById("customFragments");
const ruleOverridesInput = document.getElementById("ruleOverrides");
const draftInput = document.getElementById("draft");

const RULES = {
  "subject-verb": {
    title: "Subject-verb agreement",
    explanation:
      "A singular subject should pair with a singular verb, and a plural subject should pair with a plural verb.",
    example: "Incorrect: She are ready. Correct: She is ready.",
  },
  punctuation: {
    title: "Punctuation & mechanics",
    explanation:
      "Ensure sentences end with punctuation and apply list punctuation rules based on the chosen style guide.",
    example: "Incorrect: We packed pens paper and ink. Correct: We packed pens, paper, and ink.",
  },
  tense: {
    title: "Tense consistency",
    explanation:
      "Sentences should keep verb tenses consistent, especially when time markers appear.",
    example: "Incorrect: Yesterday we walk to the store. Correct: Yesterday we walked to the store.",
  },
  fragments: {
    title: "Sentence fragments",
    explanation:
      "Complete sentences typically include a subject and a verb unless fragments are intentionally allowed.",
    example: "Incorrect: Running through the hall. Correct: We were running through the hall.",
  },
};

const SUBJECT_VERB_PAIRS = [
  { pattern: /\b(I|you|we|they)\s+is\b/gi, replacement: "$1 are" },
  { pattern: /\b(he|she|it)\s+are\b/gi, replacement: "$1 is" },
  { pattern: /\b(he|she|it)\s+were\b/gi, replacement: "$1 was" },
  { pattern: /\b(I|you|we|they)\s+was\b/gi, replacement: "$1 were" },
  { pattern: /\b(he|she|it)\s+do\b/gi, replacement: "$1 does" },
  { pattern: /\b(I|you|we|they)\s+does\b/gi, replacement: "$1 do" },
];

const TIME_MARKERS = ["yesterday", "ago", "last", "earlier", "previously"];

const template = document.getElementById("resultTemplate");

styleGuideSelect.addEventListener("change", () => {
  customOptions.hidden = styleGuideSelect.value !== "custom";
});

runCheckButton.addEventListener("click", () => {
  const text = draftInput.value.trim();
  const overrides = ruleOverridesInput.value
    .split(",")
    .map((value) => value.trim().toLowerCase())
    .filter(Boolean);
  const settings = getStyleSettings();

  const issues = text ? collectIssues(text, overrides, settings) : [];
  renderResults(issues, text);
});

function getStyleSettings() {
  if (styleGuideSelect.value === "cmos") {
    return { oxfordComma: true, allowFragments: false, label: "CMOS" };
  }

  if (styleGuideSelect.value === "ap") {
    return { oxfordComma: false, allowFragments: false, label: "AP" };
  }

  return {
    oxfordComma: customOxford.checked,
    allowFragments: customFragments.checked,
    label: "Custom",
  };
}

function collectIssues(text, overrides, settings) {
  const issues = [];

  if (!overrides.includes("subject-verb")) {
    issues.push(...checkSubjectVerb(text));
  }

  if (!overrides.includes("punctuation")) {
    issues.push(...checkPunctuation(text, settings));
  }

  if (!overrides.includes("tense")) {
    issues.push(...checkTense(text));
  }

  if (!settings.allowFragments && !overrides.includes("fragments")) {
    issues.push(...checkFragments(text));
  }

  return issues;
}

function checkSubjectVerb(text) {
  const issues = [];

  SUBJECT_VERB_PAIRS.forEach((pair) => {
    let match = pair.pattern.exec(text);
    while (match) {
      const original = match[0];
      const suggestion = match[0].replace(pair.pattern, pair.replacement);
      issues.push({
        id: crypto.randomUUID(),
        ruleId: "subject-verb",
        title: RULES["subject-verb"].title,
        summary: `Possible mismatch: "${original}" → "${suggestion}"`,
        explanation: RULES["subject-verb"].explanation,
        example: RULES["subject-verb"].example,
        original,
        suggestion,
      });
      match = pair.pattern.exec(text);
    }
  });

  return issues;
}

function checkPunctuation(text, settings) {
  const issues = [];
  const sentences = splitSentences(text);

  sentences.forEach((sentence) => {
    if (!/[.!?]$/.test(sentence.trim())) {
      issues.push({
        id: crypto.randomUUID(),
        ruleId: "punctuation",
        title: RULES.punctuation.title,
        summary: `Sentence missing terminal punctuation: "${sentence.trim()}"`,
        explanation: RULES.punctuation.explanation,
        example: RULES.punctuation.example,
        original: sentence,
        suggestion: `${sentence.trim()}.`,
      });
    }
  });

  const listPattern = /\b(\w+),\s+(\w+)\s+and\s+(\w+)\b/g;
  let match = listPattern.exec(text);
  while (match) {
    const original = match[0];
    if (settings.oxfordComma) {
      const suggestion = `${match[1]}, ${match[2]}, and ${match[3]}`;
      if (original !== suggestion) {
        issues.push({
          id: crypto.randomUUID(),
          ruleId: "punctuation",
          title: `${RULES.punctuation.title} (${settings.label})`,
          summary: `Add Oxford comma for ${settings.label} style: "${original}" → "${suggestion}"`,
          explanation: RULES.punctuation.explanation,
          example: RULES.punctuation.example,
          original,
          suggestion,
        });
      }
    } else {
      const suggestion = `${match[1]}, ${match[2]} and ${match[3]}`;
      if (original !== suggestion) {
        issues.push({
          id: crypto.randomUUID(),
          ruleId: "punctuation",
          title: `${RULES.punctuation.title} (${settings.label})`,
          summary: `Remove Oxford comma for ${settings.label} style: "${original}" → "${suggestion}"`,
          explanation: RULES.punctuation.explanation,
          example: RULES.punctuation.example,
          original,
          suggestion,
        });
      }
    }
    match = listPattern.exec(text);
  }

  const doubleSpacePattern = /\.\s{2,}[A-Z]/g;
  match = doubleSpacePattern.exec(text);
  while (match) {
    const original = match[0];
    const suggestion = original.replace(/\s{2,}/, " ");
    issues.push({
      id: crypto.randomUUID(),
      ruleId: "punctuation",
      title: RULES.punctuation.title,
      summary: "Extra spacing after punctuation.",
      explanation: RULES.punctuation.explanation,
      example: RULES.punctuation.example,
      original,
      suggestion,
    });
    match = doubleSpacePattern.exec(text);
  }

  return issues;
}

function checkTense(text) {
  const issues = [];
  const sentences = splitSentences(text);

  sentences.forEach((sentence) => {
    const lowerSentence = sentence.toLowerCase();
    const hasTimeMarker = TIME_MARKERS.some((marker) => lowerSentence.includes(marker));

    if (hasTimeMarker) {
      const presentVerbs = /\b(is|are|does|has|walk|run|talk|drive|go)\b/i;
      const match = sentence.match(presentVerbs);
      if (match) {
        issues.push({
          id: crypto.randomUUID(),
          ruleId: "tense",
          title: RULES.tense.title,
          summary: `Time marker suggests past tense in: "${sentence.trim()}"`,
          explanation: RULES.tense.explanation,
          example: RULES.tense.example,
          original: sentence.trim(),
          suggestion: sentence.trim().replace(presentVerbs, (verb) => toPastTense(verb)),
        });
      }
    }
  });

  return issues;
}

function checkFragments(text) {
  const issues = [];
  const sentences = splitSentences(text);

  sentences.forEach((sentence) => {
    const trimmed = sentence.trim();
    if (!trimmed) {
      return;
    }
    const hasVerb = /\b(is|are|was|were|be|been|being|do|did|does|have|has|had|walk|walked|run|ran|drive|drove|go|went|say|said)\b/i;
    const hasSubject = /\b(I|you|we|they|he|she|it|the|a|an|this|that|these|those|someone|anyone)\b/i;
    if (!hasVerb.test(trimmed) || !hasSubject.test(trimmed)) {
      issues.push({
        id: crypto.randomUUID(),
        ruleId: "fragments",
        title: RULES.fragments.title,
        summary: `Possible fragment: "${trimmed}"`,
        explanation: RULES.fragments.explanation,
        example: RULES.fragments.example,
        original: trimmed,
        suggestion: `Consider revising "${trimmed}" into a complete sentence.`,
      });
    }
  });

  return issues;
}

function splitSentences(text) {
  return text
    .split(/(?<=[.!?])\s+/)
    .map((sentence) => sentence.trim())
    .filter(Boolean);
}

function toPastTense(verb) {
  const lower = verb.toLowerCase();
  const irregular = {
    is: "was",
    are: "were",
    does: "did",
    has: "had",
    go: "went",
    run: "ran",
    drive: "drove",
  };

  if (irregular[lower]) {
    return matchCase(verb, irregular[lower]);
  }

  return matchCase(verb, `${lower}ed`);
}

function matchCase(original, replacement) {
  if (original[0] === original[0].toUpperCase()) {
    return replacement.charAt(0).toUpperCase() + replacement.slice(1);
  }
  return replacement;
}

function renderResults(issues, text) {
  resultsList.innerHTML = "";
  resultsCount.textContent = `${issues.length} issue${issues.length === 1 ? "" : "s"}`;

  issues.forEach((issue) => {
    const node = template.content.cloneNode(true);
    node.querySelector(".result__title").textContent = issue.title;
    node.querySelector(".result__rule").textContent = `Rule: ${issue.ruleId}`;
    node.querySelector(".result__summary").textContent = issue.summary;
    node.querySelector(".result__explanation").textContent = issue.explanation;
    node.querySelector(".result__example").textContent = issue.example;

    const status = node.querySelector(".result__status");
    const approveButton = node.querySelector(".button--approve");
    const rejectButton = node.querySelector(".button--reject");

    approveButton.addEventListener("click", () => {
      if (issue.original && issue.suggestion) {
        draftInput.value = applySuggestion(draftInput.value, issue.original, issue.suggestion);
      }
      status.textContent = "Approved";
      approveButton.disabled = true;
      rejectButton.disabled = true;
    });

    rejectButton.addEventListener("click", () => {
      status.textContent = "Rejected";
      approveButton.disabled = true;
      rejectButton.disabled = true;
    });

    resultsList.appendChild(node);
  });

  if (!issues.length && text) {
    const emptyMessage = document.createElement("p");
    emptyMessage.textContent = "No issues found for the selected rules.";
    resultsList.appendChild(emptyMessage);
  }
}

function applySuggestion(text, original, suggestion) {
  const index = text.indexOf(original);
  if (index === -1) {
    return text;
  }
  return `${text.slice(0, index)}${suggestion}${text.slice(index + original.length)}`;
}
