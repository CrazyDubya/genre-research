const storageKey = "canon-manager-state";

const state = loadState() ?? {
  characters: [],
  locations: [],
  factions: [],
  rules: [],
  events: [],
  scenes: [],
};

const elements = {
  characterForm: document.getElementById("characterForm"),
  characterId: document.getElementById("characterId"),
  characterName: document.getElementById("characterName"),
  characterDescription: document.getElementById("characterDescription"),
  characterFaction: document.getElementById("characterFaction"),
  characterLocation: document.getElementById("characterLocation"),
  characterKnowledge: document.getElementById("characterKnowledge"),
  characterList: document.getElementById("characterList"),
  characterReset: document.getElementById("characterReset"),
  locationForm: document.getElementById("locationForm"),
  locationId: document.getElementById("locationId"),
  locationName: document.getElementById("locationName"),
  locationDescription: document.getElementById("locationDescription"),
  locationList: document.getElementById("locationList"),
  locationReset: document.getElementById("locationReset"),
  factionForm: document.getElementById("factionForm"),
  factionId: document.getElementById("factionId"),
  factionName: document.getElementById("factionName"),
  factionDescription: document.getElementById("factionDescription"),
  factionList: document.getElementById("factionList"),
  factionReset: document.getElementById("factionReset"),
  ruleForm: document.getElementById("ruleForm"),
  ruleId: document.getElementById("ruleId"),
  ruleName: document.getElementById("ruleName"),
  ruleDescription: document.getElementById("ruleDescription"),
  ruleList: document.getElementById("ruleList"),
  ruleReset: document.getElementById("ruleReset"),
  eventForm: document.getElementById("eventForm"),
  eventId: document.getElementById("eventId"),
  eventName: document.getElementById("eventName"),
  eventDate: document.getElementById("eventDate"),
  eventDescription: document.getElementById("eventDescription"),
  eventLocation: document.getElementById("eventLocation"),
  eventList: document.getElementById("eventList"),
  eventReset: document.getElementById("eventReset"),
  sceneForm: document.getElementById("sceneForm"),
  sceneId: document.getElementById("sceneId"),
  sceneTitle: document.getElementById("sceneTitle"),
  sceneDate: document.getElementById("sceneDate"),
  sceneLocation: document.getElementById("sceneLocation"),
  sceneSummary: document.getElementById("sceneSummary"),
  sceneCharacters: document.getElementById("sceneCharacters"),
  sceneFactions: document.getElementById("sceneFactions"),
  sceneRules: document.getElementById("sceneRules"),
  sceneEvents: document.getElementById("sceneEvents"),
  sceneKnowledge: document.getElementById("sceneKnowledge"),
  sceneList: document.getElementById("sceneList"),
  sceneReset: document.getElementById("sceneReset"),
  validationList: document.getElementById("validationList"),
  promptForm: document.getElementById("promptForm"),
  promptScene: document.getElementById("promptScene"),
  promptLock: document.getElementById("promptLock"),
  promptOutput: document.getElementById("promptOutput"),
  exportButton: document.getElementById("exportButton"),
  importButton: document.getElementById("importButton"),
  importFile: document.getElementById("importFile"),
};

const defaultOption = (label) => {
  const option = document.createElement("option");
  option.value = "";
  option.textContent = label;
  return option;
};

const toDateValue = (value) => {
  if (!value) {
    return null;
  }
  const parsed = Date.parse(value);
  return Number.isNaN(parsed) ? null : parsed;
};

const createId = () => crypto.randomUUID();

const saveState = () => {
  localStorage.setItem(storageKey, JSON.stringify(state));
};

function loadState() {
  const raw = localStorage.getItem(storageKey);
  if (!raw) {
    return null;
  }
  try {
    return JSON.parse(raw);
  } catch (error) {
    console.warn("Failed to parse saved state", error);
    return null;
  }
}

const renderSelectOptions = (select, items, placeholder) => {
  select.innerHTML = "";
  select.append(defaultOption(placeholder));
  items.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = item.name;
    select.append(option);
  });
};

const renderCheckboxes = (container, items, selected) => {
  container.innerHTML = "";
  items.forEach((item) => {
    const label = document.createElement("label");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = item.id;
    checkbox.checked = selected?.includes(item.id) ?? false;
    label.append(checkbox, document.createTextNode(item.name));
    container.append(label);
  });
};

const collectCheckedValues = (container) =>
  [...container.querySelectorAll("input[type='checkbox']")]
    .filter((input) => input.checked)
    .map((input) => input.value);

const findById = (collection, id) => collection.find((item) => item.id === id);

const listMeta = (label, value) => {
  if (!value) {
    return null;
  }
  const meta = document.createElement("div");
  meta.className = "item-meta";
  meta.textContent = `${label}: ${value}`;
  return meta;
};

const buildListItem = ({
  title,
  description,
  meta = [],
  locked,
  onEdit,
  onDelete,
  onToggleLock,
}) => {
  const wrapper = document.createElement("div");
  wrapper.className = "list-item";
  const header = document.createElement("header");
  const heading = document.createElement("h3");
  heading.textContent = title;
  const actions = document.createElement("div");
  actions.className = "item-actions";

  const editButton = document.createElement("button");
  editButton.type = "button";
  editButton.textContent = "Edit";
  editButton.className = "secondary";
  editButton.disabled = locked;
  editButton.addEventListener("click", onEdit);

  const deleteButton = document.createElement("button");
  deleteButton.type = "button";
  deleteButton.textContent = "Delete";
  deleteButton.className = "secondary";
  deleteButton.addEventListener("click", onDelete);

  const lockToggle = document.createElement("button");
  lockToggle.type = "button";
  lockToggle.textContent = locked ? "Unlock" : "Lock";
  lockToggle.className = "secondary";
  lockToggle.addEventListener("click", onToggleLock);

  actions.append(editButton, deleteButton, lockToggle);
  header.append(heading, actions);

  wrapper.append(header);
  if (description) {
    const body = document.createElement("p");
    body.textContent = description;
    wrapper.append(body);
  }
  meta.filter(Boolean).forEach((item) => wrapper.append(item));
  return wrapper;
};

const resetForm = (form, idField) => {
  form.reset();
  idField.value = "";
};

const updateAll = () => {
  saveState();
  renderSelectors();
  renderLists();
  renderValidations();
  renderPromptSceneOptions();
};

const renderSelectors = () => {
  renderSelectOptions(elements.characterFaction, state.factions, "No faction");
  renderSelectOptions(elements.characterLocation, state.locations, "No home location");
  renderSelectOptions(elements.eventLocation, state.locations, "No location");
  renderSelectOptions(elements.sceneLocation, state.locations, "No location");

  renderCheckboxes(elements.characterKnowledge, state.events, []);
  renderCheckboxes(elements.sceneCharacters, state.characters, []);
  renderCheckboxes(elements.sceneFactions, state.factions, []);
  renderCheckboxes(elements.sceneRules, state.rules, []);
  renderCheckboxes(elements.sceneEvents, state.events, []);
  renderCheckboxes(elements.sceneKnowledge, state.events, []);
};

const renderLists = () => {
  renderCharacterList();
  renderLocationList();
  renderFactionList();
  renderRuleList();
  renderEventList();
  renderSceneList();
};

const renderCharacterList = () => {
  elements.characterList.innerHTML = "";
  state.characters.forEach((character) => {
    const faction = findById(state.factions, character.factionId)?.name;
    const home = findById(state.locations, character.homeLocationId)?.name;
    const knowledge = character.knownEventIds
      .map((id) => findById(state.events, id)?.name)
      .filter(Boolean)
      .join(", ");

    const item = buildListItem({
      title: character.name,
      description: character.description,
      meta: [
        listMeta("Faction", faction),
        listMeta("Home", home),
        listMeta("Known events", knowledge),
      ],
      locked: character.locked,
      onEdit: () => populateCharacterForm(character),
      onDelete: () => removeItem(state.characters, character.id),
      onToggleLock: () => toggleLock(character),
    });
    elements.characterList.append(item);
  });
};

const renderLocationList = () => {
  elements.locationList.innerHTML = "";
  state.locations.forEach((location) => {
    const item = buildListItem({
      title: location.name,
      description: location.description,
      locked: location.locked,
      onEdit: () => populateLocationForm(location),
      onDelete: () => removeItem(state.locations, location.id),
      onToggleLock: () => toggleLock(location),
    });
    elements.locationList.append(item);
  });
};

const renderFactionList = () => {
  elements.factionList.innerHTML = "";
  state.factions.forEach((faction) => {
    const item = buildListItem({
      title: faction.name,
      description: faction.description,
      locked: faction.locked,
      onEdit: () => populateFactionForm(faction),
      onDelete: () => removeItem(state.factions, faction.id),
      onToggleLock: () => toggleLock(faction),
    });
    elements.factionList.append(item);
  });
};

const renderRuleList = () => {
  elements.ruleList.innerHTML = "";
  state.rules.forEach((rule) => {
    const item = buildListItem({
      title: rule.name,
      description: rule.description,
      locked: rule.locked,
      onEdit: () => populateRuleForm(rule),
      onDelete: () => removeItem(state.rules, rule.id),
      onToggleLock: () => toggleLock(rule),
    });
    elements.ruleList.append(item);
  });
};

const renderEventList = () => {
  elements.eventList.innerHTML = "";
  state.events.forEach((event) => {
    const location = findById(state.locations, event.locationId)?.name;
    const item = buildListItem({
      title: event.name,
      description: event.description,
      meta: [listMeta("Date", event.date), listMeta("Location", location)],
      locked: event.locked,
      onEdit: () => populateEventForm(event),
      onDelete: () => removeItem(state.events, event.id),
      onToggleLock: () => toggleLock(event),
    });
    elements.eventList.append(item);
  });
};

const renderSceneList = () => {
  elements.sceneList.innerHTML = "";
  state.scenes.forEach((scene) => {
    const location = findById(state.locations, scene.locationId)?.name;
    const characters = scene.characterIds
      .map((id) => findById(state.characters, id)?.name)
      .filter(Boolean)
      .join(", ");
    const factions = scene.factionIds
      .map((id) => findById(state.factions, id)?.name)
      .filter(Boolean)
      .join(", ");
    const rules = scene.ruleIds
      .map((id) => findById(state.rules, id)?.name)
      .filter(Boolean)
      .join(", ");
    const events = scene.eventIds
      .map((id) => findById(state.events, id)?.name)
      .filter(Boolean)
      .join(", ");
    const knowledge = scene.knowledgeEventIds
      .map((id) => findById(state.events, id)?.name)
      .filter(Boolean)
      .join(", ");

    const item = buildListItem({
      title: scene.title,
      description: scene.summary,
      meta: [
        listMeta("Date", scene.date),
        listMeta("Location", location),
        listMeta("Characters", characters),
        listMeta("Factions", factions),
        listMeta("Rules", rules),
        listMeta("Events", events),
        listMeta("Required knowledge", knowledge),
      ],
      locked: scene.locked,
      onEdit: () => populateSceneForm(scene),
      onDelete: () => removeItem(state.scenes, scene.id),
      onToggleLock: () => toggleLock(scene),
    });
    elements.sceneList.append(item);
  });
};

const renderPromptSceneOptions = () => {
  renderSelectOptions(elements.promptScene, state.scenes, "Select a scene");
};

const removeItem = (collection, id) => {
  const index = collection.findIndex((item) => item.id === id);
  if (index !== -1) {
    collection.splice(index, 1);
    updateAll();
  }
};

const toggleLock = (item) => {
  item.locked = !item.locked;
  updateAll();
};

const populateCharacterForm = (character) => {
  if (character.locked) {
    return;
  }
  elements.characterId.value = character.id;
  elements.characterName.value = character.name;
  elements.characterDescription.value = character.description ?? "";
  elements.characterFaction.value = character.factionId ?? "";
  elements.characterLocation.value = character.homeLocationId ?? "";
  renderCheckboxes(elements.characterKnowledge, state.events, character.knownEventIds);
};

const populateLocationForm = (location) => {
  if (location.locked) {
    return;
  }
  elements.locationId.value = location.id;
  elements.locationName.value = location.name;
  elements.locationDescription.value = location.description ?? "";
};

const populateFactionForm = (faction) => {
  if (faction.locked) {
    return;
  }
  elements.factionId.value = faction.id;
  elements.factionName.value = faction.name;
  elements.factionDescription.value = faction.description ?? "";
};

const populateRuleForm = (rule) => {
  if (rule.locked) {
    return;
  }
  elements.ruleId.value = rule.id;
  elements.ruleName.value = rule.name;
  elements.ruleDescription.value = rule.description ?? "";
};

const populateEventForm = (event) => {
  if (event.locked) {
    return;
  }
  elements.eventId.value = event.id;
  elements.eventName.value = event.name;
  elements.eventDate.value = event.date ?? "";
  elements.eventDescription.value = event.description ?? "";
  elements.eventLocation.value = event.locationId ?? "";
};

const populateSceneForm = (scene) => {
  if (scene.locked) {
    return;
  }
  elements.sceneId.value = scene.id;
  elements.sceneTitle.value = scene.title;
  elements.sceneDate.value = scene.date ?? "";
  elements.sceneLocation.value = scene.locationId ?? "";
  elements.sceneSummary.value = scene.summary ?? "";
  renderCheckboxes(elements.sceneCharacters, state.characters, scene.characterIds);
  renderCheckboxes(elements.sceneFactions, state.factions, scene.factionIds);
  renderCheckboxes(elements.sceneRules, state.rules, scene.ruleIds);
  renderCheckboxes(elements.sceneEvents, state.events, scene.eventIds);
  renderCheckboxes(elements.sceneKnowledge, state.events, scene.knowledgeEventIds);
};

const renderValidations = () => {
  const issues = [];

  const eventsByKey = new Map();
  state.events.forEach((event) => {
    if (!event.date || !event.locationId) {
      return;
    }
    const key = `${event.date}-${event.locationId}`;
    if (!eventsByKey.has(key)) {
      eventsByKey.set(key, []);
    }
    eventsByKey.get(key).push(event);
  });

  eventsByKey.forEach((events) => {
    if (events.length > 1) {
      const names = events.map((event) => event.name).join(", ");
      issues.push({
        type: "warning",
        message: `Timeline conflict: multiple events share the same date and location (${names}).`,
      });
    }
  });

  state.scenes.forEach((scene) => {
    const sceneDateValue = toDateValue(scene.date);
    scene.eventIds.forEach((eventId) => {
      const event = findById(state.events, eventId);
      if (!event) {
        return;
      }
      const eventDateValue = toDateValue(event.date);
      if (sceneDateValue && eventDateValue && sceneDateValue < eventDateValue) {
        issues.push({
          type: "error",
          message: `Scene "${scene.title}" references event "${event.name}" before it occurs.`,
        });
      }
    });

    scene.knowledgeEventIds.forEach((eventId) => {
      const event = findById(state.events, eventId);
      if (!event) {
        return;
      }
      scene.characterIds.forEach((characterId) => {
        const character = findById(state.characters, characterId);
        if (!character) {
          return;
        }
        if (!character.knownEventIds.includes(eventId)) {
          issues.push({
            type: "error",
            message: `Character knowledge mismatch: ${character.name} in "${scene.title}" lacks knowledge of "${event.name}".`,
          });
        }
      });
    });
  });

  if (issues.length === 0) {
    issues.push({ type: "success", message: "No validation issues detected." });
  }

  elements.validationList.innerHTML = "";
  issues.forEach((issue) => {
    const div = document.createElement("div");
    div.className = `issue ${issue.type}`;
    div.textContent = issue.message;
    elements.validationList.append(div);
  });
};

const buildPrompt = (sceneId, enforceLocks) => {
  const scene = findById(state.scenes, sceneId);
  if (!scene) {
    return "Select a scene to generate a prompt.";
  }

  const characters = scene.characterIds.map((id) => findById(state.characters, id)).filter(Boolean);
  const factions = scene.factionIds.map((id) => findById(state.factions, id)).filter(Boolean);
  const rules = scene.ruleIds.map((id) => findById(state.rules, id)).filter(Boolean);
  const events = scene.eventIds.map((id) => findById(state.events, id)).filter(Boolean);
  const knowledge = scene.knowledgeEventIds.map((id) => findById(state.events, id)).filter(Boolean);
  const location = findById(state.locations, scene.locationId);

  const lockedFacts = [
    ...state.characters.filter((item) => item.locked),
    ...state.locations.filter((item) => item.locked),
    ...state.factions.filter((item) => item.locked),
    ...state.rules.filter((item) => item.locked),
    ...state.events.filter((item) => item.locked),
  ];

  const lockSection = enforceLocks
    ? `Locked canon (do not alter without approval):\n${lockedFacts
        .map((item) => `- ${item.name}: ${item.description ?? ""}`)
        .join("\n")}`
    : "Locked canon enforcement is OFF.";

  return [
    "You are writing the next scene in a serialized narrative.",
    "Use the canon data below and avoid contradictions.",
    "",
    lockSection,
    "",
    `Scene title: ${scene.title}`,
    `Scene date/time: ${scene.date || "Unspecified"}`,
    `Location: ${location?.name ?? "Unspecified"}`,
    `Scene summary: ${scene.summary || ""}`,
    "",
    "Characters present:",
    ...characters.map((character) => `- ${character.name}: ${character.description ?? ""}`),
    "",
    "Factions involved:",
    ...factions.map((faction) => `- ${faction.name}: ${faction.description ?? ""}`),
    "",
    "Rules referenced:",
    ...rules.map((rule) => `- ${rule.name}: ${rule.description ?? ""}`),
    "",
    "Events referenced:",
    ...events.map((event) => `- ${event.name}: ${event.description ?? ""}`),
    "",
    "Required knowledge (characters must already know):",
    ...knowledge.map((event) => `- ${event.name}: ${event.description ?? ""}`),
    "",
    "Write the scene with consistent tone, and flag any uncertainties about canon.",
  ].join("\n");
};

const handleExport = () => {
  const blob = new Blob([JSON.stringify(state, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "canon-data.json";
  link.click();
  URL.revokeObjectURL(url);
};

const handleImport = (event) => {
  const file = event.target.files?.[0];
  if (!file) {
    return;
  }
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const data = JSON.parse(reader.result);
      Object.assign(state, data);
      updateAll();
    } catch (error) {
      alert("Unable to import file. Ensure it is valid JSON.");
    }
  };
  reader.readAsText(file);
};

// Forms

elements.characterForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const id = elements.characterId.value;
  const payload = {
    id: id || createId(),
    name: elements.characterName.value.trim(),
    description: elements.characterDescription.value.trim(),
    factionId: elements.characterFaction.value || null,
    homeLocationId: elements.characterLocation.value || null,
    knownEventIds: collectCheckedValues(elements.characterKnowledge),
  };

  if (!payload.name) {
    return;
  }

  if (id) {
    const existing = findById(state.characters, id);
    if (!existing || existing.locked) {
      return;
    }
    Object.assign(existing, payload);
  } else {
    payload.locked = false;
    state.characters.push(payload);
  }

  resetForm(elements.characterForm, elements.characterId);
  updateAll();
});

elements.characterReset.addEventListener("click", () => {
  resetForm(elements.characterForm, elements.characterId);
  renderCheckboxes(elements.characterKnowledge, state.events, []);
});

elements.locationForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const id = elements.locationId.value;
  const payload = {
    id: id || createId(),
    name: elements.locationName.value.trim(),
    description: elements.locationDescription.value.trim(),
  };
  if (!payload.name) {
    return;
  }
  if (id) {
    const existing = findById(state.locations, id);
    if (!existing || existing.locked) {
      return;
    }
    Object.assign(existing, payload);
  } else {
    payload.locked = false;
    state.locations.push(payload);
  }
  resetForm(elements.locationForm, elements.locationId);
  updateAll();
});

elements.locationReset.addEventListener("click", () => {
  resetForm(elements.locationForm, elements.locationId);
});

elements.factionForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const id = elements.factionId.value;
  const payload = {
    id: id || createId(),
    name: elements.factionName.value.trim(),
    description: elements.factionDescription.value.trim(),
  };
  if (!payload.name) {
    return;
  }
  if (id) {
    const existing = findById(state.factions, id);
    if (!existing || existing.locked) {
      return;
    }
    Object.assign(existing, payload);
  } else {
    payload.locked = false;
    state.factions.push(payload);
  }
  resetForm(elements.factionForm, elements.factionId);
  updateAll();
});

elements.factionReset.addEventListener("click", () => {
  resetForm(elements.factionForm, elements.factionId);
});

elements.ruleForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const id = elements.ruleId.value;
  const payload = {
    id: id || createId(),
    name: elements.ruleName.value.trim(),
    description: elements.ruleDescription.value.trim(),
  };
  if (!payload.name) {
    return;
  }
  if (id) {
    const existing = findById(state.rules, id);
    if (!existing || existing.locked) {
      return;
    }
    Object.assign(existing, payload);
  } else {
    payload.locked = false;
    state.rules.push(payload);
  }
  resetForm(elements.ruleForm, elements.ruleId);
  updateAll();
});

elements.ruleReset.addEventListener("click", () => {
  resetForm(elements.ruleForm, elements.ruleId);
});

elements.eventForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const id = elements.eventId.value;
  const payload = {
    id: id || createId(),
    name: elements.eventName.value.trim(),
    date: elements.eventDate.value.trim(),
    description: elements.eventDescription.value.trim(),
    locationId: elements.eventLocation.value || null,
  };
  if (!payload.name) {
    return;
  }
  if (id) {
    const existing = findById(state.events, id);
    if (!existing || existing.locked) {
      return;
    }
    Object.assign(existing, payload);
  } else {
    payload.locked = false;
    state.events.push(payload);
  }
  resetForm(elements.eventForm, elements.eventId);
  updateAll();
});

elements.eventReset.addEventListener("click", () => {
  resetForm(elements.eventForm, elements.eventId);
});

elements.sceneForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const id = elements.sceneId.value;
  const payload = {
    id: id || createId(),
    title: elements.sceneTitle.value.trim(),
    date: elements.sceneDate.value.trim(),
    locationId: elements.sceneLocation.value || null,
    summary: elements.sceneSummary.value.trim(),
    characterIds: collectCheckedValues(elements.sceneCharacters),
    factionIds: collectCheckedValues(elements.sceneFactions),
    ruleIds: collectCheckedValues(elements.sceneRules),
    eventIds: collectCheckedValues(elements.sceneEvents),
    knowledgeEventIds: collectCheckedValues(elements.sceneKnowledge),
  };
  if (!payload.title) {
    return;
  }
  if (id) {
    const existing = findById(state.scenes, id);
    if (!existing || existing.locked) {
      return;
    }
    Object.assign(existing, payload);
  } else {
    payload.locked = false;
    state.scenes.push(payload);
  }
  resetForm(elements.sceneForm, elements.sceneId);
  updateAll();
});

elements.sceneReset.addEventListener("click", () => {
  resetForm(elements.sceneForm, elements.sceneId);
  renderCheckboxes(elements.sceneCharacters, state.characters, []);
  renderCheckboxes(elements.sceneFactions, state.factions, []);
  renderCheckboxes(elements.sceneRules, state.rules, []);
  renderCheckboxes(elements.sceneEvents, state.events, []);
  renderCheckboxes(elements.sceneKnowledge, state.events, []);
});

elements.promptForm.addEventListener("submit", (event) => {
  event.preventDefault();
  elements.promptOutput.value = buildPrompt(
    elements.promptScene.value,
    elements.promptLock.checked
  );
});

elements.exportButton.addEventListener("click", handleExport);

elements.importButton.addEventListener("click", () => {
  elements.importFile.click();
});

elements.importFile.addEventListener("change", handleImport);

updateAll();
