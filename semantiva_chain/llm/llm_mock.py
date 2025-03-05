"""
Mock API wrapper for Semantiva-Chain.

Handles interaction with a Mock model.
"""

from .llm_interface import LLMInterface
from semantiva.logger import Logger

from typing import Dict, Any, Optional


class MockLLM(LLMInterface):
    """
    Mock API wrapper for Semantiva-Chain.

    """

    def __init__(
        self, api_key: str, model: str = "mock_0", logger: Optional[Logger] = None
    ):
        """
        Initializes the Mock LLM instance with Mock API credentials and Mock model selection.

        Args:
            api_key (str): Mock key for authentication.
            model (str): The specific Mock model to use.
        """
        super().__init__(logger)
        self.api_key = api_key
        self.model = model
        self.logger.info(f"Initialized Mock LLM with model: {self.model}")

    def generate_response(self, prompt: str, parameters: Dict[str, Any] = None) -> str:
        """
        Generates a response using Mock API.

        Args:
            prompt (str): The input prompt for the model.
            parameters (Dict[str, Any], optional): Additional parameters like temperature and max tokens.

        Returns:
            str: The generated response from the LLM.

        Raises:
            Exception: If an error occurs while interacting with OpenAI's API.
        """
        parameters = parameters or {}
        try:
            mock_response = (
                f"Mock LLM response with parameters {parameters} to prompt:\n{prompt}"
            )
            return mock_response
        except Exception as e:
            return f"Error: {str(e)}"
