
This project is part of a collaborative financial co-pilot application. Specifically, this branch implements the Multiple Context Protocol (MCP)-inspired API server using FastAPI — enabling modular, scalable interaction between an LLM client and real-time financial tools.

### 🚀 Overview

The financial_api service acts as an MCP-like backend built with FastAPI. It exposes multiple modular tools as HTTP endpoints, wrapping real APIs and Retrieval-Augmented Generation (RAG) pipelines. This setup allows an LLM-based client (e.g., LangChain + OpenAI) to dynamically query financial data and knowledge sources via a clear client-server architecture.

While not fully MCP-spec-compliant (due to FastAPI’s HTTP approach), this service mimics core MCP concepts:

| MCP Concept                         | Implemented with FastAPI? | Notes                                                     |
|-------------------------------------|----------------------------|-----------------------------------------------------------|
| 🧠 LLM at the center                | ✅                         | LangChain + OpenAI LLM interacts as the client            |
| 🔌 Tools as external modules        | ✅                         | Each tool is a FastAPI route serving real financial APIs/RAG |
| 📡 Client-server architecture       | ✅                         | FastAPI acts as server, LLM client sends requests         |
| 🛰️ Real API integration            | ✅                         | Calls Alpha Vantage, NewsAPI, and other financial data sources |
| 🔁 Modular and scalable             | ✅                         | Easily add/remove API routes and RAG tools                |
| 🧱 MCP SDK-level STDIO/JSON-RPC     | ❌                         | Uses HTTP rather than JSON-RPC or STDIO                  |
| 🏷️ Official MCP label              | ❌                         | Functionally similar but not MCP-spec-compliant           |



### 🛠️ Tech Stack

     Python 3.x

     FastAPI

     Retrieval-Augmented Generation (RAG) pipeline

     uvicorn (ASGI server)


### ⚙️ Setup & Running

  1. Clone the repo and enter directory

     git clone https://github.com/yourusername/financial_co_pilot.git

     cd financial_api

  2. Create and activate virtual environment

     python -m venv venv

     venv\Scripts\activate    # Windows 

  3. Install dependencies

     pip install -r requirements.txt

  4. Setup environment variables
     (Copy .env.example to .env and fill in your API keys for OpenAI, Alpha Vantage, NewsAPI, etc.)

     cp .env.example .env

5. Run the FastAPI server

     uvicorn api_server:app --reload

    Open http://localhost:8000/docs to explore the automatically generated interactive API docs (Swagger UI).




