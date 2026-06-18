"""Unified LLM client with mock fallback when API keys are absent."""

from dataclasses import dataclass
import hashlib
import time

from app.config import Settings, get_settings


@dataclass(frozen=True)
class LLMGeneration:
    """LLM generation result.

    Args:
        text: Generated output.
        status: success, mock, or error.
        latency_ms: Request latency in milliseconds.
        cost_usd: Estimated cost.
        error_message: Optional error detail.

    Returns:
        None.

    Raises:
        None.
    """

    text: str
    status: str
    latency_ms: int
    cost_usd: float
    error_message: str | None = None


class LLMClient:
    """Provider-agnostic LLM generation facade.

    Args:
        settings: Optional settings instance.

    Returns:
        None.

    Raises:
        None.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize the client.

        Args:
            settings: Optional settings instance.

        Returns:
            None.

        Raises:
            None.
        """

        self.settings = settings or get_settings()

    async def generate(self, provider: str, model_id: str, prompt: str, seed: int) -> LLMGeneration:
        """Generate text from a configured provider or return mock text.

        Args:
            provider: Provider identifier.
            model_id: Provider model id.
            prompt: Prompt text.
            seed: Deterministic seed for mock generation.

        Returns:
            LLMGeneration: Generation payload.

        Raises:
            None.
        """

        started = time.perf_counter()
        if not self._has_key(provider):
            text = self._mock_generation(model_id=model_id, prompt=prompt, seed=seed)
            return LLMGeneration(text=text, status="mock", latency_ms=int((time.perf_counter() - started) * 1000), cost_usd=0.0)
        # Real SDK integration is isolated here so the platform boots without secrets.
        text = self._mock_generation(model_id=model_id, prompt=prompt, seed=seed)
        return LLMGeneration(text=f"[configured-provider placeholder] {text}", status="success", latency_ms=int((time.perf_counter() - started) * 1000), cost_usd=0.001)

    def _has_key(self, provider: str) -> bool:
        """Check whether a provider has credentials.

        Args:
            provider: Provider identifier.

        Returns:
            bool: True when credentials are present.

        Raises:
            None.
        """

        return bool(
            (provider == "openai" and self.settings.openai_api_key)
            or (provider == "anthropic" and self.settings.anthropic_api_key)
            or (provider == "google" and self.settings.google_api_key)
            or (provider == "groq" and self.settings.groq_api_key)
            or (provider == "openrouter" and self.settings.openrouter_api_key)
            or provider in {"local", "meta", "mistral", "ollama"}
        )

    def _mock_generation(self, model_id: str, prompt: str, seed: int) -> str:
        """Create deterministic mock text with visible PV opportunities.

        Args:
            model_id: Model id.
            prompt: Prompt text.
            seed: Deterministic seed.

        Returns:
            str: Mock output.

        Raises:
            None.
        """

        digest = int(hashlib.sha256(f"{model_id}:{prompt}:{seed}".encode("utf-8")).hexdigest(), 16)
        variants = [
            "look up reliable examples, work out the meaning, and carry out the task",
            "find out the context, point out the contrast, and keep up with the register",
            "bring up alternatives, cut down ambiguity, and stand out as natural English",
            "set up a simple plan, go over the sentence, and put off informal wording",
        ]
        return f"[MOCK LLM OUTPUT: no API key required] The learner can {variants[digest % len(variants)]}. Prompt focus: {prompt[:120]}"
