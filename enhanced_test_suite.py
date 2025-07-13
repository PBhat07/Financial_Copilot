#!/usr/bin/env python3
"""
Enhanced Test Suite for Financial Copilot
Tests complex scenarios and shows differences between LLM backends
"""

import os
import time
import sys
from dotenv import load_dotenv
load_dotenv()

# Import agent
try:
    from agent.agent_executor import FinancialAgentExecutor
except ImportError:
    from agent_executor import FinancialAgentExecutor

# Complex test scenarios
COMPLEX_TEST_SCENARIOS = [
    # 1. Market Analysis
    {
        "category": "Market Analysis",
        "queries": [
            "Analyze the current market sentiment for tech stocks",
            "What are the key factors driving Tesla's stock price volatility?",
            "How would you evaluate if the market is overvalued right now?"
        ]
    },
    
    # 2. Investment Strategy
    {
        "category": "Investment Strategy", 
        "queries": [
            "If I have $10,000 to invest, what would be a good diversified portfolio strategy?",
            "What are the pros and cons of value vs growth investing in the current market?",
            "How should I adjust my investment strategy for a recession?"
        ]
    },
    
    # 3. Company Analysis
    {
        "category": "Company Analysis",
        "queries": [
            "Compare Apple and Microsoft as investment opportunities",
            "What are the key risks and opportunities for AI companies?",
            "How would you analyze a company's competitive moat?"
        ]
    },
    
    # 4. Technical vs Fundamental
    {
        "category": "Technical vs Fundamental",
        "queries": [
            "When should I use technical analysis vs fundamental analysis?",
            "What are the most reliable technical indicators for stock trading?",
            "How do I calculate and interpret the Sharpe ratio?"
        ]
    },
    
    # 5. Real-time Data Integration
    {
        "category": "Real-time Data",
        "queries": [
            "Get current prices for AAPL, MSFT, and GOOGL and compare their P/E ratios",
            "What's the latest news affecting Tesla's stock price?",
            "Show me earnings data for the top 5 tech companies"
        ]
    }
]

def test_backend_comprehensive(backend_name):
    """Test a backend with comprehensive scenarios"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING {backend_name.upper()} BACKEND")
    print(f"{'='*60}")
    
    os.environ["LLM_BACKEND"] = backend_name
    
    try:
        agent = FinancialAgentExecutor()
        print(f"✅ {backend_name} agent initialized successfully")
        
        total_queries = 0
        successful_queries = 0
        total_time = 0
        
        for scenario in COMPLEX_TEST_SCENARIOS:
            print(f"\n📊 Category: {scenario['category']}")
            print("-" * 40)
            
            for query in scenario['queries']:
                total_queries += 1
                print(f"\n🔍 Query: {query}")
                
                try:
                    t0 = time.time()
                    result = agent.process_query(query)
                    dt = time.time() - t0
                    total_time += dt
                    
                    if result["status"] == "success":
                        successful_queries += 1
                        print(f"✅ SUCCESS ({dt:.2f}s)")
                        print(f"📝 Answer: {result['answer'][:300]}{'...' if len(result['answer'])>300 else ''}")
                    else:
                        print(f"❌ FAILED ({dt:.2f}s): {result['answer']}")
                        
                except Exception as e:
                    print(f"❌ ERROR ({time.time()-t0:.2f}s): {e}")
                
                print("-" * 30)
        
        # Summary
        success_rate = (successful_queries / total_queries) * 100
        avg_time = total_time / total_queries if total_queries > 0 else 0
        
        print(f"\n📈 {backend_name.upper()} SUMMARY:")
        print(f"   Success Rate: {success_rate:.1f}% ({successful_queries}/{total_queries})")
        print(f"   Average Response Time: {avg_time:.2f}s")
        print(f"   Total Test Time: {total_time:.2f}s")
        
        return {
            "backend": backend_name,
            "success_rate": success_rate,
            "avg_time": avg_time,
            "total_queries": total_queries,
            "successful_queries": successful_queries
        }
        
    except Exception as e:
        print(f"❌ Failed to initialize {backend_name} agent: {e}")
        return None

def compare_backends():
    """Compare performance between backends"""
    print("🚀 FINANCIAL COPILOT - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    results = {}
    
    # Test Gemini
    if os.getenv("GOOGLE_API_KEY"):
        results["gemini"] = test_backend_comprehensive("gemini")
    else:
        print("⚠️ Skipping Gemini: Missing GOOGLE_API_KEY")
    
    # Test Claude  
    if os.getenv("ANTHROPIC_API_KEY"):
        results["claude"] = test_backend_comprehensive("claude")
    else:
        print("⚠️ Skipping Claude: Missing ANTHROPIC_API_KEY")
    
    # Comparison
    if len(results) > 1:
        print(f"\n{'='*60}")
        print("📊 BACKEND COMPARISON")
        print(f"{'='*60}")
        
        for backend, result in results.items():
            if result:
                print(f"\n{backend.upper()}:")
                print(f"  Success Rate: {result['success_rate']:.1f}%")
                print(f"  Avg Response Time: {result['avg_time']:.2f}s")
                print(f"  Total Queries: {result['total_queries']}")
    
    return results

if __name__ == "__main__":
    compare_backends() 