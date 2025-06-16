
# FLASK VS GRADIO

| Feature         | **Flask**                      | **Gradio**                            |
| --------------- | ------------------------------ | ------------------------------------- |
| Setup           | Manual routing, HTML templates | Plug-and-play, no HTML needed         |
| Customizability | High (full control)            | Medium (but improving)                |
| Time to build   | Slower                         | Much faster                           |
| Ideal for       | Production-ready apps          | Prototypes, demos, portfolio projects |
| Colab support   | Not native (needs `ngrok`)     | Fully supported                       |




## Potential Work Flow
![image](https://github.com/user-attachments/assets/eb721809-b975-446b-bd1b-69aa6fd11a2d)
![image](https://github.com/user-attachments/assets/9499d7bd-3319-4004-8679-4b6e201c41e7)


## Install necessary libraries for RAG
<pre> ```
 print("Installing RAG pipeline libraries...")
 !pip install -qqq langchain pypdf faiss-cpu # Core LangChain, PDF loader, FAISS 
 !pip install -qqq "langchain_google_genai" "google-generativeai" # Google Gemini embeddings and LLM 
 !pip install -qqq "langchain_community" "langchain_core" # Ensure core and community packages are up to date 
 print("Libraries installed.") ``` </pre>

## Run rag_pipeline.py file
<pre>
!python rag_pipeline.py </pre>

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1GIjCBMroWHaHUpppp_-9eMNgjhQ-hjCG?usp=sharing)


