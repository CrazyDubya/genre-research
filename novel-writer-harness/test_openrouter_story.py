#!/usr/bin/env python3
"""
Test script for OpenRouter story generation.
Verifies the OpenRouter integration works correctly with the LLM service.
"""
import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.llm_service import LLMService, LLMConfig, LLMProvider


async def test_story_generation():
    """Test story generation using OpenRouter."""

    # Check for API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY environment variable not set")
        return False

    print("=" * 60)
    print("OpenRouter Story Generation Test")
    print("=" * 60)

    # Configure OpenRouter
    config = LLMConfig(
        provider=LLMProvider.OPENROUTER,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        model="anthropic/claude-3.5-sonnet",  # Using a reliable model
        temperature=0.7,
        max_tokens=1024,
    )

    print(f"\nProvider: {config.provider.value}")
    print(f"Model: {config.model}")
    print(f"Base URL: {config.base_url}")

    # Create service
    service = LLMService(config)

    # Test 1: Simple story continuation
    print("\n" + "-" * 60)
    print("Test 1: Story Continuation")
    print("-" * 60)

    story_beginning = """
    The old lighthouse keeper watched the storm approach from the rocky shore.
    After forty years of tending the light, he knew this one was different.
    The clouds moved against the wind, and the sea had turned an unnatural shade of green.
    """

    context = """
    Genre: Mystery/Horror
    Setting: Remote New England coastal town, 1923
    Main character: Thomas Harrow, 67, lighthouse keeper who has seen strange things
    Tone: Atmospheric, slow-building dread
    """

    print("\nStory beginning:")
    print(story_beginning.strip())
    print("\nGenerating continuation...")

    try:
        response = await service.continue_writing(
            current_text=story_beginning,
            context=context,
            instructions="Continue with an eerie discovery that hints at something supernatural",
            word_count=200,
        )

        if response.success:
            print("\n✓ SUCCESS!")
            print(f"\nModel used: {response.model}")
            print(f"Tokens: {response.usage}")
            print("\nGenerated text:")
            print("-" * 40)
            print(response.content)
            print("-" * 40)
        else:
            print(f"\n✗ FAILED: {response.error}")
            return False

    except Exception as e:
        print(f"\n✗ EXCEPTION: {e}")
        return False

    # Test 2: Generate story options
    print("\n" + "-" * 60)
    print("Test 2: Story Options (Branching)")
    print("-" * 60)

    print("\nGenerating 3 options for continuing the story...")

    try:
        response = await service.suggest_options(
            current_text=story_beginning,
            context=context,
            num_options=3,
        )

        if response.success:
            print("\n✓ SUCCESS!")
            print(f"\nModel used: {response.model}")
            print("\nGenerated options:")
            print("-" * 40)
            print(response.content[:1500] + "..." if len(response.content) > 1500 else response.content)
            print("-" * 40)
        else:
            print(f"\n✗ FAILED: {response.error}")
            return False

    except Exception as e:
        print(f"\n✗ EXCEPTION: {e}")
        return False

    # Test 3: Streaming test
    print("\n" + "-" * 60)
    print("Test 3: Streaming Response")
    print("-" * 60)

    print("\nStreaming a short story paragraph...")
    print("-" * 40)

    try:
        full_text = await service.stream_content(
            system_prompt="You are a novelist. Write a single atmospheric paragraph.",
            user_prompt="Write a paragraph about a mysterious door appearing in an ordinary place.",
            context="",
            on_token=lambda t: print(t, end="", flush=True),
        )
        print("\n" + "-" * 40)
        print(f"\n✓ SUCCESS! Streamed {len(full_text)} characters")

    except Exception as e:
        print(f"\n✗ EXCEPTION: {e}")
        return False

    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = asyncio.run(test_story_generation())
    sys.exit(0 if success else 1)
