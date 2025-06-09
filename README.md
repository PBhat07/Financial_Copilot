# LLM_script_assistant
 An LLM-powered assistant that helps film creators write character dialogues based on scene descriptions, voice tone, and even image inputs (optional). It uses RAG to pull examples from existing scripts and MCP to condition outputs.

## KelvinQiu802/llm-mcp-rag
This repository demonstrates an augmented LLM setup combining chat interfaces with MCP and RAG functionalities. It emphasizes a lightweight implementation without relying on heavy frameworks like LangChain. This can be particularly useful for understanding how to integrate RAG and MCP in a streamlined manner.

#FLASK VS GRADIO

| Feature         | **Flask**                      | **Gradio**                            |
| --------------- | ------------------------------ | ------------------------------------- |
| Setup           | Manual routing, HTML templates | Plug-and-play, no HTML needed         |
| Customizability | High (full control)            | Medium (but improving)                |
| Time to build   | Slower                         | Much faster                           |
| Ideal for       | Production-ready apps          | Prototypes, demos, portfolio projects |
| Colab support   | Not native (needs `ngrok`)     | Fully supported                       |
