# Style Integrity Guidelines (Originality-First)

These guidelines define how to support **style inspiration** without close imitation or paraphrase. They are intended for tools that take user samples and output new writing that is **original in content** while **inspired by high-level stylistic traits**.

---

## 1. Acceptable Style Targets (No Direct Imitation)

Style targets must be **abstract and non-identifying**. Avoid naming authors, titles, or quoting unique lines. Acceptable targets focus on *how* text feels rather than *what* it says.

**Allowed style dimensions:**
- **Tone:** emotional posture (e.g., hopeful, clinical, ominous, playful)
- **Register:** formality level (e.g., colloquial, academic, legalistic)
- **Rhythm:** cadence patterns (e.g., short punchy sentences; long periodic sentences; varied sentence length)
- **Diction:** general vocabulary band (e.g., simple vs. ornate; concrete vs. abstract)
- **Imagery density:** amount of sensory detail vs. plain exposition
- **Narrative distance:** intimate vs. detached perspective
- **Dialogue style:** terse, overlapping, lyrical, etc.

**Explicitly disallowed targets:**
- Explicitly naming living authors or specific works as models
- Mimicking distinctive phrasing, catchphrases, or signature idioms
- Reusing the same subject matter, metaphors, or plot beats from samples

---

## 2. Style Guide Inputs (User Samples + “Do Not Emulate” Rules)

When users provide samples, treat them as **feature extraction inputs**, not templates. Also allow users to provide **negative constraints**.

**Input structure:**
- **Samples (required):** user-provided passages used to infer style traits.
- **Do-not-emulate list (required):**
  - Words, phrases, or metaphors to avoid
  - Named entities (authors, characters, places)
  - Signature constructions (e.g., “As X would say…”) to exclude

**Processing expectations:**
- Extract only **high-level traits** (tone, register, rhythm, density, POV distance).
- Strip or mask **named entities** and **distinctive phrases** during analysis.
- Persist a “negative constraint” list for generation and post-checks.

---

## 3. Similarity Checks (Prevent Close Paraphrase)

Add automated checks to ensure outputs do not closely track user samples.

**Recommended checks:**
- **N-gram overlap limits:** reject or rewrite if 6–8 word overlap exceeds a low threshold.
- **Semantic similarity threshold:** run embedding similarity and flag outputs that exceed the allowed distance to any sample.
- **Rare-phrase detection:** block reuse of unusual multiword phrases found in samples.
- **Entity overlap:** prevent reuse of named entities from samples unless user explicitly allowed them.

**Behavior:**
- If a check fails, either **regenerate with stricter constraints** or **surface a warning** and request revised inputs.

---

## 4. “Inspired By” Prompting (Style > Content)

Prompts should explicitly discourage content reuse and direct the model to produce **fresh ideas**.

**Prompt pattern:**
- “Write an original passage *inspired by* the following stylistic traits.”
- “Do **not** reuse topics, scenes, or metaphors from the samples.”
- “Avoid named entities, unique phrases, and plot structures from the inputs.”

**Example prompt skeleton:**
> “Generate an original scene with [tone], [register], [rhythm]. Avoid subject matter and metaphors used in the samples. Do not echo sample phrasing; prefer novel imagery and content.”

---

## 5. Disclaimers and UI Cues (Originality + Attribution)

The UI should reinforce originality and transparent use of user inputs.

**UI cues:**
- “Inspired by style, not content.”
- “No direct imitation or paraphrase of samples.”
- “Output is original; attribution applies only to user-provided samples.”

**Disclaimers (recommended placement):**
- **Before generation:** “Samples are used to infer general style features only.”
- **After generation:** “The output is newly generated and does not copy sample content.”
- **In help/tooltips:** explain how similarity checks and do-not-emulate rules work.

---

## Implementation Checklist (Quick Reference)

- [ ] Define allowed style dimensions (tone/register/rhythm/diction/imagery).
- [ ] Capture and enforce do-not-emulate rules.
- [ ] Mask named entities before style extraction.
- [ ] Run n-gram, semantic, and rare-phrase similarity checks.
- [ ] Use prompts that emphasize “inspired by” traits only.
- [ ] Display originality disclaimers and attribution cues in UI.
