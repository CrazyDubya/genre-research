# Interactive Fiction Revision Checklist

**Systematic guide to revising and polishing your Interactive Fiction. Use this checklist to ensure quality, consistency, and player satisfaction.**

---

## Phase 1: World and Map

### Map Consistency
- [ ] All rooms connected logically (no impossible geography)
- [ ] Exits match (if Room A is north of Room B, Room B is south of Room A)
- [ ] No dead-end rooms without purpose
- [ ] Map flows naturally (player can navigate without frustration)
- [ ] Each room unique (no duplicate descriptions)

### Room Descriptions
- [ ] Every room has clear, distinctive description
- [ ] Room descriptions establish mood and atmosphere
- [ ] Sensory details present (sight, sound, smell where appropriate)
- [ ] Each room has 3-5 significant, interactive objects
- [ ] Room descriptions contain at least one subtle clue or hook
- [ ] Exits clearly indicated
- [ ] Description length appropriate (longer for exploration areas, shorter for action)
- [ ] No generic placeholder descriptions

### Environmental Storytelling
- [ ] Room descriptions reveal story/history
- [ ] Objects reveal character or plot information
- [ ] World feels lived-in and consistent
- [ ] Details reward careful observation and re-reading
- [ ] Environmental clues support main narrative
- [ ] Puzzles emerge naturally from environment

---

## Phase 2: Objects and Items

### Object Quality
- [ ] Every object has reason to exist
- [ ] Object descriptions are specific and detailed
- [ ] Important objects are clearly distinguished from scenery
- [ ] Scenery objects enhance atmosphere
- [ ] Interactive objects are hinted at (not hidden arbitrarily)
- [ ] Takeable objects clearly marked
- [ ] Object uses logical and intuitive

### Object Descriptions
- [ ] Each object has unique examination description
- [ ] Objects reveal information when examined
- [ ] Hidden properties revealed on examination
- [ ] Object descriptions vary (not repetitive)
- [ ] Containers function correctly
- [ ] Object state changes appropriately

---

## Phase 3: Puzzles

### Puzzle Fairness
- [ ] All required clues provided
- [ ] Clues findable through exploration
- [ ] Solutions logical and derivable
- [ ] No "guess the verb" problems
- [ ] No pixel hunting (text equivalent)
- [ ] Appropriate difficulty for game stage
- [ ] Solutions integrated into story
- [ ] Wrong answer feedback helpful but not giving away

### Puzzle Integration
- [ ] Puzzles advance story or reveal information
- [ ] Puzzle rewards worth effort
- [ ] Puzzles create "aha!" moments
- [ ] Multiple hint opportunities if player stuck
- [ ] Puzzles escalate in difficulty appropriately
- [ ] Each puzzle unique (not repetitive)

### Puzzle Flow
- [ ] Puzzles can be solved in logical order
- [ ] Required information available when needed
- [ ] No soft locks (player can't get stuck permanently)
- [ ] Backtracking minimized or justified
- [ ] Puzzles don't block progression unfairly

---

## Phase 4: NPCs

### NPC Quality
- [ ] Each NPC has distinct personality
- [ ] NPC dialogue matches their character
- [ ] NPCs provide useful information
- [ ] NPCs have knowledge limits (realistic)
- [ ] NPC behavior consistent
- [ ] NPCs remember player interactions (if designed to)
- [ ] NPC movement/presence logical

### NPC Implementation
- [ ] NPCs appear/disappear appropriately
- [ ] NPC dialogue topics clear
- [ ] ASK/TELL topics relevant
- [ ] NPC responses vary appropriately
- [ ] NPCs don't break game logic

---

## Phase 5: Commands and Interactions

### Command Coverage
- [ ] All significant objects interactable
- [ ] Standard verbs work where expected (OPEN doors, TAKE items)
- [ ] Synonyms accepted (not just one specific word)
- [ ] Failed attempts give helpful feedback
- [ ] Unusual actions have appropriate responses
- [ ] No actions crash the game

### Custom Commands
- [ ] Custom commands intuitive
- [ ] Syntax clear and consistent
- [ ] Help available if needed
- [ ] Experimental commands signposted

---

## Phase 6: Player Experience

### Goal Clarity
- [ ] Player understands overall objective
- [ ] Short-term goals clear
- [ ] Progress indicators present
- [ ] Player knows when they've accomplished something

### Guidance
- [ ] Game provides hints if player stuck
- [ ] Not stuck forever (hint system or gentle nudges)
- [ ] Tutorial for unique mechanics (if any)
- [ ] Early puzzles teach mechanics

### Agency and Satisfaction
- [ ] Player choices matter
- [ ] Solving puzzles feels rewarding
- [ ] Exploration rewarded
- [ ] Aha! moments deliver satisfaction
- [ ] Player feels clever, not frustrated

---

## Phase 7: Writing Quality

### Prose Style
- [ ] Writing consistent throughout
- [ ] Tone matches genre and story
- [ ] No typos or grammatical errors
- [ ] Descriptions vivid and specific
- [ ] Avoid repetitive words/phrases
- [ ] Show, don't tell (especially in descriptions)

### System Messages
- [ ] Default messages replaced with custom ones
- [ ] Error messages helpful and thematic
- [ ] Success messages satisfying
- [ ] Message tone consistent with game

---

## Phase 8: Technical

### Implementation
- [ ] No bugs or crashes
- [ ] All exits functional
- [ ] All objects coded correctly
- [ ] All puzzles implemented
- [ ] Game is winnable
- [ ] No broken states (can't continue)

### Edge Cases
- [ ] Tested unusual actions
- [ ] Tested taking everything
- [ ] Tested dropping everything
- [ ] Tested going in circles
- [ ] Tested dying/restarting (if applicable)

---

## Phase 9: Interactive Fiction Specifics

### Parser-Based Elements
- [ ] Navigation smooth and intuitive
- [ ] Object handling works correctly
- [ ] Inventory management clear
- [ ] Command parsing generous (accepts synonyms)
- [ ] Ambiguous commands handled gracefully
- [ ] No parser guess-the-verb issues

### Player Agency
- [ ] Multiple approaches possible (where appropriate)
- [ ] Player can examine world freely
- [ ] Not overly linear (exploration allowed)
- [ ] Player doesn't feel railroaded

### Environmental Storytelling
- [ ] World tells story through details
- [ ] Revisiting rooms reveals new information
- [ ] Details gain meaning with knowledge
- [ ] World consistent and believable

---

## Phase 10: Final Polish

### Walkthrough
- [ ] Complete walkthrough exists
- [ ] Game winnable from start to finish
- [ ] All puzzles solvable
- [ ] No dead ends
- [ ] All content accessible

### Replay Value
- [ ] Details discovered on replay
- [ ] Alternative approaches possible
- [ ] Environmental layers revealed

### Player Testing
- [ ] Tested by multiple players
- [ ] Feedback addressed
- [ ] Common frustrations identified and fixed
- [ ] Win rate appropriate (not too easy/hard)

---

## Quick Checks

### Critical Must-Haves
- [ ] Game is completable
- [ ] No bugs that prevent progress
- [ ] All puzzles fair and solvable
- [ ] Clear objectives
- [ ] Satisfying conclusion

### Quality Markers
- [ ] Writing is polished
- [ ] World is coherent
- [ ] Player feels smart when solving puzzles
- [ ] Environmental storytelling rewards exploration
- [ ] NPC interactions meaningful
- [ ] Consistent tone and style

---

## Common Problems to Check For

**Guess the Verb:**
- [ ] Player knows solution but can't figure out command
- Fix: Accept multiple synonyms, make commands intuitive

**Hidden Objects:**
- [ ] Required objects too obscure to find
- Fix: Make important objects visible in room descriptions

**Arbitrary Puzzles:**
- [ ] Solutions don't follow from clues
- Fix: Ensure all puzzles have logical clue paths

**Soft Locks:**
- [ ] Player can get stuck permanently
- Fix: Provide ways out, prevent unrecoverable states

**Vague Goals:**
- [ ] Player doesn't know what to do
- Fix: Clarify objectives through environmental clues or early guidance

**Repetitive Descriptions:**
- [ ] Room descriptions feel same-y
- Fix: Give each room distinctive features and mood

---

## Testing Questions

**Ask Testers:**
- Did you know what you were trying to accomplish?
- Were any puzzles frustrating or unfair?
- Did you ever feel stuck? Where?
- Did you know where to go next?
- What was your favorite moment? Least favorite?
- Did the world feel coherent?
- Did you want to keep exploring?

---

## Priority Revisions

**If Time Is Limited, Prioritize:**

1. **Critical:** Fix bugs, ensure game is winnable
2. **High:** Fix unfair puzzles, improve goal clarity
3. **Medium:** Improve prose, enhance descriptions
4. **Low:** Add polish, enhance hints, expand content

---

## Final Questions

**Before Release:**
- Is this fair to players?
- Is this satisfying to complete?
- Does this deliver on its premise?
- Would you recommend this to others?
- Does this honor the IF tradition?

---

**End of Checklist**

---

**Usage:**
1. Complete first draft
2. Use checklist systematically
3. Revise based on each phase
4. Test with real players
5. Return to checklist for final polish
6. Release when all critical items checked

---

## Readability, Vocabulary, and Style Checks
- [ ] Readability score measured (e.g., Flesch-Kincaid) matches target audience.
- [ ] Sentence length distribution supports intended pace.
- [ ] Vocabulary level consistent (no random shifts in formality/complexity).
- [ ] Jargon/slang is either clear from context or defined.
- [ ] Repetitive words/phrases reduced.

## Pacing Analysis (Scene Length + Tension Curve)
- [ ] Scene lengths tracked (word/page count) and vary intentionally.
- [ ] Long scenes broken with beats or transitions where needed.
- [ ] Tension curve plotted across the story (rises, releases, peaks).
- [ ] Major releases placed after high-tension scenes.

## Tone and Voice Consistency Audit
- [ ] Narrative tone consistent with genre expectations.
- [ ] POV voice stable across chapters/sections.
- [ ] Character voices maintain consistent diction and cadence.
- [ ] Tonal shifts are deliberate and signposted.

## Target Audience Alignment
- [ ] Target audience defined (age, subgenre, sensitivity).
- [ ] Content intensity matches audience expectations.
- [ ] Complexity matches audience comfort (plot density, jargon, mechanics).
- [ ] Hook/logline reflects what the audience wants.
