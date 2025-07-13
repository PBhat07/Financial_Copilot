from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP
from pyngrok import ngrok
from dotenv import load_dotenv
import requests
import os
import uvicorn
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()
# Get API keys from environment
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")
FMP_API_KEY = os.getenv("FMP_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")

# Application settings
APPLICATION_PORT = int(os.getenv("API_PORT", "8000"))
HOST = os.getenv("API_HOST", "0.0.0.0")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    print("🚀 Starting Financial API Server...")
    
    # Set up ngrok if token is provided and enabled
    tunnel = None
    if NGROK_AUTH_TOKEN and os.getenv("ENABLE_NGROK", "false").lower() == "true":
        print("🌐 Setting up ngrok tunnel...")
        try:
            ngrok.set_auth_token(NGROK_AUTH_TOKEN)
            
            # Create tunnel with your static domain
            STATIC_DOMAIN = os.getenv("NGROK_DOMAIN", "rat-expert-amazingly.ngrok-free.app")
            tunnel = ngrok.connect(APPLICATION_PORT, domain=STATIC_DOMAIN)
            public_url = tunnel.public_url

            print(f"✅ ngrok tunnel created: {public_url}")
            print(f"📊 API Documentation: {public_url}/docs")
            print(f"🔗 MCP Server: {public_url}/mcp")
            
            # Store the URL for later use
            app.state.public_url = public_url
        except Exception as e:
            print(f"⚠️ Failed to create ngrok tunnel: {e}")
            print("💡 Continuing with localhost only")
    else:
        print("🌐 Running in localhost mode")
        print(f"📊 API Documentation: http://localhost:{APPLICATION_PORT}/docs")
        print(f"🔗 MCP Server: http://localhost:{APPLICATION_PORT}/mcp")
    
    yield
    
    # Cleanup
    if tunnel:
        print("🛑 Closing ngrok tunnel...")
        try:
            ngrok.disconnect(tunnel.public_url)
        except:
            pass

# Create FastAPI app with lifecycle management
app = FastAPI(
    title="Financial Copilot API",
    description="Real-time financial data retrieval service with MCP integration",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your existing financial endpoints (minimal changes)
@app.get("/stock/{symbol}")
async def get_stock_price(symbol: str):
    """Get current stock price for a given symbol"""
    if not TWELVE_DATA_API_KEY:
        raise HTTPException(status_code=500, detail="TWELVE_DATA_API_KEY not configured")
    
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_DATA_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "price" in data:
            return {
                "symbol": symbol,
                "price": float(data["price"]),
                "status": "success",
                "source": "twelve_data"
            }
        else:
            raise HTTPException(
                status_code=404, 
                detail=f"Price data not found for {symbol}: {data.get('message', 'Unknown error')}"
            )
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")

@app.get("/earnings/{symbol}")
async def get_earnings_report(symbol: str):
    """Get latest earnings report for a company"""
    if not FMP_API_KEY:
        raise HTTPException(status_code=500, detail="FMP_API_KEY not configured")
    
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=1&apikey={FMP_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            report = data[0]
            return {
                "symbol": symbol,
                "date": report.get('date'),
                "revenue": report.get('revenue'),
                "net_income": report.get('netIncome'),
                "eps": report.get('eps'),
                "gross_profit": report.get('grossProfit'),
                "status": "success",
                "source": "fmp"
            }
        else:
            raise HTTPException(status_code=404, detail=f"No earnings data found for {symbol}")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")

@app.get("/news/{company}")
async def get_company_news(company: str, limit: int = 3):
    """Get latest news for a company"""
    if not NEWS_API_KEY:
        raise HTTPException(status_code=500, detail="NEWS_API_KEY not configured")
    
    url = f"https://newsapi.org/v2/everything?q={company}&pageSize={limit}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "ok":
            articles = []
            for article in data.get("articles", [])[:limit]:
                articles.append({
                    "title": article.get('title'),
                    "description": article.get('description'),
                    "published_at": article.get('publishedAt'),
                    "url": article.get('url'),
                    "source": article.get('source', {}).get('name')
                })
            
            return {
                "company": company,
                "articles": articles,
                "total_results": len(articles),
                "status": "success",
                "source": "news_api"
            }
        else:
            raise HTTPException(status_code=404, detail=f"No news found for {company}")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")

@app.get("/dividend/{symbol}")
async def get_dividend_yield(symbol: str):
    """Get dividend yield for a stock"""
    if not FMP_API_KEY:
        raise HTTPException(status_code=500, detail="FMP_API_KEY not configured")
    
    url = f"https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?limit=1&apikey={FMP_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            metrics = data[0]
            dividend_yield = metrics.get("dividendYield")
            
            if dividend_yield is not None:
                return {
                    "symbol": symbol,
                    "dividend_yield": round(dividend_yield * 100, 2),
                    "dividend_yield_decimal": dividend_yield,
                    "period": metrics.get("period"),
                    "status": "success",
                    "source": "fmp"
                }
            else:
                return {
                    "symbol": symbol,
                    "dividend_yield": 0,
                    "message": "No dividend data available",
                    "status": "success",
                    "source": "fmp"
                }
        else:
            raise HTTPException(status_code=404, detail=f"No metrics found for {symbol}")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")

# Health check endpoint
@app.get("/")
async def root():
    """API health check"""
    return {
        "message": "Financial Copilot API is running",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs",
        "mcp": "/mcp",
        "endpoints": {
            "stock": "/stock/{symbol}",
            "earnings": "/earnings/{symbol}",
            "news": "/news/{company}",
            "dividend": "/dividend/{symbol}"
        }
    }

# Add MCP integration (this is the magic!)
mcp = FastApiMCP(
    app,
    name="Financial Copilot MCP Server",
    description="Real-time financial data retrieval tools for AI agents",
)

# Mount MCP server - this exposes all your endpoints as MCP tools automatically!
mcp.mount()

if __name__ == "__main__":
    print("🚀 Starting Financial Copilot API Server...")
    print(f"📍 Local server will run on: http://localhost:{APPLICATION_PORT}")
    print(f"📚 API docs will be at: http://localhost:{APPLICATION_PORT}/docs")
    print(f"🔗 MCP server will be at: http://localhost:{APPLICATION_PORT}/mcp")
    
    # Run the server
    uvicorn.run(
        app, 
        host=HOST, 
        port=APPLICATION_PORT,
        log_level="info"
    )
