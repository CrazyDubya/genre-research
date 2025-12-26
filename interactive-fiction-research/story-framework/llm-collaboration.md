# LLM Collaboration Workflow for Interactive Fiction

**Purpose:** Define collaboration modes, decision tracking, and guardrails for LLM-assisted interactive fiction development.

---

## 1. Collaboration Modes

Use one of these modes per session or task. Make the mode visible in the UI header and in any system logs.

### **Ask-first**
- **Behavior:** LLM asks before making any material change or creative decision.
- **Best for:** Early ideation, sensitive canon work, high-stakes revisions.
- **Rule:** No edits without explicit user confirmation.

### **Suggest-then-accept**
- **Behavior:** LLM drafts suggestions, user approves before applying.
- **Best for:** Iterative writing, selective improvements, controlled drafting.
- **Rule:** Edits are staged until the user accepts them.

### **Auto-draft with edits**
- **Behavior:** LLM drafts automatically, user reviews and edits.
- **Best for:** Speed drafting, exploratory scenes, low-risk expansions.
- **Rule:** Always show a change summary and diff before finalizing.

### **Rewrite/expand**
- **Behavior:** LLM rewrites or expands user-provided text within specified constraints.
- **Best for:** Style polish, tone adjustments, or expansion tasks.
- **Rule:** Must preserve canon and narrative constraints unless user approves changes.

---

## 2. Decision Ledger (UI Requirement)

Maintain a **Decision Ledger** panel that logs key creative and structural choices.

**Log these decisions:**
- POV (first/second/third)
- Tense (past/present)
- Narrative voice and style notes
- Character traits and arcs
- Setting rules and world state
- Puzzle rules and interaction constraints
- Timeline anchors and cause/effect links

**Ledger entry format:**
- **Decision:** concise label
- **Detail:** short, specific description
- **Rationale:** why the choice was made
- **Scope:** chapter/scene/world/system
- **Status:** active / proposed / superseded
- **Linked artifacts:** story bible section, scene, or revision note

**UI behaviors:**
- Filter by scope (scene, chapter, world)
- Highlight conflicts (e.g., POV mismatch)
- One-click jump to affected content

---

## 3. Canon Change Confirmations

**Canon data includes:** story bible, timeline, core character traits, world rules, and established facts.

**Require explicit confirmation whenever the LLM proposes canon changes:**
- Changing POV or tense after set
- Altering character backstory or traits
- Modifying timeline anchors
- Introducing new world rules or exceptions
- Retconning established facts

**Confirmation checklist (must be shown to user):**
- What canon item changes
- Why the change is needed
- Which scenes are affected
- Alternative options that preserve canon

**Rule:** No canon change is applied without user confirmation.

---

## 4. Clarifier Checkpoints (Hallucination Guardrails)

Insert “request a clarifier” checkpoints when the model lacks verified context.

**Trigger conditions:**
- Missing or ambiguous timeline data
- Unclear character motivations or traits
- Unspecified rules for magic/tech systems
- Conflicting notes in the story bible
- A required fact is missing from the current scene context

**Clarifier prompt template:**
- **Missing detail:** [specific gap]
- **Why needed:** [impact on scene or consistency]
- **Options:** [2–3 plausible choices]
- **User ask:** “Which should we use?”

**Rule:** Do not fabricate missing canon or timeline information.

---

## 5. “What Changed?” Diff Views

Provide a **diff view** for any edit or rewrite so the user can review changes precisely.

**Diff requirements:**
- Inline additions and deletions
- Change summary (bulleted)
- Link to the Decision Ledger entry (if applicable)
- Ability to accept/reject per change block

**Use cases:**
- Line edits of prose
- Structural changes (reordered scenes)
- Canon changes (must also trigger confirmation flow)

---

## Quick Implementation Checklist

- [ ] Choose collaboration mode at session start
- [ ] Show Decision Ledger panel with filters and conflicts
- [ ] Gate canon changes behind explicit confirmation
- [ ] Insert clarifier checkpoints when context is missing
- [ ] Provide “What Changed?” diff views before finalizing edits

---

**Outcome:** A collaboration system that protects canon, increases transparency, and prevents hallucinated changes while enabling fast, controlled drafting.
