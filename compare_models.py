#!/usr/bin/env python3
"""
Simple Model Comparison for Financial Copilot
Compares Gemini vs Claude performance
"""

import os
import time
from dotenv import load_dotenv

load_dotenv()

try:
    from agent.agent_executor import FinancialAgentExecutor
except ImportError:
    from agent_executor import FinancialAgentExecutor

def compare_models():
    """Simple comparison between Gemini and Claude"""
    print("🔬 MODEL COMPARISON TEST")
    print("=" * 40)
    
    # Test queries
    queries = [
        "Analyze sentiment: Apple reports record earnings growth",
        "What are key financial ratios for stock analysis?",
        "Get current price of MSFT"
    ]
    
    results = {}
    
    # Test available backends based on API keys
    backends_to_test = []
    
    if os.getenv("GOOGLE_API_KEY"):
        backends_to_test.append("gemini")
    else:
        print("⚠️ Skipping Gemini: Missing GOOGLE_API_KEY")
    
    if os.getenv("ANTHROPIC_API_KEY"):
        backends_to_test.append("claude")
    else:
        print("⚠️ Skipping Claude: Missing ANTHROPIC_API_KEY")
    
    if not backends_to_test:
        print("❌ No API keys found. Please set GOOGLE_API_KEY or ANTHROPIC_API_KEY")
        return
    
    for backend in backends_to_test:
        print(f"\n🧪 Testing {backend.upper()}:")
        
        # Set backend
        os.environ["LLM_BACKEND"] = backend
        agent = FinancialAgentExecutor()
        
        backend_results = []
        
        for i, query in enumerate(queries, 1):
            print(f"  {i}. {query[:50]}...")
            
            try:
                start_time = time.time()
                result = agent.process_query(query)
                response_time = time.time() - start_time
                
                backend_results.append({
                    "query": query,
                    "time": response_time,
                    "success": result.get('status') == 'success',
                    "answer_length": len(result.get('answer', ''))
                })
                
                print(f"     ⏱️ {response_time:.2f}s ✅")
                
            except Exception as e:
                backend_results.append({
                    "query": query,
                    "time": 0,
                    "success": False,
                    "error": str(e)
                })
                print(f"     ❌ Error")
        
        results[backend] = backend_results
    
    # Display comparison
    print("\n📊 COMPARISON RESULTS:")
    print("=" * 40)
    
    for backend in backends_to_test:
        data = results[backend]
        avg_time = sum(r['time'] for r in data) / len(data)
        success_rate = sum(1 for r in data if r['success']) / len(data) * 100
        
        print(f"\n{backend.upper()}:")
        print(f"  Average Time: {avg_time:.2f}s")
        print(f"  Success Rate: {success_rate:.1f}%")

if __name__ == "__main__":
    compare_models()
