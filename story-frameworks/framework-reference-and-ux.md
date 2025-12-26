# Story Framework Reference, Beat Schemas, and UX Integration

## 1. Concise Framework References

### Three-Act Structure
- **Purpose:** Classic pacing model for setup, confrontation, resolution.
- **Strengths:** Clear escalation, adaptable to most genres.
- **Typical use:** Novels, films, episodic arcs.

### Five-Act Structure
- **Purpose:** Expands three-act with more granular rising action and climax.
- **Strengths:** Better mid-story tension control, strong turning points.
- **Typical use:** Theatre, prestige TV, long-form narratives.

### Hero’s Journey (Monomyth)
- **Purpose:** Mythic arc of transformation through ordeal and return.
- **Strengths:** Strong emotional arc and thematic growth.
- **Typical use:** Quest stories, fantasy, adventure, character-driven epics.

### Save the Cat (STC)
- **Purpose:** Beat sheet that maps emotional and plot turning points.
- **Strengths:** Clear timing guidance, useful for outlining quickly.
- **Typical use:** Screenplays, commercial genre fiction.

## 2. Canonical Beat Schemas

> Each schema defines canonical beat names and ordering. Optional beats are marked.

### Three-Act Structure (Canonical Beats)
**Act I – Setup**
1. **Opening Image** – Tone, world, and main character.
2. **Theme Stated** – Hint of the story’s core question.
3. **Inciting Incident** – Disrupts the normal world.
4. **Debate** – Protagonist resists or considers action.
5. **Act I Break / Commitment** – Protagonist commits to a new path.

**Act II – Confrontation**
6. **Rising Action / Tests** – Obstacles, stakes rise.
7. **Midpoint** – Major revelation, reversal, or escalation.
8. **Bad Guys Close In** – Pressure intensifies; allies/frictions.
9. **All Is Lost** – Apparent defeat.
10. **Dark Night of the Soul** – Internal reckoning.

**Act III – Resolution**
11. **Climax** – Final confrontation and decisive choice.
12. **Resolution / Denouement** – New normal, thematic payoff.

### Five-Act Structure (Canonical Beats)
**Act I – Exposition**
1. **Opening Status Quo**
2. **Inciting Incident**
3. **First Turning Point** – Commits to conflict.

**Act II – Rising Action**
4. **Progress & Complications**
5. **Rising Stakes**
6. **Midpoint Reversal**

**Act III – Crisis**
7. **Major Setback**
8. **Crisis / Lowest Point**

**Act IV – Climax**
9. **Final Plan**
10. **Climactic Confrontation**

**Act V – Resolution**
11. **Falling Action**
12. **Denouement / New Equilibrium**

### Hero’s Journey (Canonical Beats)
1. **Ordinary World**
2. **Call to Adventure**
3. **Refusal of the Call** (optional)
4. **Meeting the Mentor**
5. **Crossing the Threshold**
6. **Tests, Allies, Enemies**
7. **Approach to the Inmost Cave**
8. **Ordeal**
9. **Reward (Seizing the Sword)**
10. **Road Back**
11. **Resurrection**
12. **Return with the Elixir**

### Save the Cat (Canonical Beats)
1. **Opening Image**
2. **Theme Stated**
3. **Set-Up**
4. **Catalyst**
5. **Debate**
6. **Break into Two**
7. **B Story**
8. **Fun and Games**
9. **Midpoint**
10. **Bad Guys Close In**
11. **All Is Lost**
12. **Dark Night of the Soul**
13. **Break into Three**
14. **Finale**
15. **Final Image**

## 3. Beat-to-GUI Data Structure Mapping

### Outline Node Schema
Use a normalized structure so beats can be rendered in a tree, list, or kanban.

```json
{
  "id": "beat_03_inciting_incident",
  "framework": "three_act",
  "act": "Act I",
  "beat_order": 3,
  "beat_name": "Inciting Incident",
  "summary": "A disruption that forces the protagonist to react.",
  "is_optional": false,
  "status": "planned",
  "scene_links": ["scene_012"],
  "goal": "Introduce the threat and raise stakes.",
  "stakes": "What happens if the hero ignores it?",
  "notes": "",
  "tags": ["turning_point", "setup"]
}
```

### Scene Goal Schema
Attach each beat to one or more scenes; each scene can carry a goal and outcome.

```json
{
  "scene_id": "scene_012",
  "beat_id": "beat_03_inciting_incident",
  "scene_goal": "Reveal the antagonist’s move.",
  "conflict": "Hero is unprepared for the threat.",
  "outcome": "Hero must respond; status quo is broken.",
  "characters": ["protagonist", "antagonist"],
  "location": "Downtown lab",
  "time": "Day 3"
}
```

### UI Rendering Guidance
- **Outline tree:** `Act → Beat → Scenes`.
- **Beat list:** Sort by `beat_order` and show `status` as a pill.
- **Scene board:** Group by `beat_name` or `act`.
- **Progress meter:** `% beats completed` + `key beats completed`.

## 4. Selection UX: Framework Pick → Beat Template

### Flow
1. **Framework chooser modal**
   - Options: Three-Act, Five-Act, Hero’s Journey, Save-the-Cat.
   - Each option shows a one-line description and expected beat count.
2. **Preview panel**
   - A small outline of acts and beat names.
   - Optional: example story artifact snippet.
3. **Confirm selection**
   - System generates beat nodes with default summaries and goals.
4. **Post-selection options**
   - Toggle optional beats.
   - Rename beats or merge beats.
   - Choose pacing template (slow/standard/fast) to stretch or compress beat spacing.

### Generation Logic (Pseudo)
```
beats = load_framework_beats(selected_framework)
for beat in beats:
  create_outline_node(beat)
  if beat.default_scene_count:
    create_placeholder_scenes(beat)
```

## 5. Validation Prompts (Progression Checks)

### General Prompts
- **Clarity:** “Does this beat advance the protagonist’s goal?”
- **Causality:** “What caused this beat, and what does it cause next?”
- **Stakes:** “What changes if the protagonist fails here?”
- **Character:** “What do we learn about the protagonist?”

### Beat-Specific Prompts (Examples)
- **Inciting Incident:** “Is the disruption strong enough to force response?”
- **Midpoint:** “What new information or reversal changes the trajectory?”
- **All Is Lost:** “What makes this feel like the lowest point?”
- **Climax:** “What decisive choice resolves the central conflict?”

### Automated Checklist per Framework
Attach a checklist to each beat with required fields:
- `summary` present
- `goal` present
- `stakes` present
- `scene_links` count ≥ 1

Trigger warnings if critical beats are missing or empty (e.g., Midpoint, Climax, Final Image).
