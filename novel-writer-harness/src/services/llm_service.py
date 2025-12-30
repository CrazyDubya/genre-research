"""
LLM Service for novel writing assistance.

Provides a unified interface to different LLM providers:
- Anthropic Claude
- OpenAI GPT
- Local models via Ollama
- Custom API endpoints
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import AsyncIterator, Optional, Callable
import os
import json


class LLMProvider(Enum):
    """Supported LLM providers."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    OPENROUTER = "openrouter"
    OLLAMA = "ollama"
    CUSTOM = "custom"


@dataclass
class LLMConfig:
    """Configuration for LLM connection."""
    provider: LLMProvider = LLMProvider.ANTHROPIC
    model: str = "claude-sonnet-4-20250514"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 120

    @classmethod
    def from_env(cls, provider: LLMProvider = LLMProvider.ANTHROPIC) -> "LLMConfig":
        """Create config from environment variables."""
        config = cls(provider=provider)

        if provider == LLMProvider.ANTHROPIC:
            config.api_key = os.getenv("ANTHROPIC_API_KEY")
            config.model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        elif provider == LLMProvider.OPENAI:
            config.api_key = os.getenv("OPENAI_API_KEY")
            config.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        elif provider == LLMProvider.OPENROUTER:
            config.api_key = os.getenv("OPENROUTER_API_KEY")
            config.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
            config.model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-sonnet-4")
        elif provider == LLMProvider.OLLAMA:
            config.base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            config.model = os.getenv("OLLAMA_MODEL", "llama3.2")

        return config


@dataclass
class LLMResponse:
    """Response from LLM."""
    content: str
    model: str
    usage: dict = None
    finish_reason: str = ""
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.error is None and self.content


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""

    def __init__(self, config: LLMConfig):
        self.config = config

    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = "",
    ) -> LLMResponse:
        """Generate a completion."""
        pass

    @abstractmethod
    async def stream(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = "",
    ) -> AsyncIterator[str]:
        """Stream a completion."""
        pass


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude client."""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.client = None

    def _ensure_client(self):
        """Lazy initialization of client."""
        if self.client is None:
            try:
                from anthropic import AsyncAnthropic
                self.client = AsyncAnthropic(api_key=self.config.api_key)
            except ImportError:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = "",
    ) -> LLMResponse:
        """Generate a completion using Claude."""
        self._ensure_client()

        # Build messages
        messages = []
        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}"})
            messages.append({"role": "assistant", "content": "I understand the context. How can I help?"})

        messages.append({"role": "user", "content": user_prompt})

        try:
            response = await self.client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                system=system_prompt,
                messages=messages,
                temperature=self.config.temperature,
            )

            return LLMResponse(
                content=response.content[0].text,
                model=response.model,
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                },
                finish_reason=response.stop_reason,
            )
        except Exception as e:
            return LLMResponse(
                content="",
                model=self.config.model,
                error=str(e),
            )

    async def stream(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = "",
    ) -> AsyncIterator[str]:
        """Stream a completion using Claude."""
        self._ensure_client()

        messages = []
        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}"})
            messages.append({"role": "assistant", "content": "I understand the context. How can I help?"})

        messages.append({"role": "user", "content": user_prompt})

        try:
            async with self.client.messages.stream(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                system=system_prompt,
                messages=messages,
                temperature=self.config.temperature,
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception as e:
            yield f"[Error: {str(e)}]"


class OpenAIClient(BaseLLMClient):
    """OpenAI GPT client."""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.client = None

    def _ensure_client(self):
        """Lazy initialization of client."""
        if self.client is None:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=self.config.api_key)
            except ImportError:
                raise ImportError("openai package not installed. Run: pip install openai")

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = "",
    ) -> LLMResponse:
        """Generate a completion using GPT."""
        self._ensure_client()

        messages = [{"role": "system", "content": system_prompt}]

        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}"})
            messages.append({"role": "assistant", "content": "I understand the context. How can I help?"})

        messages.append({"role": "user", "content": user_prompt})

        try:
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )

            choice = response.choices[0]
            return LLMResponse(
                content=choice.message.content,
                model=response.model,
                usage={
                    "input_tokens": response.usage.prompt_tokens,
                    "output_tokens": response.usage.completion_tokens,
                },
                finish_reason=choice.finish_reason,
            )
        except Exception as e:
            return LLMResponse(
                content="",
                model=self.config.model,
                error=str(e),
            )

    async def stream(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = "",
    ) -> AsyncIterator[str]:
        """Stream a completion using GPT."""
        self._ensure_client()

        messages = [{"role": "system", "content": system_prompt}]

        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}"})
            messages.append({"role": "assistant", "content": "I understand the context. How can I help?"})

        messages.append({"role": "user", "content": user_prompt})

        try:
            stream = await self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                stream=True,
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"[Error: {str(e)}]"


class OpenRouterClient(BaseLLMClient):
    """
    OpenRouter client - unified access to multiple LLM providers.

    OpenRouter provides a single API endpoint to access models from:
    - Anthropic (Claude)
    - OpenAI (GPT-4, GPT-4o)
    - Meta (Llama)
    - Mistral
    - Google (Gemini)
    - And many more

    Uses OpenAI-compatible API format with additional headers.
    """

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.client = None
        self.base_url = config.base_url or "https://openrouter.ai/api/v1"

    def _ensure_client(self):
        """Lazy initialization of client."""
        if self.client is None:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(
                    api_key=self.config.api_key,
                    base_url=self.base_url,
                    default_headers={
                        "HTTP-Referer": "https://github.com/genre-research/novel-writer-harness",
                        "X-Title": "Novel Writer Harness",
                    },
                )
            except ImportError:
                raise ImportError("openai package not installed. Run: pip install openai")

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = "",
    ) -> LLMResponse:
        """Generate a completion using OpenRouter."""
        self._ensure_client()

        messages = [{"role": "system", "content": system_prompt}]

        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}"})
            messages.append({"role": "assistant", "content": "I understand the context. How can I help?"})

        messages.append({"role": "user", "content": user_prompt})

        try:
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )

            choice = response.choices[0]
            return LLMResponse(
                content=choice.message.content,
                model=response.model,
                usage={
                    "input_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "output_tokens": response.usage.completion_tokens if response.usage else 0,
                },
                finish_reason=choice.finish_reason,
            )
        except Exception as e:
            return LLMResponse(
                content="",
                model=self.config.model,
                error=str(e),
            )

    async def stream(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = "",
    ) -> AsyncIterator[str]:
        """Stream a completion using OpenRouter."""
        self._ensure_client()

        messages = [{"role": "system", "content": system_prompt}]

        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}"})
            messages.append({"role": "assistant", "content": "I understand the context. How can I help?"})

        messages.append({"role": "user", "content": user_prompt})

        try:
            stream = await self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                stream=True,
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"[Error: {str(e)}]"

    def get_available_models(self) -> list[str]:
        """Return commonly used OpenRouter model identifiers."""
        return [
            # Anthropic
            "anthropic/claude-sonnet-4",
            "anthropic/claude-opus-4",
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-3-opus",
            # OpenAI
            "openai/gpt-4o",
            "openai/gpt-4-turbo",
            "openai/o1-preview",
            # Meta
            "meta-llama/llama-3.1-405b-instruct",
            "meta-llama/llama-3.1-70b-instruct",
            # Mistral
            "mistralai/mistral-large",
            "mistralai/mixtral-8x22b-instruct",
            # Google
            "google/gemini-pro-1.5",
            # DeepSeek
            "deepseek/deepseek-chat",
        ]


class OllamaClient(BaseLLMClient):
    """Ollama local model client."""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.base_url = config.base_url or "http://localhost:11434"

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = "",
    ) -> LLMResponse:
        """Generate a completion using Ollama."""
        try:
            import httpx
        except ImportError:
            raise ImportError("httpx package not installed. Run: pip install httpx")

        prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser: {user_prompt}"

        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.config.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": self.config.temperature,
                            "num_predict": self.config.max_tokens,
                        },
                    },
                )
                response.raise_for_status()
                data = response.json()

                return LLMResponse(
                    content=data.get("response", ""),
                    model=self.config.model,
                    usage={
                        "input_tokens": data.get("prompt_eval_count", 0),
                        "output_tokens": data.get("eval_count", 0),
                    },
                    finish_reason="stop" if data.get("done") else "incomplete",
                )
            except Exception as e:
                return LLMResponse(
                    content="",
                    model=self.config.model,
                    error=str(e),
                )

    async def stream(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = "",
    ) -> AsyncIterator[str]:
        """Stream a completion using Ollama."""
        try:
            import httpx
        except ImportError:
            raise ImportError("httpx package not installed. Run: pip install httpx")

        prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser: {user_prompt}"

        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.config.model,
                        "prompt": prompt,
                        "stream": True,
                        "options": {
                            "temperature": self.config.temperature,
                            "num_predict": self.config.max_tokens,
                        },
                    },
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            data = json.loads(line)
                            if "response" in data:
                                yield data["response"]
            except Exception as e:
                yield f"[Error: {str(e)}]"


class LLMService:
    """
    High-level LLM service for novel writing.

    Provides writing-specific methods that use the appropriate LLM client.
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig.from_env()
        self.client = self._create_client()

    def _create_client(self) -> BaseLLMClient:
        """Create the appropriate client based on provider."""
        clients = {
            LLMProvider.ANTHROPIC: AnthropicClient,
            LLMProvider.OPENAI: OpenAIClient,
            LLMProvider.OPENROUTER: OpenRouterClient,
            LLMProvider.OLLAMA: OllamaClient,
        }

        client_class = clients.get(self.config.provider, AnthropicClient)
        return client_class(self.config)

    def update_config(self, config: LLMConfig) -> None:
        """Update configuration and recreate client."""
        self.config = config
        self.client = self._create_client()

    async def generate_content(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = "",
    ) -> LLMResponse:
        """Generate content with the configured LLM."""
        return await self.client.generate(system_prompt, user_prompt, context)

    async def stream_content(
        self,
        system_prompt: str,
        user_prompt: str,
        context: str = "",
        on_token: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Stream content and optionally call callback on each token."""
        full_response = []

        async for token in self.client.stream(system_prompt, user_prompt, context):
            full_response.append(token)
            if on_token:
                on_token(token)

        return "".join(full_response)

    async def continue_writing(
        self,
        current_text: str,
        context: str,
        instructions: str = "",
        word_count: int = 500,
    ) -> LLMResponse:
        """Continue writing from current point."""
        system_prompt = """You are a skilled novelist. Continue the story naturally,
matching the tone, style, and pacing of the existing text. Write approximately
{} words. Maintain character voices and advance the narrative meaningfully.""".format(word_count)

        user_prompt = f"Continue from here:\n\n{current_text[-2000:]}"  # Last 2000 chars
        if instructions:
            user_prompt += f"\n\nInstructions: {instructions}"

        return await self.client.generate(system_prompt, user_prompt, context)

    async def suggest_options(
        self,
        current_text: str,
        context: str,
        num_options: int = 3,
    ) -> LLMResponse:
        """Generate multiple options for continuing the story."""
        system_prompt = f"""You are a skilled novelist. Provide {num_options} distinct options
for continuing the story. Each option should take the narrative in a different direction.
Format each option clearly with a header and brief summary before the prose."""

        user_prompt = f"Current text:\n\n{current_text[-1500:]}\n\nProvide {num_options} different ways to continue."

        return await self.client.generate(system_prompt, user_prompt, context)

    async def rewrite_passage(
        self,
        passage: str,
        context: str,
        instructions: str = "",
    ) -> LLMResponse:
        """Rewrite a passage with improvements."""
        system_prompt = """You are a skilled editor. Rewrite the given passage to improve it.
Maintain the core meaning and story beats but enhance the prose quality.
Focus on: vivid language, stronger verbs, better flow, and emotional impact."""

        user_prompt = f"Rewrite this passage:\n\n{passage}"
        if instructions:
            user_prompt += f"\n\nSpecific focus: {instructions}"

        return await self.client.generate(system_prompt, user_prompt, context)

    async def generate_dialogue(
        self,
        characters: list[str],
        situation: str,
        context: str,
        character_details: str = "",
    ) -> LLMResponse:
        """Generate dialogue for characters."""
        system_prompt = """You are a skilled dialogue writer. Create natural, character-specific
dialogue that reveals personality, advances plot, and sounds authentic.
Each character should have a distinct voice."""

        user_prompt = f"""Write dialogue for: {', '.join(characters)}
Situation: {situation}

Character details:
{character_details}"""

        return await self.client.generate(system_prompt, user_prompt, context)

    async def expand_passage(
        self,
        passage: str,
        context: str,
        focus: str = "sensory details",
    ) -> LLMResponse:
        """Expand a passage with more detail."""
        system_prompt = f"""You are a skilled novelist. Expand the given passage with more
{focus}. Add depth and richness while maintaining the narrative flow.
The expansion should feel natural, not forced."""

        user_prompt = f"Expand this passage:\n\n{passage}"

        return await self.client.generate(system_prompt, user_prompt, context)

    async def analyze_text(
        self,
        text: str,
        focus_areas: list[str] = None,
    ) -> LLMResponse:
        """Analyze text for potential improvements."""
        focus = focus_areas or ["pacing", "character voice", "description", "dialogue"]
        system_prompt = f"""You are an experienced editor. Analyze the given text focusing on:
{', '.join(focus)}

Provide specific, actionable feedback with examples from the text."""

        user_prompt = f"Analyze this text:\n\n{text}"

        return await self.client.generate(system_prompt, user_prompt, "")

    async def brainstorm_ideas(
        self,
        topic: str,
        context: str,
        num_ideas: int = 5,
    ) -> LLMResponse:
        """Brainstorm creative ideas for the story."""
        system_prompt = f"""You are a creative consultant for novelists. Generate {num_ideas}
creative, surprising, and narratively interesting ideas for the given topic.
Consider the established story context. Ideas should be specific and actionable."""

        user_prompt = f"Brainstorm ideas for: {topic}"

        return await self.client.generate(system_prompt, user_prompt, context)
