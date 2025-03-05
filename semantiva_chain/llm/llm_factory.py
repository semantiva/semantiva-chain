"""
Factory class for dynamically selecting an LLM provider.

Allows runtime injection of different LLMs.
"""

from .llm_interface import LLMInterface
from .llm_openai import OpenAILLM
from .llm_mock import MockLLM


class LLMFactory:
    """
    Factory for instantiating LLM providers dynamically.

    This class allows selection of different LLM models at runtime based on
    the provider name and API credentials.

    Methods:
        get_llm(provider: str, api_key: str, model: str = None) -> LLMInterface:
            Returns an LLM instance based on the selected provider.
    """

    @staticmethod
    def get_llm(provider: str, api_key: str, model: str = None) -> LLMInterface:
        """
        Returns an LLM instance based on the provider.

        Args:
            provider (str): The LLM provider ("openai" or "deepseek").
            api_key (str): The API key for authentication.
            model (str, optional): The model to use (default models are used if None).

        Returns:
            LLMInterface: An instance of the selected LLM class.

        Raises:
            ValueError: If an unsupported provider is specified.
        """
        provider = provider.lower()

        if provider == "openai":
            return OpenAILLM(api_key, model or "gpt-4o-mini")
        elif provider == "mock":
            return MockLLM(api_key, model or "mock")
        else:
            raise ValueError(
                f"Unsupported LLM provider: '{provider}'. Choose 'openai' or 'mock'."
            )
