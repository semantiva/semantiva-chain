"""
Extracts metadata from Semantiva components.

This module retrieves structured metadata from Semantiva-based ComputingTasks, Pipelines, 
and Processors. It provides information on:
- Class hierarchy
- Input/output types
- Context dependencies
- Processing logic parameters

This metadata enables AI-powered workflow analysis, consistency validation, and 
documentation generation.
"""

import inspect
from typing import Dict, Any, Type
from semantiva.component_loader.component_loader import ComponentLoader
from semantiva.data_types.data_types import BaseDataType


class ComponentMetadataExtractor:
    """
    Extracts metadata from Semantiva components.

    Methods:
        get_metadata(component_name: str) -> Dict[str, Any]:
            Retrieves structured metadata for the given component.

        _get_class_hierarchy(cls: Type) -> list:
            Returns the class hierarchy of the component.

        _get_interfaces(cls: Type) -> list:
            Extracts input and output data types from the component.

        _get_processing_logic(cls: Type) -> Dict[str, Any]:
            Extracts details of the processing logic, including parameters.
    """

    @staticmethod
    def get_metadata(component_name: str) -> Dict[str, Any]:
        """
        Retrieves metadata for a given Semantiva component.

        Args:
            component_name (str): The name of the component to retrieve metadata for.

        Returns:
            Dict[str, Any]: A dictionary containing the component's metadata.
        """
        component_class = ComponentLoader.get_class(component_name)

        if not component_class:
            return {"error": f"Component '{component_name}' not found."}

        return {
            "component_name": component_name,
            "module_path": component_class.__module__,
            "class_hierarchy": ComponentMetadataExtractor._get_class_hierarchy(
                component_class
            ),
            "interfaces": ComponentMetadataExtractor._get_interfaces(component_class),
            "processing_logic": ComponentMetadataExtractor._get_processing_logic(
                component_class
            ),
            "docstring": inspect.getdoc(component_class),
        }

    @staticmethod
    def _get_class_hierarchy(cls: Type) -> list:
        """
        Retrieves the class hierarchy of a component.

        Args:
            cls (Type): The component class.

        Returns:
            list: A list representing the class hierarchy.
        """
        return [
            base.__name__ for base in inspect.getmro(cls) if base.__name__ != "object"
        ]

    @staticmethod
    def _get_interfaces(cls: Type) -> list:
        """
        Extracts input and output data types from the component.

        Args:
            cls (Type): The component class.

        Returns:
            list: A list of dictionaries representing input/output types.
        """
        interfaces = []
        if hasattr(cls, "input_data_type") and callable(cls.input_data_type):
            interfaces.append(
                {"interface_type": "input", "data_type": cls.input_data_type().__name__}
            )
        if hasattr(cls, "output_data_type") and callable(cls.output_data_type):
            interfaces.append(
                {
                    "interface_type": "output",
                    "data_type": cls.output_data_type().__name__,
                }
            )
        return interfaces

    @staticmethod
    def _get_processing_logic(cls: Type) -> Dict[str, Any]:
        """
        Extracts details of the processing logic, including parameters and types.

        Args:
            cls (Type): The component class.

        Returns:
            Dict[str, Any]: Metadata about the processing logic.
        """
        if not hasattr(cls, "_process_logic"):
            return {"error": "Processing logic not defined"}

        signature = inspect.signature(cls._process_logic)
        parameters = [
            {
                "name": param.name,
                "type": (
                    param.annotation.__name__
                    if param.annotation != param.empty
                    else "Unknown"
                ),
            }
            for param in signature.parameters.values()
            if param.name != "self"
        ]

        return {
            "parameters": parameters,
            "description": inspect.getdoc(cls._process_logic),
        }
