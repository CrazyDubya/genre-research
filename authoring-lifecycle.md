# Authoring Lifecycle Map

This document outlines the authoring lifecycle, the user decision points in each phase, required UI surfaces, data captured per phase, and guardrails that guide iterative progress.

## 1) Lifecycle phases (concept discovery → final compile)

1. **Concept discovery**
2. **Premise selection**
3. **Outline**
4. **Scene planning**
5. **Drafting**
6. **Revision**
7. **Line-edit**
8. **Final compile**

---

## 2) User decision points per phase

- **Concept discovery**
  - Capture/accept raw ideas (seed prompts, genre mashups, themes, what-if questions).
  - Decide whether to save an idea to a project backlog.
- **Premise selection**
  - Choose a premise from the backlog (or create a new one).
  - Confirm target audience/genre fit and scope (novel/novella/short).
  - Approve a premise as the project anchor.
- **Outline**
  - Select an outline depth (beats-only vs detailed chapter outline).
  - Lock the macro-structure (acts, major beats, midpoint, climax).
  - Approve the outline as draft-ready.
- **Scene planning**
  - Decide on scene list completeness (minimum viable vs exhaustive).
  - Approve scene objectives, POV, and setting for each scene.
  - Lock the scene list before drafting (or choose outline-light).
- **Drafting**
  - Accept/reject draft text per scene.
  - Decide whether to iterate within drafting or move to revision.
  - Mark draft as complete (first draft “done”).
- **Revision**
  - Prioritize revision focus (structure, character arc, pacing, stakes).
  - Accept/reject structural changes and reordering.
  - Lock major revisions before line-edit.
- **Line-edit**
  - Approve style pass (voice consistency, clarity, cadence).
  - Accept/reject sentence-level edits and continuity fixes.
  - Mark line-edit complete.
- **Final compile**
  - Select export format(s) (DOCX, PDF, EPUB, Fountain, etc.).
  - Confirm metadata (title, author, copyright, blurb).
  - Final approval for release/export.

---

## 3) Required UI surfaces

- **Project dashboard**
  - Phase status, progress indicators, quick links, backlog.
- **Story bible**
  - World, characters, themes, tone, rules, and constraints.
- **Outline editor**
  - Beat/act view with drag-and-drop structure.
- **Scene workspace**
  - Scene list + per-scene planning + drafting editor.
- **Revision review**
  - Change lists, reordering, revision notes, comparisons.
- **Export**
  - Final compile settings and format outputs.

---

## 4) Data stored per phase

- **Concept discovery**
  - Idea seeds, themes, genre tags, tone snippets, references, inspiration links.
- **Premise selection**
  - Selected premise summary, target audience, stakes statement, core conflict.
- **Outline**
  - Act/beat structure, thematic throughline, major turning points, timeline constraints.
- **Scene planning**
  - Scene list, POV per scene, location, objective, conflict, outcome, setup/payoff links.
- **Drafting**
  - Scene draft text, word counts, inline notes, draft status flags.
- **Revision**
  - Revision plan, structural change log, character arc deltas, pacing notes.
- **Line-edit**
  - Style decisions (voice, tense, diction), consistency log, line edits.
- **Final compile**
  - Export settings, final metadata, versioned output artifacts.

**Cross-phase data (persistent):**
- **Story bible**: tone, POV rules, themes, character arcs, setting canon, timeline constraints, glossary.
- **Project metadata**: title, author, genre, formats, status, collaborators.

---

## 5) Guardrails for iterative progress

- **Phase gating (default):**
  - Lock outline before drafting.
  - Lock major revisions before line-edit.
  - Require line-edit completion before final compile.
- **Optional “outline light” mode:**
  - Allows drafting with a minimal beat list, but requires scene list completion before 25% draft progress.
- **Revision checkpointing:**
  - Require a revision plan before major reordering.
  - Track accepted/rejected changes with audit history.
- **Scope control:**
  - Warn on premise changes after outline lock; require explicit re-approval.
- **Progress integrity:**
  - Enforce explicit phase transitions and “done” confirmations to prevent accidental skips.
