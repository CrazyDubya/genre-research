# Canon Management Worksheet (Interactive Fiction)

Use this worksheet to track story canon with structured schemas, automatic update rules, contradiction checks, and entry locks. It is designed for IF projects where the world must stay consistent across exploration paths.

---

## 1) Canon Schemas

### Characters (traits, goals, arcs)

**Character Schema**
- **ID:** (unique slug)
- **Name:**
- **Role:** (player character, NPC, antagonist, ally, etc.)
- **Status:** (alive, missing, dead, unknown)
- **Traits:**
  - **Core Traits:** (stable personality traits)
  - **Surface Traits:** (contextual behaviors)
  - **Contradictions:** (intentional inconsistencies that define complexity)
- **Goals:**
  - **Short-Term:** (immediate objectives)
  - **Long-Term:** (overarching motivations)
  - **Conflicts:** (what blocks these goals)
- **Arc:**
  - **Starting State:** (beliefs, relationships, status)
  - **Key Turns:** (major moments that shift the arc)
  - **Ending State:** (final change or resolution)
- **Relationships:** (who/what they affect)
- **Knowledge Timeline:** (what they know and when they learn it)
- **Canon Notes:** (facts that must stay consistent)

---

### Locations

**Location Schema**
- **ID:**
- **Name:**
- **Type:** (interior, exterior, region, liminal space)
- **Parent Location:** (if nested)
- **Access Rules:** (how the player reaches it)
- **Key Features:** (distinctive objects, hazards, sensory cues)
- **State Variables:** (lighting, weather, damage, locks)
- **Linked Characters:** (who appears here and under what conditions)
- **Lore Ties:** (history or legend tied to the location)
- **Canon Notes:** (non-negotiable facts)

---

### Timeline

**Timeline Schema**
- **Event ID:**
- **Event Summary:**
- **Time Marker:** (date, time, or relative position)
- **Location:**
- **Characters Present:**
- **Trigger:** (what causes the event)
- **Consequences:** (state changes, new facts)
- **Player Visibility:** (known, discoverable, hidden)
- **Canon Notes:** (fixed beats that must not shift)

---

### Lore

**Lore Schema**
- **Lore ID:**
- **Statement:** (the fact or legend)
- **Type:** (history, myth, rule, technology, culture)
- **Source:** (witness, document, environmental clue)
- **Reliability:** (confirmed, rumored, disputed)
- **Linked Locations/Characters:**
- **First Appearance:** (scene or puzzle)
- **Canon Notes:** (what must remain true)

---

### Themes

**Theme Schema**
- **Theme ID:**
- **Theme Statement:** (what the story explores)
- **Core Question:** (the thematic question to answer)
- **Character Expression:** (who embodies it)
- **Location Expression:** (where it appears)
- **Puzzle/Interaction Expression:** (how it surfaces in play)
- **Resolution:** (how the theme is answered)
- **Canon Notes:** (non-negotiable thematic anchors)

---

## 2) Automatic Updating Rules (Canon Growth)

Use these rules to append new facts to canon after approval. These should be applied whenever new text, puzzles, or interactions are added.

**Rule A — Proposed Facts Log**
- New information goes into a **Proposed Facts** log first.
- Each entry must include **source**, **scene**, and **affected schema** (character/location/timeline/lore/theme).

**Rule B — Approval Gate**
- A proposed fact becomes canon only after approval.
- Approval can be a manual review or an LLM check that validates consistency with existing canon.

**Rule C — Canon Append**
- When approved, the fact is appended to the **relevant schema** and cross-linked:
  - Character facts update **Traits**, **Goals**, or **Arc**.
  - Location facts update **Key Features** or **State Variables**.
  - Timeline facts add a new **Event**.
  - Lore facts add a new **Lore Statement**.
  - Theme facts update **Theme Expression** or **Resolution**.

**Rule D — Version Stamp**
- Every approved fact gets a **Version Stamp** (date/iteration number) for traceability.

---

## 3) Contradiction Detection Step

Use this step whenever canon changes or new content is drafted.

**Check 1 — Schema Consistency Scan**
- Compare new facts against existing entries in the same schema.
- Flag mismatches in:
  - **Timeline ordering** (events out of order or mutually exclusive)
  - **Character state** (alive vs. dead, location conflicts, knowledge timing)
  - **Location logic** (access rules conflict, state variables mismatch)
  - **Lore reliability** (confirmed fact contradicts earlier confirmed fact)
  - **Theme coherence** (new content undermines theme statement)

**Check 2 — LLM Validation Prompt**
- Feed updated canon plus new fact into an LLM prompt:
  - **“Identify contradictions, missing dependencies, or timeline issues. Return a list of conflicts with IDs.”**
- Only accept changes that return **no contradictions** or have a resolution plan.

**Check 3 — Resolution Workflow**
- If contradiction found:
  - **Amend** the new fact,
  - **Recontextualize** older canon (if not locked), or
  - **Create an intentional contradiction** (must be labeled as such).

---

## 4) Canon Locking (Prevent Accidental Changes)

**Lock Rule**
- Mark critical entries as **Locked** to prevent edits.
- Locked entries can only be modified by explicit override.

**Lock Fields**
- **Lock Status:** (Locked / Unlocked)
- **Lock Reason:** (why it must not change)
- **Lock Owner:** (who approved the lock)
- **Lock Date:** (when it was locked)

**Locking Best Practices**
- Lock core character truths (identity, fate, arc endpoints).
- Lock major timeline beats that define the story.
- Lock foundational lore (rules of magic/technology).
- Lock theme statements once finalized.

---

## 5) Example Entry (Character)

**ID:** char-marina-hale
- **Name:** Marina Hale
- **Role:** Archivist NPC
- **Status:** alive
- **Traits:**
  - **Core:** meticulous, stubborn, protective
  - **Surface:** curt, precise, dry humor
  - **Contradictions:** distrusts authority but collects official records
- **Goals:**
  - **Short-Term:** keep the archive sealed
  - **Long-Term:** reveal the truth about the collapse
  - **Conflicts:** player’s curiosity; her fear of exposure
- **Arc:**
  - **Starting State:** refuses help
  - **Key Turns:** player retrieves lost ledger; she shares map
  - **Ending State:** chooses to trust the player
- **Knowledge Timeline:**
  - Knows the ledger exists (before game)
  - Learns player has access (mid-game)
- **Canon Notes:**
  - Marina cannot leave the archive.
  - She never lies about the collapse’s cause.
- **Lock Status:** Locked
- **Lock Reason:** foundational character truth
- **Lock Owner:** narrative lead
- **Lock Date:** 2024-04-12
