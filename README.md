# LLM_script_assistant
 An LLM-powered assistant that helps film creators write character dialogues based on scene descriptions, voice tone, and even image inputs (optional). It uses RAG to pull examples from existing scripts and MCP to condition outputs.

## KelvinQiu802/llm-mcp-rag
This repository demonstrates an augmented LLM setup combining chat interfaces with MCP and RAG functionalities. It emphasizes a lightweight implementation without relying on heavy frameworks like LangChain. This can be particularly useful for understanding how to integrate RAG and MCP in a streamlined manner.

# FLASK VS GRADIO

| Feature         | **Flask**                      | **Gradio**                            |
| --------------- | ------------------------------ | ------------------------------------- |
| Setup           | Manual routing, HTML templates | Plug-and-play, no HTML needed         |
| Customizability | High (full control)            | Medium (but improving)                |
| Time to build   | Slower                         | Much faster                           |
| Ideal for       | Production-ready apps          | Prototypes, demos, portfolio projects |
| Colab support   | Not native (needs `ngrok`)     | Fully supported                       |

# DATASETS

| Role                            | Dataset                                       |
| ------------------------------- | --------------------------------------------- |
| 🎭 Real Movie Rom-Com Dialogues | **Cornell Movie Dialogs** (filtered by title) |
| 🎯 Tone/Emotion Conditioning    | **DailyDialog** (tagged emotional dialogues)  |
| 🧠 Retrieval Base               | Use either as RAG base (FAISS vector store)   |

# DailyDialog

| ✅ Pros                           | ❌ Cons                     |
| -------------------------------- | -------------------------- |
| Super clean, short conversations | Not actual movie dialogues |
| Emotion + topic labels           | May lack film realism      |
| Great for tone conditioning      |                            |

# Cornell Movie Dialogue

| ✅ Pros                           | ❌ Cons                |
| -------------------------------- | --------------------- |
| Pre-tokenized                    | No scene descriptions |
| Character names & IDs            | Limited context       |
| Dialogues from full-length films | Metadata is minimal   |

# ✅ The user will just describe a scene, and your assistant should:

Understand the implied genre, mood, and tone

Retrieve examples from a RAG store (without the user naming a movie)

Generate dialogue in that style, improving over generic GPT behavior

## How can we make the model genre aware?

### 🧩 Step 1: Build a Genre-Labeled RAG Corpus
Even though your user doesn’t provide a genre, your system should label it behind the scenes:

### 🧠 Step 2: Auto-Infer Genre from Scene Input (Simple Model)
Use a zero-shot classification model to auto-detect genre from the user’s input.

### 🔍 Step 3: Filter RAG Retrieval by Genre
Once you infer the genre:
Query only that genre subset of your FAISS index
Or store multiple FAISS indices (1 per genre) and select the right one

### ✍️ Step 4: Build a Prompt Like This:
''' text
Copy
Edit
User Scene: "A couple sits in silence in a diner booth. Rain hits the window. It's the end of something."

Inferred Genre: Romantic Comedy  
Tone: Bittersweet, awkward

Reference Dialogues (from similar scenes):
[Example 1]
[Example 2]

Write 2–3 lines of emotionally fitting dialogue in screenplay style.  '''


## Potential Work Flow
![image](https://github.com/user-attachments/assets/eb721809-b975-446b-bd1b-69aa6fd11a2d)
![image](https://github.com/user-attachments/assets/9499d7bd-3319-4004-8679-4b6e201c41e7)



