#!/usr/bin/env python3
"""
Simple System Test for Financial Copilot
Run this to verify your installation and configuration
"""

import os
import sys
from dotenv import load_dotenv
load_dotenv()

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import langchain
        print("  ✅ LangChain")
    except ImportError as e:
        print(f"  ❌ LangChain: {e}")
        return False
    
    try:
        import torch
        print("  ✅ PyTorch")
    except ImportError as e:
        print(f"  ❌ PyTorch: {e}")
        return False
    
    try:
        import faiss
        print("  ✅ FAISS")
    except ImportError as e:
        print(f"  ❌ FAISS: {e}")
        return False
    
    try:
        import fastapi
        print("  ✅ FastAPI")
    except ImportError as e:
        print(f"  ❌ FastAPI: {e}")
        return False
    
    return True

def test_environment():
    """Test environment configuration"""
    print("\n🔧 Testing environment configuration...")
    
    required_vars = {
        "LLM_BACKEND": "LLM Backend",
        "EXTERNAL_API_URL": "External API URL",
        "TWELVE_DATA_API_KEY": "Twelve Data API Key",
        "FMP_API_KEY": "Financial Modeling Prep API Key",
        "NEWS_API_KEY": "News API Key"
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            missing_vars.append(f"  ❌ {var}: {description}")
        else:
            print(f"  ✅ {var}: {description}")
    
    # Check LLM-specific keys
    backend = os.getenv("LLM_BACKEND", "gemini").lower()
    if backend == "gemini" and not os.getenv("GOOGLE_API_KEY"):
        missing_vars.append("  ❌ GOOGLE_API_KEY: Required for Gemini backend")
    elif backend == "claude" and not os.getenv("ANTHROPIC_API_KEY"):
        missing_vars.append("  ❌ ANTHROPIC_API_KEY: Required for Claude backend")
    
    if missing_vars:
        print("\n⚠️ Missing environment variables:")
        for var in missing_vars:
            print(var)
        print("\n💡 Please copy env.example to .env and fill in your API keys")
        return False
    
    return True

def test_agent_initialization():
    """Test if the agent can be initialized"""
    print("\n🤖 Testing agent initialization...")
    
    try:
        from agent.agent_executor import FinancialAgentExecutor
        agent = FinancialAgentExecutor()
        print("  ✅ Agent initialized successfully")
        return True
    except Exception as e:
        print(f"  ❌ Agent initialization failed: {e}")
        return False

def test_simple_query():
    """Test a simple query"""
    print("\n💬 Testing simple query...")
    
    try:
        from agent.agent_executor import FinancialAgentExecutor
        agent = FinancialAgentExecutor()
        
        result = agent.process_query("Explain market capitalization in simple terms")
        
        if result["status"] == "success":
            print("  ✅ Query processed successfully")
            print(f"  📝 Response: {result['answer'][:100]}...")
            return True
        else:
            print(f"  ❌ Query failed: {result['answer']}")
            return False
            
    except Exception as e:
        print(f"  ❌ Query test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Financial Copilot - System Test")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Environment", test_environment),
        ("Agent Initialization", test_agent_initialization),
        ("Simple Query", test_simple_query)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 TEST SUMMARY")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your system is ready to use.")
        print("💡 Run 'python interactive_launcher.py' to start using Financial Copilot!")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        print("💡 Make sure you have:")
        print("  1. Installed all dependencies: pip install -r requirements.txt")
        print("  2. Set up your .env file with API keys")
        print("  3. Started the API server: python launch_api.py")

if __name__ == "__main__":
    main() 