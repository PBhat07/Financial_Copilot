#!/usr/bin/env python3
"""
Robust launcher and test script for Financial Copilot.
Checks environment, API server, and LLM backends (Gemini/Claude).
"""

import os
import sys
import time
import requests
from dotenv import load_dotenv
load_dotenv()

REQUIRED_ENV = [
    "LLM_BACKEND", "EXTERNAL_API_URL",
    "TWELVE_DATA_API_KEY", "FMP_API_KEY", "NEWS_API_KEY",
    "GOOGLE_API_KEY", "ANTHROPIC_API_KEY"
]

API_HEALTH_ENDPOINT = "/"  # Adjust if you have a specific health endpoint

# Print environment summary
print("\n=== ENVIRONMENT SUMMARY ===")
for var in REQUIRED_ENV:
    print(f"{var}: {os.getenv(var, '[NOT SET]')}")
print("==========================\n")

# Check API server
api_url = os.getenv("EXTERNAL_API_URL", "http://localhost:8000")
try:
    print(f"Checking API server at {api_url}{API_HEALTH_ENDPOINT} ...")
    resp = requests.get(api_url + API_HEALTH_ENDPOINT, timeout=10)
    if resp.status_code == 200:
        print("✅ API server reachable.")
    else:
        print(f"❌ API server error: {resp.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Could not reach API server: {e}")
    sys.exit(1)

# Import agent
try:
    from agent.agent_executor import FinancialAgentExecutor
except ImportError:
    from agent_executor import FinancialAgentExecutor

# Test queries designed to show differences between backends and test complex scenarios
TEST_QUERIES = [
    # General knowledge (should use direct LLM, not tools)
    "Explain the concept of market capitalization in simple terms",
    "What is the difference between fundamental and technical analysis?",
    "How would you analyze a company's debt-to-equity ratio?",
    
    # Tool-requiring queries
    "Get the current stock price of AAPL",
    "What are the latest earnings for TSLA?",
    "Show me recent news about Microsoft",
    
    # Complex queries that might need both tools and reasoning
    "Compare the P/E ratios of tech companies and explain what they mean",
    "What factors might affect Tesla's stock price today?",
    "Analyze the relationship between interest rates and stock market performance",
    "How would you evaluate if a stock is overvalued or undervalued?",
    
    # Multi-step reasoning queries
    "If I want to invest in renewable energy, what companies should I research and why?",
    "What are the key risks and opportunities for AI companies in the current market?",
    "How would you build a diversified portfolio for a 30-year investment horizon?"
]

# Test both backends if possible
def test_backend(backend_name, skip_if_missing_key=None):
    print(f"\n=== Testing backend: {backend_name} ===")
    os.environ["LLM_BACKEND"] = backend_name
    if skip_if_missing_key and not os.getenv(skip_if_missing_key):
        print(f"[SKIP] {backend_name} test: missing {skip_if_missing_key}")
        return False
    try:
        agent = FinancialAgentExecutor()
        for prompt in TEST_QUERIES:
            print(f"\nPrompt: {prompt}")
            t0 = time.time()
            result = agent.process_query(prompt)
            dt = time.time() - t0
            if result["status"] == "success":
                print(f"✅ PASS ({dt:.2f}s): {result['answer'][:200]}{'...' if len(result['answer'])>200 else ''}")
            else:
                print(f"❌ FAIL ({dt:.2f}s): {result['answer']}")
        return True
    except Exception as e:
        print(f"❌ Exception during {backend_name} test: {e}")
        return False

results = {}
# Test Gemini if key present
if os.getenv("GOOGLE_API_KEY"):
    results["gemini"] = test_backend("gemini", skip_if_missing_key="GOOGLE_API_KEY")
else:
    print("[SKIP] Gemini test: missing GOOGLE_API_KEY")
    results["gemini"] = False
# Test Claude if key present
if os.getenv("ANTHROPIC_API_KEY"):
    results["claude"] = test_backend("claude", skip_if_missing_key="ANTHROPIC_API_KEY")
else:
    print("[SKIP] Claude test: missing ANTHROPIC_API_KEY")
    results["claude"] = False

print("\n=== TEST SUMMARY ===")
for backend, passed in results.items():
    print(f"{backend}: {'PASS' if passed else 'FAIL or SKIPPED'}")

if all(results.values()):
    print("\n🎉 All tests passed! System is ready.")
    sys.exit(0)
else:
    print("\n⚠️ Some tests failed or were skipped. Check logs above.")
    sys.exit(1)
