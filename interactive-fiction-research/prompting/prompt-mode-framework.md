# Prompt Mode Framework for Interactive Fiction

**Purpose:** Keep interactive fiction generation consistent by separating writing stages, enforcing structured templates, and validating against canon.

---

## 1. Distinct Prompt Modes

Use a different prompt mode for each stage to prevent drift. Each mode has a clear input/output contract.

### Brainstorm Mode
**Goal:** Generate raw ideas without committing to canon.  
**Inputs:** Genre, theme, constraint list, target player experience.  
**Outputs:** A list of candidate concepts (settings, conflicts, puzzles, tone).

### Outline Mode
**Goal:** Select and structure ideas into a coherent story plan.  
**Inputs:** Selected concept, constraints, canonical facts, world rules.  
**Outputs:** A scene or location outline with goals, gates, and puzzle arcs.

### Draft Mode
**Goal:** Produce in-world content using an approved outline.  
**Inputs:** Outline chunk, canonical facts, character traits, world rules.  
**Outputs:** In-world prose, descriptions, and interactive affordances.

### Revise Mode
**Goal:** Improve clarity, pacing, and interactivity without changing canon.  
**Inputs:** Draft, checklist items, canon pack.  
**Outputs:** Revised draft with changes annotated or summarized.

### Critique Mode
**Goal:** Diagnose problems and list fixes, not rewrite.  
**Inputs:** Draft, player persona, success criteria.  
**Outputs:** Issue list with severity, recommended fixes, and examples.

---

## 2. Structured Prompt Templates

Use templates to prevent drift and keep outputs machine-checkable.

### Template: Outline → Scene Spec

**Prompt**
```
Mode: Outline → Scene Spec
Scope: [single scene/location]
Input Outline:
- Scene Goal:
- Gate/Lock:
- Key/Unlock:
- Player Actions:
- NPC/Entity:
- Mood/Tone:
- Story Reveal:

Canon Pack:
- Canonical Facts:
- Character Traits:
- World Rules:

Output Format (strict):
Scene Spec:
  Title:
  Location:
  Goal:
  Gate:
  Key:
  Interactive Objects:
    - Name:
      Properties:
      Affordances:
  NPCs:
    - Name:
      Role:
      Constraints:
  Environmental Story Clues:
  Player Feedback:
  Failure States:
  Required Canon References:
```

**Notes**
- Every object must list at least one **Affordance** (action the player can attempt).
- If a canon item is referenced, add it to **Required Canon References**.

### Template: Scene Spec → Draft

**Prompt**
```
Mode: Draft
Input Scene Spec: [paste Scene Spec]
Canon Pack: [paste canon pack]

Output Format (strict):
Scene Draft:
  Room Description (2-4 paragraphs):
  Interactive Affordances (bulleted verbs + targets):
  Default Parser Responses (3-6):
  Clue Reveals:
  Exit Summary:
```

---

## 3. Memory Mechanisms

Maintain a **Canon Pack** that is updated only by explicit approval. Treat this as your single source of truth.

### Canon Pack Structure
```
Canon Pack:
  Canonical Facts:
    - [immutable facts about the world or story]
  Character Traits:
    - Character: [name]
      Core Traits: [3-5 traits]
      Known Goals: [goals]
      Constraints: [what they will not do]
  World Rules:
    - [physics, magic, technology limits, social rules]
  Object Registry:
    - Object: [name]
      Properties: [size, weight, state]
      Allowed Interactions: [verbs]
```

### Canon Updates
- Updates must be explicit: **“Canon Update Request”**.
- Log changes with **reason**, **impact**, and **affected scenes**.
- Avoid retroactive changes unless flagged as **Retcon**.

---

## 4. Model Validation Step

Add a post-generation check that compares output to canon and required structure.

### Validation Prompt Template
```
Mode: Validation
Input:
  Draft: [paste output]
  Scene Spec: [paste spec]
  Canon Pack: [paste canon]

Output Format (strict):
Validation Report:
  Canon Conflicts:
    - [conflict + evidence]
  Missing Requirements:
    - [missing spec element]
  Unclear Affordances:
    - [action/target missing or vague]
  Drift Risk:
    - [where the draft deviates from outline intent]
  Fix Suggestions:
    - [specific edits]
```

### Acceptance Gate
- **Pass** if: no canon conflicts, all required fields present, and affordances are clear.
- **Fail** if: any canon conflict or missing spec element.

---

## Recommended Workflow

1. **Brainstorm** → generate 3–5 concepts.
2. **Outline** → pick one and produce a scene spec.
3. **Draft** → write the scene strictly from the spec.
4. **Validation** → check against canon and spec.
5. **Revise** → incorporate fixes.
6. **Critique** → evaluate player experience once stable.
