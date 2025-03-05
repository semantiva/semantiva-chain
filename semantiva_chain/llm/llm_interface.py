"""
Defines the LLM interface for integrating different AI models.

All LLM implementations must inherit from this interface and implement
the `generate_response` method.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from semantiva.logger import Logger


class LLMInterface(ABC):
    """
    Abstract base class for LLM integrations.

    Methods:
        generate_response(prompt: str, parameters: Dict[str, Any] = None) -> str:
            Generates a response from the LLM based on the input prompt.
    """

    def __init__(self, logger: Optional[Logger] = None):
        if logger:
            # If a logger instance is provided, use it
            self.logger = logger
        else:
            # If no logger is provided, create a new Logger instance
            self.logger = Logger()

    @abstractmethod
    def generate_response(self, prompt: str, parameters: Dict[str, Any] = None) -> str:
        """
        Generates a response from the LLM based on the input prompt.

        Args:
            prompt (str): The input prompt for the model.
            parameters (Dict[str, Any], optional): Additional parameters for the model.

        Returns:
            str: The generated response from the LLM.
        """
        pass
