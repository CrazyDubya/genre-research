# Writing Flow UX Improvements

## 1. High-Friction Touchpoints

### Outline Creation
- **Blank-page overload:** Too many fields and structural choices before the writer has momentum.
- **Unclear starting point:** No strong entry prompt or default outline template.
- **Context switching:** Jumping between plot, character, and world tabs without a clear sequence.
- **Weak sense of progress:** Users can't see how close they are to a viable outline.

### Scene Transitions
- **Scene continuity confusion:** Hard to track what changed between scenes (stakes, POV, location).
- **Inconsistent scene handoffs:** No standard prompt for "what carries over" to the next scene.
- **Navigation friction:** Too many clicks to move to the next scene or compare scenes.

### Revisions
- **Revision overload:** Long lists of possible edits without prioritization.
- **No quick diff:** Hard to see before/after or the specific intent behind a change.
- **High cognitive load:** Users must remember original goals while rewriting.

## 2. Guided Flow Modes (Minimal Choices per Step)

### Mode A: "Quick Outline" (5–7 steps)
1. **Story Goal** → single prompt + example.
2. **Protagonist** → name, desire, obstacle.
3. **Inciting Incident** → short guided prompt.
4. **Midpoint Shift** → one forced choice (raise stakes / reveal / reversal).
5. **Climax** → single paragraph prompt.
6. **Resolution** → one sentence.
7. **Export Outline** → auto-structured summary.

### Mode B: "Scene Builder" (4 steps)
- Scene location & time
- Character entry point
- Scene goal & obstacle
- Exit point & consequence

### Mode C: "Revision Sprint" (3 steps)
- **Identify Pain Point** → pick 1 issue (pacing / dialogue / description)
- **AI Suggestion** → single LLM rewrite option
- **Accept / Reject** → approve or request alt

## 3. Revision Visibility Improvements

### Quick Diff View
- Side-by-side before/after
- Highlight what changed
- Show intent (why this change was made)

### Prioritized Edit Lists
- **Critical:** Plot consistency, character motivation
- **Important:** Pacing, scene transitions, voice fit
- **Polish:** Grammar, tone, descriptive depth

### Progress Tracking
- Revision checklist with completion %
- Scene completion status
- Overall document readiness score

## 4. Scene Navigation Enhancements

### Scene Card Dashboard
- Thumbnail view of all scenes
- Quick stats: word count, POV, tone
- Color-coded status (draft, revised, locked, exported)
- One-click jump to any scene

### Scene Continuity Panel
- "What carries over from previous scene"
- "What changes in this scene"
- "What sets up the next scene"
- Conflict/plot thread tracker

## 5. Guided Prompts (Minimal Cognitive Load)

### Outline Guidance
- "What does your protagonist want? (1 sentence)"
- "What stops them? (1 sentence)"
- "How do they overcome it? (1 sentence)"

### Scene Guidance
- "What's the scene goal?"
- "What's the obstacle?"
- "How does it resolve?"
- "What's the next scene consequence?"

### Revision Guidance
- "What's the main issue here?"
- "Suggested fix: [AI generates 1 option]"
- "Keep original / Use suggestion / Show me another option"

## 6. Feedback & Iteration Speed

### Real-Time Collaboration
- Comment threads on scenes
- Approval gates (author → editor → manager)
- Version history with restore points

### Quick Export Options
- "Export this scene"
- "Export current draft"
- "Export approved version"
- "Export with tracked changes"

## Implementation Priorities

### Phase 1 (MVP)
- Quick Outline mode
- Scene Builder basics
- Revision Sprint (AI suggestion + accept/reject)
- Basic scene continuity view

### Phase 2
- Full Scene Card Dashboard
- Prioritized edit lists
- Approval gates workflow
- Export with tracked changes

### Phase 3
- Advanced continuity checking
- Multi-author collaboration features
- Custom prompt templates
- Analytics & readiness scoring
