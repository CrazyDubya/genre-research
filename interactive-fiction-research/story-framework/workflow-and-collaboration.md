# Workflow, Collaboration, and Publishing Features

Practical guidance for managing interactive fiction drafts, reviewer feedback, and release-ready exports.

---

## 1. Version Control for Chapters and Scenes (with Diff Views)

**Goal:** Track changes to narrative content without losing earlier drafts or revisions.

**Recommendations:**
- **Scene-level versioning:** Maintain versions for each chapter or scene, not just the project as a whole.
- **Diff views:** Provide side-by-side or inline diffs for paragraphs, dialogue, and choices.
- **Named snapshots:** Label important versions (e.g., `Chapter 3 - combat rewrite`, `Puzzle flow rework`).
- **Branching drafts:** Allow parallel iterations for alternative endings or puzzle paths.
- **Restore points:** One-click rollback for any scene revision.

**Implementation checklist:**
- [ ] Store revisions per scene/chapter with timestamps and author tags.
- [ ] Provide paragraph-level diffs (additions, deletions, edits).
- [ ] Support comparison between any two versions.
- [ ] Allow snapshot tagging for major revisions.

---

## 2. Feedback Threads (Notes on Paragraphs/Scenes)

**Goal:** Capture reviewer feedback in-context without interrupting narrative flow.

**Recommendations:**
- **Paragraph anchoring:** Let reviewers attach notes to specific paragraphs, choices, or room descriptions.
- **Threaded discussions:** Support replies and resolution status (open/resolved).
- **Author action states:** Mark notes as “accepted,” “rejected,” or “pending.”
- **Visibility controls:** Filter by reviewer, status, or content type (scene, puzzle, description).
- **Version-aware notes:** Flag feedback linked to an earlier version when content has changed.

**Implementation checklist:**
- [ ] Comment anchors for paragraphs and choice blocks.
- [ ] Threaded replies and status tags.
- [ ] Resolve/unresolve toggles for editing workflows.
- [ ] Notifications or summary digests for new feedback.

---

## 3. Milestone Checkpoints (Draft → Beta → Final)

**Goal:** Create structured stages for review and publishing readiness.

**Recommended checkpoints:**
1. **Draft v1**
   - Core narrative complete
   - All puzzles implemented (rough form)
2. **Beta Review**
   - External readers provide feedback
   - Major narrative and puzzle issues addressed
3. **Final**
   - Prose polish
   - Testing passes complete
   - Export-ready

**Implementation checklist:**
- [ ] Project-level status field (Draft v1, Beta Review, Final).
- [ ] Gate requirements for each milestone (e.g., “No open critical feedback”).
- [ ] Snapshot or tag created automatically at each checkpoint.
- [ ] Changelog summary for milestone transitions.

---

## 4. Export Options (DOCX, PDF, EPUB)

**Goal:** Support multiple sharing and publishing formats with minimal reformatting effort.

**Recommended exports:**
- **DOCX:** For editorial collaboration and track changes.
- **PDF:** For clean review distribution.
- **EPUB:** For digital publishing and device testing.

**Formatting considerations:**
- Preserve **scene headings** and **choice blocks**.
- Convert **links or branching structures** to a readable linear format (appendices, flow notes).
- Include **metadata**: title, author, version, export date.
- Provide **export profiles** for beta vs. final formatting.

**Implementation checklist:**
- [ ] DOCX export with consistent heading and paragraph styles.
- [ ] PDF export with a clean, paginated layout.
- [ ] EPUB export with metadata and navigation.
- [ ] Branching structure appendix or flowchart section.

---

## Summary

A robust workflow for interactive fiction should combine:
- **Version control** at the scene level with clear diffs
- **Threaded feedback** attached directly to the narrative
- **Milestone checkpoints** with gated requirements
- **Export formats** that respect both prose and interactive structure
