# tools/retrieval.py

from langchain.agents import Tool
from rag.rag_pipeline import search_financial_documents

def make_financial_retriever_tool(qa_chain):
    """
    Create a tool for the agent to retrieve answers from financial documents.
    The tool uses the QA chain to search the vector store and get an answer.
    """
    # Define the actual function the tool will execute
    def _run_financial_search(query: str) -> str:
        try:
            answer, source_docs = search_financial_documents(query, qa_chain)
            # (We return only the answer text. The agent can ask for sources if needed, 
            # or we could format them here if we wanted the agent to see citations.)
            return answer
        except Exception as e:
            return f"Error during document search: {e}"

    # Create a LangChain Tool instance
    return Tool(
        name="FinancialDocumentRetriever",
        func=_run_financial_search,
        description=(
            "Use this tool to answer questions by searching the financial document database. "
            "Provide a financial question, and it will return an answer based on the documents."
        )
    )
