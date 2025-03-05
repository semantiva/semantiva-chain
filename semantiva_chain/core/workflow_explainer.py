"""
Generates natural language explanations for Semantiva workflows.

Extracts workflow metadata, analyzes processing steps, and formulates
human-readable descriptions of the workflow’s function and structure.
"""

import os
from typing import List, Dict, Any, Optional
from semantiva.logger import Logger
from semantiva_chain.core.component_metadata_extractor import ComponentMetadataExtractor
from semantiva_chain.llm.llm_factory import LLMFactory
from pprint import pformat


class WorkflowExplainer:
    """
    Provides workflow analysis and explanations.

    This class extracts metadata from Semantiva pipeline configurations and
    generates natural language explanations using an LLM.

    Methods:
        explain(node_configurations: list) -> str:
            Generates a human-readable explanation of the specified workflow.
    """

    def __init__(self, logger: Optional[Logger] = None):
        """
        Initializes the WorkflowExplainer with an LLM instance.

        The LLM provider is determined dynamically from environment variables.
        """
        self.logger = logger if logger else Logger()

        llm_provider = os.getenv("LLM_PROVIDER", "openai")
        self.logger.info(
            f"Initializing WorkflowExplainer with LLM provider: {llm_provider}"
        )
        self.llm = LLMFactory.get_llm(
            provider=llm_provider,
            api_key=os.getenv("LLM_API_KEY"),
            model=os.getenv("LLM_MODEL"),
        )

    def explain(self, node_configurations: List[Dict[str, Any]]) -> str:
        """
        Generates a human-readable explanation for a given pipeline configuration.

        Args:
            node_configurations (list): List of pipeline node configurations.

        Returns:
            str: Natural language explanation of the workflow.
        """
        if not node_configurations:
            return "The provided workflow configuration is empty."

        components = []
        for node in node_configurations:
            processor_name = node.get("processor")
            if not processor_name:
                return f"Error: Missing 'processor' key in node configuration: {node}"

            metadata = ComponentMetadataExtractor.get_metadata(processor_name)
            if "error" in metadata:
                return f"Error: {metadata['error']}"

            components.append(metadata)

        self.logger.info(
            "Extracted metadata for components:\n%s",
            pformat(components, indent=2, width=100),
        )
        prompt = self._generate_prompt(node_configurations, components)
        return self.llm.generate_response(prompt)

    def _generate_prompt(
        self,
        node_configurations: List[Dict[str, Any]],
        components: List[Dict[str, Any]],
    ) -> str:
        """
        Generates an LLM prompt incorporating full pipeline configuration and metadata.

        Args:
            node_configurations (list): The original pipeline structure.
            components (list): Extracted metadata for components in the workflow.

        Returns:
            str: A structured prompt for the LLM.
        """
        # Convert full pipeline configuration to a structured format
        pipeline_structure = "\n".join(
            [
                (
                    f"- Step {idx + 1}: {node.get('processor')}\n"
                    f"  Context Keyword: {node.get('context_keyword', 'None')}\n"
                    "  Parameters:\n"
                    + "\n".join(
                        [
                            f"    - {key}: {value}"
                            for key, value in (node.get("parameters") or {}).items()
                        ]
                    )
                )
                for idx, node in enumerate(node_configurations)
                if isinstance(node.get("parameters"), dict)
                or node.get("parameters") is None
            ]
        )

        # Convert extracted metadata into structured descriptions
        component_descriptions = "\n".join(
            [
                f"- {comp['component_name']}:\n"
                f"  Description: {comp.get('docstring', 'No description available.')}\n"
                f"  Module: {comp.get('module_path', 'Unknown')}\n"
                f"  Class Hierarchy: {', '.join(map(str, comp.get('class_hierarchy', [])))}\n"
                f"  Interfaces:\n"
                + "\n".join(
                    [
                        f"    - {iface['interface_type']}: {iface['data_type']}"
                        for iface in comp.get("interfaces", [])
                        if isinstance(iface, dict)
                        and "interface_type" in iface
                        and "data_type" in iface
                    ]
                )
                + f"\n  Processing Logic:\n"
                + "\n".join(
                    [
                        f"    - {param['name']}: {param['type']}"
                        for param in comp.get("processing_logic", {}).get(
                            "parameters", []
                        )
                        if isinstance(param, dict)
                        and "name" in param
                        and "type" in param
                    ]
                )
                for comp in components
            ]
        )

        # Construct a smarter LLM prompt with structured pipeline and metadata
        return f"""
        You are an AI workflow assistant. Given the following pipeline configuration, 
        explain how it works in a clear and structured manner.

        **Pipeline Configuration:**
        {pipeline_structure}

        **Component Details:**
        {component_descriptions}

        Provide a detailed, structured, and human-readable explanation of the workflow.
        """
