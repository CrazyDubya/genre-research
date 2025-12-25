# Command & Interaction Mechanics

**Understanding how players interact with Interactive Fiction worlds.**

---

## Understanding Interaction Mechanics

### The Foundation: Parser Systems

In Interactive Fiction (IF), parser systems serve as the communication bridge between player intentions and the fictional world. The parser interprets typed commands and generates appropriate world responses.

**Core Components:**
- **Input Processing:** How commands are understood
- **Action Handling:** What happens when commands are executed
- **Response Generation:** How the world responds to actions
- **State Management:** How the world changes and persists
- **Error Handling:** How invalid or impossible actions are addressed

### Parser Types

#### 1. Full Parser
- **Definition:** Understands complex sentence structures
- **Example:** "Give the red key to the old woman near the fountain"
- **Advantages:** Natural language feel, flexible command structure
- **Disadvantages:** Complex programming, potential for misunderstanding
- **Best Used By:** Experienced players, complex simulation games

#### 2. Abbreviated Parser
- **Definition:** Accepts shortened command forms
- **Example:** "GIVE KEY WOMAN" instead of full sentence
- **Advantages:** Faster input, simpler programming
- **Disadvantages:** Less natural language, learning curve
- **Best Used By:** General audience, faster-paced games

#### 3. Menu-Based Parser
- **Definition:** Offers limited pre-selected options
- **Example:** "What would you like to do? A) Give key B) Talk to woman C) Examine fountain"
- **Advantages:** No learning curve, clear options
- **Disadvantages:** Less freedom, less immersive
- **Best Used By:** New players, narrative-focused games

#### 4. Hybrid Parser
- **Definition:** Combines multiple input methods
- **Example:** Menu for basic actions, parser for complex ones
- **Advantages:** Flexible, user-friendly
- **Disadvantages:** More complex to design
- **Best Used By:** Mixed audiences, complex games

---

## Command Processing

### Standard Command Structure

#### Two-Part Commands
- **Structure:** VERB NOUN
- **Examples:** "take lamp", "open door", "examine book"
- **Processing:** The verb indicates the action, the noun indicates the target
- **Variations:** "take the lamp", "TAKE LAMP", "get lamp"

#### Three-Part Commands
- **Structure:** VERB NOUN PREPOSITION NOUN
- **Examples:** "put key in box", "give apple to guard", "climb up ladder"
- **Processing:** More complex action affecting multiple objects
- **Variations:** "PUT KEY IN BOX", "put key inside box"

#### Four-Part Commands
- **Structure:** VERB NOUN PREPOSITION NOUN PREPOSITION NOUN
- **Examples:** "pour water from bottle into cup", "throw rock at window with force"
- **Processing:** Complex interactions involving multiple objects
- **Variations:** "POUR WATER INTO CUP FROM BOTTLE"

### Command Vocabulary

#### Essential Verbs
- **Movement:** go, walk, run, climb, enter, exit, up, down, north, south, east, west
- **Examination:** look, examine, x, inspect, read, search
- **Manipulation:** take, get, drop, put, open, close, lock, unlock, push, pull, turn
- **Interaction:** talk to, ask, tell, give, show, attack, hit, kiss
- **Self-Action:** eat, drink, wear, remove, inventory, save, restore

#### Extended Verbs
- **Environmental:** light, extinguish, turn on, turn off, switch, flip
- **Social:** smile, nod, wave, bow, ignore, follow, wait
- **Transportation:** drive, ride, board, sail, fly
- **Crafting/Use:** make, build, fix, repair, combine, mix

### Synonym Management

#### Standard Synonyms
Provide multiple ways to express the same action:
- **Take:** get, pick up, grab, acquire
- **Look:** examine, inspect, x, check, view, see, study
- **Go:** walk, travel, move, proceed, head
- **Open:** unlock, pry, force

#### Contextual Synonyms
Some verbs should work differently depending on object type:
- **Open door** vs. **read book** vs. **drink water**
- **Climb tree** vs. **climb stairs** vs. **climb rope**
- **Turn key** vs. **turn page** vs. **turn light**

---

## Response Generation

### Standard Response Types

#### Success Responses
When an action works as intended:
- **Simple:** "You take the lamp."
- **Descriptive:** "You grasp the brass lamp and swing it free from its hook. It feels heavier than expected."
- **Consequential:** "You take the lamp just as the candle flickers out. Now you have a light source."

#### Failure Responses
When something doesn't work:
- **Simple:** "The door is locked."
- **Helpful:** "The door is locked. You'll need to find a key."
- **Alternative:** "The door is locked, but the window beside it is slightly ajar."

#### Ambiguous Responses
When commands are unclear:
- **Clarification:** "Which book do you mean, the red one or the blue one?"
- **Options:** "Do you want to take the book, examine it, or read it?"
- **Default:** "You'll need to be more specific."

### Response Quality Standards

#### Informative
- **Purpose:** Give players useful information
- **Example:** Instead of "You can't do that," say "The door is painted shut with years of paint."
- **Benefit:** Helps players understand the world and find alternative actions

#### Atmospheric
- **Purpose:** Maintain world immersion and mood
- **Example:** Instead of "The door is locked," say "The ancient oak door stands firm, its iron hinges green with age."
- **Benefit:** Enhances story experience through interaction

#### Consistent
- **Purpose:** Maintain world logic and logic
- **Example:** If the book is described as leather-bound in one room, don't call it paper in another.
- **Benefit:** Maintains player trust and world believability

#### Helpful
- **Purpose:** Allow players to progress without getting hopelessly stuck
- **Example:** "The door is painted shut. You might try something sharp to pry it open."
- **Benefit:** Maintains challenge without creating impossible situations

---

## State Management

### World State Variables

#### Object States
Track the condition and location of objects:
- **Location:** Where is the object currently?
- **Condition:** Open/closed, locked/unlocked, on/off, broken/intact? 
- **Properties:** Can it be taken, does it provide light, is it an ingredient?
- **History:** What has happened to this object? Who interacted with it?

#### Environmental States
Track the overall world conditions:
- **Time:** Time of day, day of week, season, weather
- **Lighting:** Lit areas, dark areas, light sources
- **Accessibility:** Which areas are available to enter?
- **Ambient Conditions:** Temperature, humidity, sound levels

#### Character States
Track NPCs and the player character:
- **Location:** Where are they currently?
- **Health:** Are they injured or healthy?
- **Mood:** Are they friendly, hostile, neutral, afraid?
- **Knowledge:** What information do they possess?

### State Change Logic

#### Immediate Effects
Changes that happen right away:
- **Object Movement:** "take lamp" moves lamp to inventory
- **Door State:** "open door" changes door to open state
- **Item Condition:** "light candle" changes candle to lit state

#### Delayed Effects
Changes that happen after time passes:
- **Timer Events:** "After 10 turns, the door slams shut"
- **Environmental Changes:** "The candle will burn out in 20 turns"
- **Character Actions:** "The guard will return in 5 turns"

#### Conditional Effects
Changes based on other factors:
- **Prerequisites:** "Can only open with key present"
- **Character Stats:** "Requires strength of 8 or higher"
- **World State:** "Only works if it's nighttime"

---

## Error Handling

### Common Error Types

#### Syntax Errors
- **Problem:** "I don't understand 'frizzle the blort' or 'grabby grabby with the thing'"
- **Solution:** Provide standard verbs or ask for clarification
- **Example Response:** "You can try basic actions like 'take', 'look at', or 'open'."

#### Semantic Errors  
- **Problem:** "You can't take the sky" or "You can't open the idea"
- **Solution:** Acknowledge the impossibility with style
- **Example Response:** "That doesn't seem to be something you can interact with."

#### Prerequisites Errors
- **Problem:** "You need to have the key to unlock this door"
- **Solution:** Clearly state what's needed
- **Example Response:** "The door is locked. You'll need a key to open it."

#### Physical Limitation Errors
- **Problem:** "The door is too heavy to lift" or "You're not strong enough"
- **Solution:** Acknowledge the limitation and suggest alternatives
- **Example Response:** "The door is too heavy to lift. It's meant to be opened, not moved."

### Graceful Error Handling

#### Helpful Suggestions
- **Instead of:** "I don't understand"
- **Try:** "You might try 'examine', 'take', or 'open'"

#### Contextual Responses
- **Instead of:** "You can't do that"
- **Try:** "The door is reinforced with steel. You'd need something to cut through it."

#### Creative Responses
- **Instead of:** "That doesn't make sense"
- **Try:** "You try to think of a way to make it work, but physics doesn't seem to cooperate."

---

## Advanced Techniques

### Dynamic World Simulation

#### Physics Systems
Implement realistic world behaviors:
- **Gravity:** Items fall when dropped
- **Containment:** Items stay in containers unless removed
- **Liquid Properties:** Liquids pour and fill containers
- **Light Sources:** Light illuminates dark areas

#### Character AI
Make NPCs respond intelligently:
- **Goal-Oriented Behavior:** NPCs try to achieve objectives
- **React to Environment:** NPCs respond to world changes
- **Memory:** NPCs remember recent interactions
- **Mood Systems:** NPC behavior changes based on history

### Adaptive Narratives

#### Player Modeling
Track player preferences and style:
- **Aggressive/Passive:** How does the player prefer to handle conflicts?
- **Cautious/Curious:** How thoroughly does the player explore?
- **Direct/Methodical:** How does the player approach puzzles?

#### Content Adaptation
Modify experience based on player style:
- **Challenge Level:** Adjust difficulty based on success rate
- **Content Focus:** Emphasize preferred interaction types
- **Narrative Branching:** Slightly alter story based on choices

### Immersive Elements

#### Sensory Details
Include non-visual information:
- **Sound:** "The floorboards creak under your weight"
- **Smell:** "The air smells of old books and dust"
- **Touch:** "The door handle is cool beneath your fingers"
- **Taste:** "The water tastes metallic and cold"

#### Environmental Storytelling
Convey narrative through interactive elements:
- **Environmental Clues:** Objects showing past events
- **Character Information:** Personal belongings revealing personalities
- **Mood Setting:** Environmental details that establish atmosphere

---

## Common Mechanics Problems and Solutions

### Problem: "Guess the Verb"
**Symptoms:** Players can't figure out the right command to accomplish their goal.
**Solutions:**
- Implement synonyms for common verbs
- Look for alternative ways to express the same action
- Provide contextual hints through environment descriptions

### Problem: "Guess the Noun"
**Symptoms:** Players can't figure out what object they need to interact with.
**Solutions:**
- Make important objects more prominent in room descriptions
- Use multiple names for important objects
- Provide environmental clues about important objects

### Problem: "Unresponsive World"
**Symptoms:** Most player commands generate unhelpful responses.
**Solutions:**
- Implement more comprehensive response libraries
- Focus on making every object have some form of response
- Prioritize responses for likely player actions

### Problem: "Magic Words"
**Symptoms:** Only specific command phrases work for certain actions.
**Solutions:**
- Implement more robust synonym systems
- Use natural language processing or semantic understanding
- Design puzzles that don't require specific phrases

### Problem: "Frustrating Implementation"
**Symptoms:** The game seems to fight the player rather than facilitate play.
**Solutions:**
- Prioritize player success over technical precision
- Implement graceful fallbacks for unrecognized commands
- Focus on understanding player intent rather than exact syntax

---

## Best Practices

### Command Processing
- **Understandable:** Players should know what they can try
- **Flexible:** Multiple ways to express the same intention
- **Responsive:** Even unrecognized commands get a reasonable response
- **Intuitive:** Common sense actions work naturally

### Response Generation
- **Informative:** Responses teach players about the world
- **Atmospheric:** Maintain immersion while providing information
- **Consistent:** World behaves logically at all times
- **Helpful:** Guide players toward possible solutions

### State Management
- **Logical:** World changes follow consistent rules
- **Trackable:** Important changes are easy to follow
- **Persistent:** Changes remain across sessions when appropriate
- **Recoverable:** Players can undo important mistakes

### Quality Assurance
- **Extensive Testing:** Test with players unfamiliar with the game
- **Alternative Paths:** Ensure different approaches are viable
- **Stuck Prevention:** Make sure there are no true dead ends
- **Consistency Checks:** Verify world logic across all areas

---

**Remember:** The interaction mechanics should fade into the background, letting players focus on exploring and enjoying the world. The system should feel responsive and intuitive while maintaining the illusion of a living, breathing world.