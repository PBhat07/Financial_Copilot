from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

from rag.rag_pipeline import (
    load_pdfs,
    split_documents,
    create_embeddings_and_vector_db,
    setup_qa_chain,
    search_financial_documents,
)

from mcp_tools.financial_tools import (
    get_stock_price,
    get_earnings_report,
    get_company_news,
    get_dividend_yield,
)

# --- Config ---
PDF_DIR = "data/financial_docs"
VECTOR_DB_PATH = "faiss_index"
LLM_MODEL = "gemini-1.5-flash"

# --- App Setup ---
app = FastAPI(
    title="Financial Copilot API",
    description="LLM-based API for financial document search and live financial data.",
    version="1.0.0"
)

# --- Load & Initialize RAG Pipeline ---
documents = load_pdfs(PDF_DIR)
if not documents:
    raise RuntimeError("No documents found in PDF directory.")

chunks = split_documents(documents)
vector_db = create_embeddings_and_vector_db(chunks, VECTOR_DB_PATH)
qa_chain = setup_qa_chain(vector_db, LLM_MODEL)


# --- Request Models ---
class AskRequest(BaseModel):
    question: str


class FinancialQueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 4


class StockRequest(BaseModel):
    symbol: str


# --- Endpoints ---

@app.post("/ask")
def ask_question(payload: AskRequest):
    try:
        response = qa_chain.invoke({"query": payload.question})
        answer = response.get("result", "")
        source_docs = [
            {
                "page": doc.metadata.get("page"),
                "source": os.path.basename(doc.metadata.get("source", ""))
            }
            for doc in response.get("source_documents", [])
        ]
        return {
            "answer": answer,
            "sources": source_docs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query_financial_docs")
def query_financial_docs(payload: FinancialQueryRequest):
    try:
        # Use the internal retriever directly to limit top_k results
        retriever = vector_db.as_retriever(search_kwargs={"k": payload.top_k})
        temp_qa_chain = setup_qa_chain(vector_db, LLM_MODEL)
        response = temp_qa_chain.invoke({"query": payload.query})

        answer = response.get("result", "")
        source_docs = [
            {
                "page": doc.metadata.get("page"),
                "source": os.path.basename(doc.metadata.get("source", ""))
            }
            for doc in response.get("source_documents", [])
        ]
        return {
            "answer": answer,
            "sources": source_docs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_stock_price")
def get_price(data: StockRequest):
    try:
        price = get_stock_price(data.symbol)
        return {"symbol": data.symbol, "price": price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_earnings_report")
def earnings(data: StockRequest):
    try:
        report = get_earnings_report(data.symbol)
        return {"symbol": data.symbol, "earnings_report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_company_news")
def news(data: StockRequest):
    try:
        news_items = get_company_news(data.symbol)
        return {"symbol": data.symbol, "news": news_items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_dividend_yield")
def dividends(data: StockRequest):
    try:
        yield_value = get_dividend_yield(data.symbol)
        return {"symbol": data.symbol, "dividend_yield": yield_value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
