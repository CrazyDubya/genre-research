# Voice & Style Prompt Kit

**Purpose:** Provide drafting and revision prompts that always include style guide excerpts.

---

## Drafting Prompt (Scene or Chapter)

**Prompt Template:**

```
You are writing in the voice described below. Draft the next scene/chapter.

Voice Profile Snapshot:
- POV: [preferred POV]
- Tense: [preferred tense]
- Narrative distance: [close/medium/far]
- Core traits: [trait list]

Style Guide Excerpts (must follow):
- [Excerpt 1]
- [Excerpt 2]
- [Excerpt 3]

Context:
- Current location: [where the scene takes place]
- Player goal: [goal]
- Required story beats: [beats]
- Interactive elements: [objects, puzzles, NPCs]

Output requirements:
- Length: [word count]
- Include at least [X] interactive affordances (e.g., examinable objects)
- Maintain the voice and vocabulary rules above
```

---

## Revision Prompt (Voice Pass)

**Prompt Template:**

```
Revise the text to match the voice and style guide below without changing plot or mechanics.

Voice Profile Snapshot:
- POV: [preferred POV]
- Tense: [preferred tense]
- Narrative distance: [close/medium/far]
- Core traits: [trait list]

Style Guide Excerpts (must follow):
- [Excerpt 1]
- [Excerpt 2]
- [Excerpt 3]

Text to revise:
[Paste scene or chapter]

Output requirements:
- Preserve meaning and interactive affordances
- Align diction with preferred vocabulary
- Remove banned words/phrases
```

---

## Revision Prompt (Consistency Check)

**Prompt Template:**

```
Review the following chapters for voice consistency.

Voice Profile Snapshot:
- POV: [preferred POV]
- Tense: [preferred tense]
- Narrative distance: [close/medium/far]
- Core traits: [trait list]

Style Guide Excerpts (must follow):
- [Excerpt 1]
- [Excerpt 2]
- [Excerpt 3]

Chapters:
- Chapter 1: [paste]
- Chapter 2: [paste]
- Chapter 3: [paste]

Output requirements:
- Identify any deviations from POV/tense
- Flag banned words/phrases
- Note shifts in sentence texture or tone
- Provide a short fix list per chapter
```

