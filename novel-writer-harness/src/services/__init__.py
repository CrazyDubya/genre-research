"""
Services for the Novel Writer Harness.
"""
from .llm_service import (
    LLMService,
    LLMConfig,
    LLMProvider,
    LLMResponse,
    BaseLLMClient,
    AnthropicClient,
    OpenAIClient,
    OllamaClient,
)
from .research_service import (
    ResearchService,
    ResearchDocument,
)

__all__ = [
    # LLM Service
    "LLMService",
    "LLMConfig",
    "LLMProvider",
    "LLMResponse",
    "BaseLLMClient",
    "AnthropicClient",
    "OpenAIClient",
    "OllamaClient",
    # Research Service
    "ResearchService",
    "ResearchDocument",
]
