# Fixed agent_executor.py with simplified MCP integration and flexible API support

import os
import sys
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain.tools import Tool

# Add paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

load_dotenv()

from models.model_provider import get_llm
from rag.rag_pipeline import setup_rag_pipeline, search_financial_documents

class FinancialAgentExecutor:
    """Enhanced Financial Agent with flexible API integration"""
    
    def __init__(self):
        self.llm_backend = os.getenv("LLM_BACKEND", "gemini")
        
        # Flexible API URL - try ngrok first, fallback to localhost
        self.external_api_url = self._get_api_url()
        
        # Initialize components
        self.llm = get_llm()
        self.memory = ConversationBufferWindowMemory(
            k=5,  # Keep last 5 interactions
            memory_key="chat_history",
            return_messages=True
        )
        
        # Setup tools
        self.tools = self._setup_tools()
        self.agent = self._initialize_agent()
        
        print(f"✅ Financial Agent initialized with {self.llm_backend} backend")
        print(f"🌐 Using API URL: {self.external_api_url}")

    def _get_api_url(self) -> str:
        """Get the best available API URL"""
        # Priority order: env variable -> ngrok -> localhost
        env_url = os.getenv("EXTERNAL_API_URL")
        if env_url:
            return env_url
        
        # Try common ngrok URLs
        ngrok_urls = [
            "https://rat-expert-amazingly.ngrok-free.app",
            "https://financial-copilot.ngrok-free.app"
        ]
        
        for url in ngrok_urls:
            try:
                response = requests.get(f"{url}/", timeout=3)
                if response.status_code == 200:
                    print(f"✅ Found working ngrok URL: {url}")
                    return url
            except:
                continue
        
        # Fallback to localhost
        localhost_url = "http://localhost:8000"
        try:
            response = requests.get(f"{localhost_url}/", timeout=3)
            if response.status_code == 200:
                print(f"✅ Using localhost API: {localhost_url}")
                return localhost_url
        except:
            print(f"⚠️ Warning: No API server found. Some features may not work.")
            print(f"💡 Start the API server with: python launch_api.py")
        
        # Return localhost as default (will fail gracefully)
        return localhost_url

    def create_mcp_tool_from_function(self, func, name, description):
        """Create a tool with better output formatting and input validation"""
        def wrapped_tool(input_str):
            # Input validation
            if not input_str or input_str.strip() in ["N/A", "None", ""]:
                return f"Error: Invalid input '{input_str}'. Please provide a valid input."
            
            try:
                result = func(input_str.strip())
                # Format output to indicate completion
                if name == "StockPrice":
                    return f"SUCCESS: {result}. Task completed - no further action needed."
                elif name == "EarningsReport":
                    return f"SUCCESS: {result}. Task completed - no further action needed."
                elif name == "CompanyNews":
                    return f"SUCCESS: {result}. Task completed - no further action needed."
                elif name == "DocumentSearch":
                    return f"SUCCESS: {result}. Task completed - no further action needed."
                else:
                    return f"SUCCESS: {result}. Task completed."
            except Exception as e:
                return f"Error executing {name}: {str(e)}"
        
        return Tool(
            name=name,
            description=description,
            func=wrapped_tool
        )

    def _setup_tools(self):
        """Setup simplified tools with flexible API support"""
        tools = []
        
        # RAG Tool - Use your existing RAG function directly
        def rag_search_tool(query: str) -> str:
            """Your existing RAG function as a tool"""
            try:
                if not hasattr(self, 'qa_chain'):
                    print("🔧 Initializing RAG pipeline...")
                    self.qa_chain = setup_rag_pipeline()
                
                answer, sources = search_financial_documents(query, self.qa_chain)
                
                # Format response with sources
                formatted_answer = f"{answer}\n\nSources:\n"
                for i, doc in enumerate(sources[:3], 1):
                    source_name = os.path.basename(doc.metadata.get('source', 'Unknown'))
                    page = doc.metadata.get('page', 'Unknown')
                    formatted_answer += f"{i}. {source_name} (Page {page})\n"
                
                return formatted_answer
                
            except Exception as e:
                return f"RAG search error: {str(e)}"
        
        # External API Tools - Flexible API support
        def external_stock_price(symbol: str) -> str:
            """Call external API for stock price"""
            try:
                response = requests.get(f"{self.external_api_url}/stock/{symbol}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return f"Current price of {symbol}: ${data.get('price', 'N/A')}"
                else:
                    return f"Could not fetch price for {symbol} (Status: {response.status_code})"
            except requests.exceptions.ConnectionError:
                return f"API server not available. Please start the API server with: python launch_api.py"
            except Exception as e:
                return f"API Error: {str(e)}"
        
        def external_earnings(symbol: str) -> str:
            """Get earnings from external API"""
            try:
                response = requests.get(f"{self.external_api_url}/earnings/{symbol}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return f"Earnings for {symbol}: Revenue: ${data.get('revenue', 'N/A')}, Net Income: ${data.get('net_income', 'N/A')}"
                else:
                    return f"Could not fetch earnings for {symbol} (Status: {response.status_code})"
            except requests.exceptions.ConnectionError:
                return f"API server not available. Please start the API server with: python launch_api.py"
            except Exception as e:
                return f"API Error: {str(e)}"
        
        def external_news(company: str) -> str:
            """Get news from external API"""
            try:
                response = requests.get(f"{self.external_api_url}/news/{company}?limit=3", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get('articles', [])
                    news_text = f"Latest news for {company}:\n"
                    for i, article in enumerate(articles[:3], 1):
                        news_text += f"{i}. {article.get('title', 'No title')}\n"
                    return news_text
                else:
                    return f"Could not fetch news for {company} (Status: {response.status_code})"
            except requests.exceptions.ConnectionError:
                return f"API server not available. Please start the API server with: python launch_api.py"
            except Exception as e:
                return f"API Error: {str(e)}"
        
        # Add all tools using the simple wrapper
        tools.append(self.create_mcp_tool_from_function(
            rag_search_tool,
            "DocumentSearch",
            "Search financial documents and reports for specific information. Use this ONLY for questions about company financials, earnings, reports, or document-based analysis. DO NOT use for general definitions or explanations. Input: search query string."
        ))
        
        tools.append(self.create_mcp_tool_from_function(
            external_stock_price,
            "StockPrice", 
            "Get current stock price from external API. Use ONLY for requests asking for current/latest stock prices. Input: stock symbol (e.g., TSLA, AAPL). Returns: current price in USD."
        ))
        
        tools.append(self.create_mcp_tool_from_function(
            external_earnings,
            "EarningsReport",
            "Get earnings report from external API. Use for company earnings data and financial metrics. Input: stock symbol (e.g., TSLA, AAPL). Returns: earnings data and key metrics."
        ))
        
        tools.append(self.create_mcp_tool_from_function(
            external_news,
            "CompanyNews",
            "Get company news from external API. Use for latest company news and market updates. Input: company name or stock symbol. Returns: recent news articles."
        ))
        
        return tools

    def _initialize_agent(self):
        """Initialize the LangChain agent with fixed configuration"""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=self.memory,
            handle_parsing_errors=True,
            verbose=True,
            max_iterations=8,  # Increased for multi-step queries
            early_stopping_method="generate"  # Stop when agent generates final answer
            # Removed return_intermediate_steps=True to fix the run() issue
        )

    def process_query(self, user_query: str) -> Dict[str, Any]:
        """Process user query through the agent"""
        print(f"\n🤖 Processing query with {self.llm_backend} backend...")
        print(f"📝 Query: {user_query}")
        
        try:
            # Check if query needs tool use
            if self._needs_tool_use(user_query):
                print("🔧 Using agentic workflow (tools enabled)")
                # Use invoke instead of run to avoid the output key issue
                response = self.agent.invoke({"input": user_query})
                if isinstance(response, dict) and "output" in response:
                    response = response["output"]
                elif hasattr(response, 'content'):
                    response = response.content
            else:
                print("💬 Using direct LLM response")
                response = self.llm.invoke(user_query)
                if hasattr(response, 'content'):
                    response = response.content
            
            return {
                "answer": response,
                "backend": self.llm_backend,
                "status": "success"
            }
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "answer": error_msg,
                "backend": self.llm_backend,
                "status": "error"
            }

    def _needs_tool_use(self, query: str) -> bool:
        """Determine if query needs tool usage"""
        # Direct LLM questions (general knowledge, explanations, definitions)
        direct_llm_keywords = [
            "explain", "what is", "define", "describe", "how does", "tell me about",
            "concept", "definition", "meaning", "ratio", "metric", "formula",
            "difference between", "compare", "analysis", "strategy", "approach"
        ]
        
        # Tool-requiring keywords
        tool_keywords = [
            "search", "find", "show", "get", "fetch", "retrieve",
            "document", "report", "financial", "earnings", "revenue",
            "current", "latest", "recent", "stock price", "market data",
            "news", "data", "information", "price", "now", "today"
        ]
        
        query_lower = query.lower()
        
        # Check for direct LLM questions first
        if any(keyword in query_lower for keyword in direct_llm_keywords):
            # Only use tools if it's specifically asking for current/recent data
            if not any(keyword in query_lower for keyword in ["current", "latest", "recent", "now", "today", "stock price"]):
                return False
        
        # Check for tool-requiring keywords
        return any(keyword in query_lower for keyword in tool_keywords)

    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        # Check external API status
        api_status = "unknown"
        try:
            response = requests.get(f"{self.external_api_url}/", timeout=5)
            if response.status_code == 200:
                api_status = "connected"
            else:
                api_status = "error"
        except:
            api_status = "disconnected"
        
        return {
            "llm_backend": self.llm_backend,
            "external_api_status": api_status,
            "external_api_url": self.external_api_url,
            "tools_available": len(self.tools),
            "memory_size": len(self.memory.chat_memory.messages)
        }

# Convenience function for quick usage
def create_agent() -> FinancialAgentExecutor:
    """Create and return a configured financial agent"""
    return FinancialAgentExecutor()