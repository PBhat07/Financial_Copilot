import os
from typing import Tuple, List, Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Configuration
PDF_DIR = os.getenv("PDF_DIR", "./data/financial_docs")  # Use local path instead of Google Drive
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./faiss_index")
LLM_BACKEND = os.getenv("LLM_BACKEND", "gemini")

def get_embeddings():
    """Get appropriate embeddings based on LLM backend"""
    if LLM_BACKEND == "gemini":
        print("🔧 Using Google Generative AI Embeddings")
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    else:
        print("🔧 Using HuggingFace Embeddings")
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_pdfs(directory: str):
    """Load PDF documents from directory"""
    print(f"📚 Loading PDFs from: {directory}")
    documents = []
    
    if not os.path.exists(directory):
        print(f"⚠️ PDF directory not found: {directory}")
        return []
    
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            try:
                loader = PyPDFLoader(filepath)
                docs = loader.load()
                print(f"✅ Loaded {len(docs)} pages from {filename}")
                documents.extend(docs)
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")
    
    return documents

def split_documents(documents):
    """Split documents into chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"📄 Split documents into {len(chunks)} chunks")
    return chunks

def create_vector_db(chunks, db_path):
    """Create or load vector database"""
    embeddings = get_embeddings()
    
    if os.path.exists(db_path):
        print(f"📦 Loading existing vector database from {db_path}")
        vector_db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    else:
        print("🔧 Creating new vector database...")
        vector_db = FAISS.from_documents(chunks, embeddings)
        vector_db.save_local(db_path)
        print(f"💾 Vector database saved to {db_path}")
    
    return vector_db

def setup_rag_pipeline():
    """Setup complete RAG pipeline"""
    from models.model_provider import get_llm
    
    print("🚀 Setting up RAG pipeline...")
    
    # Load or use existing vector database
    if os.path.exists(VECTOR_DB_PATH):
        print("📦 Using existing vector database")
        vector_db = create_vector_db([], VECTOR_DB_PATH)
    else:
        print("📚 Creating new vector database from documents")
        documents = load_pdfs(PDF_DIR)
        if not documents:
            raise ValueError("No documents found for RAG pipeline")
        
        chunks = split_documents(documents)
        vector_db = create_vector_db(chunks, VECTOR_DB_PATH)
    
    # Get LLM instance
    llm = get_llm()
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True
    )
    
    print("✅ RAG pipeline setup complete")
    return qa_chain

def search_financial_documents(query: str, qa_chain) -> Tuple[str, List]:
    """Search documents using RAG chain"""
    if qa_chain is None:
        raise ValueError("RAG chain not initialized")
    
    print(f"🔍 Searching for: '{query}'")
    
    try:
        response = qa_chain.invoke({"query": query})
        answer = response["result"]
        source_documents = response["source_documents"]
        
        print("✅ Search completed successfully")
        return answer, source_documents
        
    except Exception as e:
        print(f"❌ Search failed: {e}")
        raise

# Backward compatibility functions
def setup_qa_chain(vector_db, llm):
    """Legacy function for backward compatibility"""
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True
    )

def create_embeddings_and_vector_db(chunks, db_path):
    """Legacy function for backward compatibility"""
    return create_vector_db(chunks, db_path)

# # /content/drive/MyDrive/Financial_Copilot/rag/rag_pipeline.py

# import os
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.chains import RetrievalQA
# from langchain_google_genai import ChatGoogleGenerativeAI
# # from google.colab import userdata # Keep this line if you use secrets, but it won't be used directly in the script for os.environ

# # --- Configuration ---
# PDF_DIR = '/content/drive/MyDrive/Financial_Copilot/data/financial_docs'
# VECTOR_DB_PATH = '/content/drive/MyDrive/Financial_Copilot/faiss_index'

# # API Key will be set as an environment variable *before* script execution (in Colab notebook)
# # So we don't need the userdata.get() call directly here anymore within the script.
# # os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY") # This line should now be COMMENTED OUT or REMOVED

# LLM_MODEL = "gemini-1.5-flash"

# # --- RAG Pipeline Core Functions ---
# # These functions remain mostly the same, as they handle the core logic

# def load_pdfs(directory):
#     """Loads all PDF files from the specified directory."""
#     print(f"Loading PDFs from: {directory}")
#     documents = []
#     if not os.path.exists(directory):
#         print(f"Error: PDF directory not found at {directory}. Please ensure your documents are there.")
#         return []

#     for filename in os.listdir(directory):
#         if filename.endswith(".pdf"):
#             filepath = os.path.join(directory, filename)
#             try:
#                 loader = PyPDFLoader(filepath)
#                 docs = loader.load()
#                 print(f"  Loaded {len(docs)} pages from {filename}")
#                 documents.extend(docs)
#             except Exception as e:
#                 print(f"  Error loading {filename}: {e}")
#     return documents

# def split_documents(documents):
#     """Splits documents into smaller chunks."""
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200,
#         length_function=len,
#         add_start_index=True,
#     )
#     chunks = text_splitter.split_documents(documents)
#     print(f"Split documents into {len(chunks)} chunks.")
#     return chunks

# def create_embeddings_and_vector_db(chunks, db_path):
#     """Creates embeddings for chunks and stores them in a FAISS vector database."""
#     print("Initializing Google Generative AI Embeddings model...")
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#     if os.path.exists(db_path):
#         print(f"Loading existing vector database from {db_path}...")
#         vector_db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
#         print("Vector database loaded.")
#     else:
#         print("Creating new vector database (this may take a while for many documents)...")
#         vector_db = FAISS.from_documents(chunks, embeddings)
#         vector_db.save_local(db_path)
#         print(f"Vector database created and saved to {db_path}")
#     return vector_db

# def setup_qa_chain(vector_db, llm):
#     """Sets up the RetrievalQA chain with a pre-built LLM object."""
#     print(f"Setting up QA chain with LLM: {type(llm).__name__}")
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=vector_db.as_retriever(search_kwargs={"k": 4}),
#         return_source_documents=True
#     )
#     print("QA chain setup complete.")
#     return qa_chain

# # def setup_qa_chain(vector_db, llm_model_name):
# #     """Sets up the RetrievalQA chain."""
# #     print(f"Setting up QA chain with LLM: {llm_model_name}")
# #     llm = ChatGoogleGenerativeAI(model=llm_model_name, temperature=0.1)

# #     qa_chain = RetrievalQA.from_chain_type(
# #         llm=llm,
# #         chain_type="stuff",
# #         retriever=vector_db.as_retriever(search_kwargs={"k": 4}),
# #         return_source_documents=True
# #     )
# #     print("QA chain setup complete.")
# #     return qa_chain

# # --- MODIFIED: search_financial_documents function ---
# # It now takes an already initialized qa_chain as an argument.
# def search_financial_documents(query: str, qa_chain: RetrievalQA):
#     """
#     Retrieves information from the financial documents using the provided RAG QA chain.
#     This is the function signature your LLM Agent teammate will use.
#     """
#     if qa_chain is None:
#         raise ValueError("RAG QA chain is not initialized. Please call setup_qa_chain first.")

#     # Prints for console debugging/logging, will appear in Colab output widget
#     print(f"\n[RAG Search] Query: '{query}'")

#     response = qa_chain.invoke({"query": query})
#     answer = response["result"]
#     source_documents = response["source_documents"]

#     print("[RAG Search] Answer generated.")
#     # For a direct API/teammate call, you'd likely just return these,
#     # but for testing, we'll include more detailed printing in the UI part.
#     return answer, source_documents


# # --- Main Execution Block (for direct script testing only) ---
# # This block is mainly for command-line testing; the UI will use the functions directly.
# if __name__ == "__main__":
#     print("\n--- Starting RAG Pipeline Setup for Command-Line Testing ---")
#     os.makedirs(os.path.dirname(VECTOR_DB_PATH), exist_ok=True)

#     # These steps now happen only once
#     documents = load_pdfs(PDF_DIR)
#     if not documents:
#         print("No PDF documents found. Exiting.")
#         exit()

#     chunks = split_documents(documents)
#     vector_db = create_embeddings_and_vector_db(chunks, VECTOR_DB_PATH)

#     try:
#         qa_chain = setup_qa_chain(vector_db, LLM_MODEL)
#     except Exception as e:
#         print(f"Failed to set up QA chain. Check your LLM_MODEL and Google API Key. Error: {e}")
#         print("Ensure 'GOOGLE_API_KEY' is correctly set as a Colab Secret or environment variable.")
#         exit()

#     print("\n--- RAG Pipeline Setup Complete. Ready for command-line queries. ---")
#     print("Type 'exit' to quit.")

#     while True:
#         user_query = input("\nEnter your query about the financial documents: ")
#         if user_query.lower() == 'exit':
#             print("Exiting RAG pipeline testing.")
#             break
#         # Pass the initialized qa_chain to the function
#         answer, sources = search_financial_documents(user_query, qa_chain)

#         # Print results for command-line interface
#         print("\n--- Answer ---")
#         print(answer)
#         print("\n--- Sources ---")
#         for doc in sources:
#             print(f"Page: {doc.metadata.get('page')}, Source: {os.path.basename(doc.metadata.get('source'))}")