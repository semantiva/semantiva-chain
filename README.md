# Semantiva-Chain 
**AI-Powered Workflow Analysis & Documentation for Semantiva**  

## Overview 
Semantiva-Chain is an **AI-driven workflow analysis tool** designed to provide **natural language explanations, consistency validation, and automatic documentation** for workflows built with the **Semantiva framework**.  

This tool is **LLM-agnostic**, allowing users to integrate different AI models (OpenAI, DeepSeek, etc.) for **workflow understanding and validation** without modifying core logic.

---

## Key Features 

### Workflow Explanation Engine 
- Extracts **structured metadata** from Semantiva workflows.  
- Generates **human-readable explanations** of workflow logic and dependencies.  

### Component Metadata Extraction 
- Retrieves detailed metadata for **Semantiva ComputingTasks, Pipelines, and Processors**.  
- Extracts **class hierarchy, input/output types, processing logic, and dependencies**.  
- Enables **deep insights** into individual workflow components.  

### Automatic Workflow Documentation 
- Generates **Markdown, JSON, and PDF reports** summarizing workflow structure and validation results.  
- Provides **clear, structured documentation** for auditing and reference.  
- Supports **easy export and sharing**.  

### LLM-Agnostic AI Integration 
- Uses an **LLM abstraction layer**, allowing flexible AI model selection.  
- Allows **runtime configuration of LLM provider** without modifying core code.  

---

## Installation 

### Clone the Repository 
```bash
git clone https://github.com/semantiva/semantiva-chain.git
cd semantiva-chain
```

### Configure API Key for LLM Provider 
Set the preferred LLM provider (`openai` or `deepseek`) and provide the API key: (only `openai` is supported for now)
For OpenAI:
```bash
export LLM_PROVIDER="openai" # or `mock` for testing
export LLM_MODEL="gpt-3.5-turbo"
export LLM_API_KEY="your_openai_api_key"
```

### Execute the pipeline explainer demo**
```bash
python tests/pipeline_explainer_demo.py
```

---

## License
Semantiva-Chain is released under the **MIT License**.  
