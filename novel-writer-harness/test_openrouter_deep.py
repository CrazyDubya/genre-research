#!/usr/bin/env python3
"""
Deep test for OpenRouter story generation.
Tests all LLM service capabilities with a complex multi-chapter story scenario.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.llm_service import LLMService, LLMConfig, LLMProvider


# Rich story context for testing
STORY_BIBLE = """
=== THE OBSIDIAN CHRONICLES ===

GENRE: Dark Fantasy / Mystery

SETTING: The city of Verath, a crumbling metropolis built atop the ruins of an
ancient civilization. The year is 847 of the Shattered Age. Magic exists but is
dying - fewer people are born with the gift each generation. The aristocracy
hoards what magical artifacts remain.

MAIN CHARACTERS:

1. SERA VANCE (protagonist)
   - Age: 32, former detective of the City Watch, now disgraced
   - Appearance: Sharp features, prematurely grey streak in black hair, old burn
     scar on left forearm
   - Personality: Cynical but secretly idealistic, refuses to let go of cases,
     drinks too much whiskey
   - Secret: She can see the threads of fate connecting people - a dying gift
     she hides from everyone
   - Speech pattern: Clipped, economical with words, dark humor

2. MARCELLUS THORNE
   - Age: 58, wealthy collector of magical antiquities
   - Appearance: Elegant, silver hair, always impeccably dressed, walks with
     an ivory cane
   - Personality: Charming but calculating, every action serves a purpose
   - Secret: Dying of a wasting disease, desperately seeking a cure
   - Speech pattern: Formal, educated, never uses contractions

3. KAI (they/them)
   - Age: 19, street thief turned reluctant informant
   - Appearance: Slight build, quick eyes, constantly fidgeting, mismatched
     clothing
   - Personality: Distrustful, fiercely loyal once earned, survivor's instinct
   - Secret: Has a younger sibling hidden in the Undercity they're protecting
   - Speech pattern: Street slang, deflects with jokes, rarely gives straight answers

PLOT THREADS:
- A series of murders where victims are found aged decades overnight
- An artifact called "The Obsidian Heart" that may hold the key
- Corruption in the City Watch that led to Sera's disgrace
- The dying magic of the world and those who would exploit its end

TONE: Noir-influenced, morally grey, atmospheric, character-driven
"""

CHAPTER_ONE_EXCERPT = """
The rain in Verath never fell clean. It picked up the soot from the foundries,
the desperation from the slums, and something else—something that made it taste
like copper and old regrets. Sera stood under the awning of what used to be her
office, watching the grey water pool in the cobblestones.

Three weeks since they'd taken her badge. Three weeks of nothing but cheap
whiskey and cheaper cases—finding runaway wives, tracking down debts that would
never be paid. But this morning's letter had changed things.

*Come to the Thorne Estate. Midnight. I know what you can see.*

No signature. Just those words in elegant script that probably cost more than
her rent. She should have burned it. Instead, she'd spent the day preparing.

The Thorne Estate loomed at the top of the Gilt District like a tombstone for
old money. Sera adjusted the knife in her boot and the flask in her pocket, then
started walking. The threads of fate she tried so hard to ignore were pulling
tight tonight, converging on that house like streams feeding a dark river.
"""


async def deep_test():
    """Run comprehensive story generation tests."""

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set")
        return False

    config = LLMConfig(
        provider=LLMProvider.OPENROUTER,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        model="anthropic/claude-3.5-sonnet",
        temperature=0.7,
        max_tokens=2048,
    )

    service = LLMService(config)

    print("=" * 70)
    print("DEEP OPENROUTER STORY GENERATION TEST")
    print("=" * 70)
    print(f"\nModel: {config.model}")
    print(f"Max tokens: {config.max_tokens}")

    tests_passed = 0
    tests_total = 6

    # =========================================================================
    # TEST 1: Extended Story Continuation with Complex Context
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 1: Extended Story Continuation (500+ words)")
    print("=" * 70)

    try:
        response = await service.continue_writing(
            current_text=CHAPTER_ONE_EXCERPT,
            context=STORY_BIBLE,
            instructions="""Continue with Sera arriving at the Thorne Estate and meeting
            Marcellus for the first time. Show tension, atmosphere, and hint at both
            characters' secrets. Include sensory details and Sera's internal observations
            about the threads of fate she sees.""",
            word_count=500,
        )

        if response.success:
            word_count = len(response.content.split())
            print(f"\n✓ SUCCESS - Generated {word_count} words")
            print(f"Tokens: {response.usage}")
            print("\n--- Generated Content ---")
            print(response.content)
            print("--- End ---")
            tests_passed += 1
        else:
            print(f"\n✗ FAILED: {response.error}")
    except Exception as e:
        print(f"\n✗ EXCEPTION: {e}")

    # =========================================================================
    # TEST 2: Character Dialogue Generation
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 2: Character Dialogue (Sera, Marcellus, and Kai)")
    print("=" * 70)

    try:
        response = await service.generate_dialogue(
            characters=["Sera Vance", "Marcellus Thorne", "Kai"],
            situation="""Sera has brought Kai to the Thorne Estate to identify a stolen
            artifact. Kai is nervous around wealth and authority. Marcellus is suspicious
            of the street thief but needs their knowledge. Tension is high as they examine
            the Obsidian Heart together.""",
            context=STORY_BIBLE,
            character_details="""
            - Sera: Protective of Kai, wary of Marcellus's motives
            - Marcellus: Desperate but hiding it, condescending toward Kai
            - Kai: Using humor to mask fear, sees something about the artifact others don't
            """,
        )

        if response.success:
            print(f"\n✓ SUCCESS")
            print(f"Tokens: {response.usage}")
            print("\n--- Generated Dialogue ---")
            print(response.content)
            print("--- End ---")
            tests_passed += 1
        else:
            print(f"\n✗ FAILED: {response.error}")
    except Exception as e:
        print(f"\n✗ EXCEPTION: {e}")

    # =========================================================================
    # TEST 3: Passage Expansion with Sensory Details
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 3: Passage Expansion (Sensory Details)")
    print("=" * 70)

    sparse_passage = """
    Sera entered the Thorne library. It was large and old. Books lined the walls.
    Marcellus sat by the fire. He looked at her and smiled.
    """

    try:
        response = await service.expand_passage(
            passage=sparse_passage,
            context=STORY_BIBLE,
            focus="sensory details, atmosphere, and character observation",
        )

        if response.success:
            print(f"\n✓ SUCCESS")
            print(f"Tokens: {response.usage}")
            print("\nOriginal (sparse):")
            print(sparse_passage.strip())
            print("\n--- Expanded Version ---")
            print(response.content)
            print("--- End ---")
            tests_passed += 1
        else:
            print(f"\n✗ FAILED: {response.error}")
    except Exception as e:
        print(f"\n✗ EXCEPTION: {e}")

    # =========================================================================
    # TEST 4: Passage Rewrite for Style
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 4: Passage Rewrite (Noir Style Enhancement)")
    print("=" * 70)

    flat_passage = """
    Kai told Sera about the murders. There had been five victims so far. They
    were all found old, even though they had been young. The Watch wasn't
    investigating properly. Someone was covering it up. Kai seemed scared.
    """

    try:
        response = await service.rewrite_passage(
            passage=flat_passage,
            context=STORY_BIBLE,
            instructions="""Rewrite in noir style matching the story's tone. Add
            atmospheric description, character voice, and tension. Make Kai's street
            dialect authentic and Sera's observations sharp.""",
        )

        if response.success:
            print(f"\n✓ SUCCESS")
            print(f"Tokens: {response.usage}")
            print("\nOriginal (flat):")
            print(flat_passage.strip())
            print("\n--- Rewritten Version ---")
            print(response.content)
            print("--- End ---")
            tests_passed += 1
        else:
            print(f"\n✗ FAILED: {response.error}")
    except Exception as e:
        print(f"\n✗ EXCEPTION: {e}")

    # =========================================================================
    # TEST 5: Text Analysis and Editorial Feedback
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 5: Editorial Analysis")
    print("=" * 70)

    sample_chapter = """
    Sera pushed open the door to the abandoned warehouse. The Obsidian Heart was
    supposed to be here, hidden by whoever had killed Marcus Thorne three nights ago.

    "You sure about this?" Kai whispered from behind her.

    "No," Sera admitted. The threads were tangled here, knotted in ways she'd never
    seen. Death and desperation and something older, something that made her gift
    recoil. "Stay close."

    The warehouse had been a textile mill once. Now it was just shadows and decay.
    Their footsteps echoed on the warped floorboards. Sera counted the exits—two
    visible, probably a third through the loading bay.

    "There." Kai pointed toward the far corner where a faint light pulsed. "That's
    not natural light. That's—"

    "Magic," Sera finished. "The dying kind."

    They approached slowly. The light came from beneath a tarp, casting strange
    shadows that seemed to move against the laws of physics. Sera pulled back the
    covering and froze.

    It wasn't the Obsidian Heart. It was a body. Young, maybe twenty. But the face
    was ancient, withered, mouth open in a silent scream. And clutched in those
    aged hands was a fragment of black crystal, still pulsing with stolen life.

    "Oh gods," Kai breathed. "That's—that's Petra. She was at the Crossed Keys
    just yesterday. She was fine. She was laughing."

    Sera knelt beside the body, careful not to touch the crystal. The threads here
    were screaming. She could see them now, could see how they'd been ripped away,
    consumed. This wasn't just murder. It was something far worse.

    "Someone's using these people as fuel," she said quietly. "Burning their years
    to power something."

    "The Heart?"

    "Or something bigger." Sera stood, her mind racing. Six victims now, if you
    counted poor Petra. Six lives drained to nothing. For what? What could possibly
    be worth this?

    The answer came to her with terrible clarity: immortality. Someone was trying
    to live forever, and they didn't care how many had to die to make it happen.
    """

    try:
        response = await service.analyze_text(
            text=sample_chapter,
            focus_areas=["pacing", "dialogue authenticity", "mystery tension", "character voice"],
        )

        if response.success:
            print(f"\n✓ SUCCESS")
            print(f"Tokens: {response.usage}")
            print("\n--- Editorial Analysis ---")
            print(response.content)
            print("--- End ---")
            tests_passed += 1
        else:
            print(f"\n✗ FAILED: {response.error}")
    except Exception as e:
        print(f"\n✗ EXCEPTION: {e}")

    # =========================================================================
    # TEST 6: Brainstorming Plot Developments
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST 6: Plot Brainstorming")
    print("=" * 70)

    try:
        response = await service.brainstorm_ideas(
            topic="""Twist revelations for the identity of the killer using the
            Obsidian Heart. The reveal should connect to Sera's past, explain why
            magic is dying, and force Sera into an impossible moral choice.""",
            context=STORY_BIBLE + "\n\nCurrent plot: Six victims drained of their "
            "life force. The Obsidian Heart artifact is central. Marcellus Thorne's "
            "brother Marcus was the latest victim.",
            num_ideas=5,
        )

        if response.success:
            print(f"\n✓ SUCCESS")
            print(f"Tokens: {response.usage}")
            print("\n--- Brainstormed Ideas ---")
            print(response.content)
            print("--- End ---")
            tests_passed += 1
        else:
            print(f"\n✗ FAILED: {response.error}")
    except Exception as e:
        print(f"\n✗ EXCEPTION: {e}")

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 70)
    print(f"RESULTS: {tests_passed}/{tests_total} tests passed")
    print("=" * 70)

    if tests_passed == tests_total:
        print("\n✓ ALL TESTS PASSED - OpenRouter integration fully verified!")
    else:
        print(f"\n⚠ {tests_total - tests_passed} test(s) failed")

    return tests_passed == tests_total


if __name__ == "__main__":
    success = asyncio.run(deep_test())
    sys.exit(0 if success else 1)
