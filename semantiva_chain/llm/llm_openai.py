"""
OpenAI API wrapper for Semantiva-Chain.

Handles interaction with OpenAI’s GPT-based models.
"""

from .llm_interface import LLMInterface


import openai
from typing import Dict, Any, Optional
from semantiva.logger import Logger


class OpenAILLM(LLMInterface):
    """
    OpenAI API wrapper for Semantiva-Chain.

    This class provides an interface to interact with OpenAI's GPT-based models
    for generating natural language explanations of workflows.

    Attributes:
        api_key (str): The API key for OpenAI authentication.
        model (str): The specific OpenAI model to use (e.g., "gpt-4", "gpt-4o-mini").

    Methods:
        generate_response(prompt: str, parameters: Dict[str, Any] = None) -> str:
            Sends a request to OpenAI's API and returns the response.
    """

    def __init__(
        self, api_key: str, model: str = "gpt-4o-mini", logger: Optional[Logger] = None
    ):
        """
        Initializes the OpenAI LLM instance with API credentials and model selection.

        Args:
            api_key (str): OpenAI API key for authentication.
            model (str): The specific GPT model to use.
        """
        super().__init__(logger)
        self.api_key = api_key
        self.model = model
        self.logger.info(f"Initialized OpenAI LLM with model: {self.model}")

    def generate_response(self, prompt: str, parameters: Dict[str, Any] = None) -> str:
        """
        Generates a response using OpenAI's GPT API.

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
            message = [
                {"role": "system", "content": "You are an AI workflow assistant."},
                {"role": "user", "content": prompt},
            ]
            self.logger.info(f"Sending prompt to OpenAI model: {prompt}")

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=message,
                api_key=self.api_key,
                temperature=parameters.get("temperature", 0.7),
                max_tokens=parameters.get("max_tokens", 1000),
            )
            self.logger.info(f"Received response from OpenAI model: {response}")
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"
