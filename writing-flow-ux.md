# Writing Flow UX Improvements

## 1. High-Friction Touchpoints

### Outline Creation
- **Blank-page overload:** Too many fields and structural choices before the writer has momentum.
- **Unclear starting point:** No strong entry prompt or default outline template.
- **Context switching:** Jumping between plot, character, and world tabs without a clear sequence.
- **Weak sense of progress:** Users can’t see how close they are to a viable outline.

### Scene Transitions
- **Scene continuity confusion:** Hard to track what changed between scenes (stakes, POV, location).
- **Inconsistent scene handoffs:** No standard prompt for “what carries over” to the next scene.
- **Navigation friction:** Too many clicks to move to the next scene or compare scenes.

### Revisions
- **Revision overload:** Long lists of possible edits without prioritization.
- **No quick diff:** Hard to see before/after or the specific intent behind a change.
- **High cognitive load:** Users must remember original goals while rewriting.

## 2. Guided Flow Modes (Minimal Choices per Step)

### Mode A: “Quick Outline” (5–7 steps)
1. **Story Goal** → single prompt + example.
2. **Protagonist** → name, desire, obstacle.
3. **Inciting Incident** → short guided prompt.
4. **Midpoint Shift** → one forced choice (raise stakes / reveal / reversal).
5. **Climax** → single paragraph prompt.
6. **Resolution** → one sentence.
7. **Export Outline** → auto-structured summary.

### Mode B: “Scene Builder” (4 steps)
1. **Scene Intent** (choose 1: advance plot / reveal character / raise stakes).
2. **Setup** (location + POV + time).
3. **Conflict/Change** (what shifts by end of scene).
4. **Carryover** (what must be remembered for next scene).

### Mode C: “Revision Sprint” (3 steps)
1. **Pick Focus** (clarity / pacing / character / stakes).
2. **Show Key Passages** (auto-highlight likely weak spots).
3. **Apply Fix** (one-click suggestions + manual edit).

## 3. Defaults and Quick Actions

### Defaults
- **Outline templates:** pre-fill standard beats (three-act or save-the-cat).
- **Scene scaffolds:** default structure with placeholders (Goal → Conflict → Change → Aftermath).
- **Revision focus:** default to “clarity” if no preference given.

### Quick Actions
- **One-click Scene Scaffold:** generate placeholder headings + prompts.
- **Auto-summarize scene:** 1–2 sentence recap to confirm intent.
- **Instant handoff:** “Create next scene” pre-fills carryover fields.
- **Progress quicknav:** jump to “next missing field.”

## 4. Progressive Disclosure UI Patterns

- **Collapsed advanced controls:** show only basics unless user expands (e.g., “POV timing,” “subtext,” “secondary goal”).
- **Layered templates:** start with a minimal scene card; expand to add beats, tension arc, or dialogue cues.
- **Inline tips on demand:** tooltips or “show examples” toggles rather than always-visible text blocks.
- **Smart defaults with override:** hide advanced controls unless user clicks “Customize.”
- **Contextual nudges:** only show revision advice after a draft is complete.

## 5. User Testing Criteria (Validation)

### Metrics
- **Time-to-first-draft:** target time from start to first complete scene/outline.
- **Drop-off points:** identify step or screen with highest exit rate.
- **Completion rate per mode:** how many users finish Quick Outline or Scene Builder.
- **Editing depth:** number of changes after first draft (signals whether prompts are useful).

### Success Criteria
- **< 15 minutes** to produce a usable outline in Quick Outline mode.
- **< 5 minutes** to create a complete scene scaffold.
- **Drop-off reduced by 25%** on outline and scene flows.
- **Positive task confidence score** (user self-report after completing flow).

### Testing Structure
- **A/B test guided vs. full UI.**
- **Timed task:** create one scene and transition to the next without assistance.
- **Qualitative review:** ask users which step felt most confusing.
