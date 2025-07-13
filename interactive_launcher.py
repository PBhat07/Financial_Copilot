#!/usr/bin/env python3
"""
Interactive Financial Copilot Launcher
User-friendly interface for testing and using the Financial Copilot
"""

import os
import sys
import time
from dotenv import load_dotenv
load_dotenv()

# Import agent
try:
    from agent.agent_executor import FinancialAgentExecutor
except ImportError:
    from agent_executor import FinancialAgentExecutor

def print_banner():
    """Print the application banner"""
    print("=" * 70)
    print("🌟 FINANCIAL COPILOT - AI-Powered Financial Analysis")
    print("=" * 70)
    print("🤖 Multi-LLM Support: Gemini & Claude")
    print("📊 Real-time Data: Stock Prices, Earnings, News")
    print("🔍 RAG Pipeline: Document Search & Analysis")
    print("=" * 70)

def check_environment():
    """Check if environment is properly configured"""
    print("🔧 Checking environment configuration...")
    
    required_vars = {
        "LLM_BACKEND": "LLM Backend (gemini/claude)",
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
    
    print("✅ Environment configuration looks good!")
    return True

def get_example_queries():
    """Get categorized example queries"""
    return {
        "General Knowledge": [
            "Explain the concept of market capitalization",
            "What is the difference between fundamental and technical analysis?",
            "How do I calculate the P/E ratio?",
            "What is a dividend yield?"
        ],
        "Real-time Data": [
            "Get the current stock price of AAPL",
            "What are the latest earnings for TSLA?",
            "Show me recent news about Microsoft",
            "Get current prices for AAPL, MSFT, and GOOGL"
        ],
        "Investment Analysis": [
            "Compare Apple and Microsoft as investment opportunities",
            "What are the key risks for AI companies?",
            "How would you analyze a company's competitive moat?",
            "What factors affect Tesla's stock price?"
        ],
        "Portfolio Strategy": [
            "If I have $10,000 to invest, what would be a good strategy?",
            "How should I adjust my investment strategy for a recession?",
            "What are the pros and cons of value vs growth investing?",
            "How do I build a diversified portfolio?"
        ],
        "Technical Analysis": [
            "What are the most reliable technical indicators?",
            "When should I use technical vs fundamental analysis?",
            "How do I calculate and interpret the Sharpe ratio?",
            "What are the key support and resistance levels?"
        ]
    }

def display_menu():
    """Display the main menu"""
    print("\n📋 MAIN MENU")
    print("-" * 30)
    print("1. 🚀 Quick Test (3 queries)")
    print("2. 🧪 Comprehensive Test (15 queries)")
    print("3. 💬 Interactive Chat")
    print("4. 📊 Example Queries")
    print("5. ⚙️  Switch LLM Backend")
    print("6. 🔧 System Status")
    print("7. 📖 Help & Documentation")
    print("0. 🚪 Exit")
    print("-" * 30)

def switch_backend():
    """Allow user to switch LLM backend"""
    current_backend = os.getenv("LLM_BACKEND", "gemini").lower()
    print(f"\n🤖 Current LLM Backend: {current_backend.upper()}")
    
    if current_backend == "gemini":
        new_backend = "claude"
        required_key = "ANTHROPIC_API_KEY"
    else:
        new_backend = "gemini"
        required_key = "GOOGLE_API_KEY"
    
    if not os.getenv(required_key):
        print(f"❌ Cannot switch to {new_backend.upper()}: Missing {required_key}")
        return
    
    os.environ["LLM_BACKEND"] = new_backend
    print(f"✅ Switched to {new_backend.upper()} backend")
    print("💡 Changes will take effect on next query")

def quick_test():
    """Run a quick test with 3 queries"""
    print("\n🚀 Running Quick Test...")
    
    test_queries = [
        "Explain market capitalization in simple terms",
        "Get the current stock price of AAPL",
        "What are the key risks for AI companies?"
    ]
    
    try:
        agent = FinancialAgentExecutor()
        print(f"✅ Agent initialized with {os.getenv('LLM_BACKEND', 'gemini').upper()} backend")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. 📝 Query: {query}")
            print("🤖 Processing...")
            
            t0 = time.time()
            result = agent.process_query(query)
            dt = time.time() - t0
            
            if result["status"] == "success":
                print(f"✅ SUCCESS ({dt:.2f}s)")
                answer = result['answer'][:200] + "..." if len(result['answer']) > 200 else result['answer']
                print(f"📝 Answer: {answer}")
            else:
                print(f"❌ FAILED ({dt:.2f}s): {result['answer']}")
            
            print("-" * 50)
        
        print("🎉 Quick test completed!")
        
    except Exception as e:
        print(f"❌ Error during quick test: {e}")

def comprehensive_test():
    """Run comprehensive test suite"""
    print("\n🧪 Running Comprehensive Test Suite...")
    print("This will test 15 complex queries across different categories.")
    
    try:
        # Import and run the enhanced test suite
        from enhanced_test_suite import compare_backends
        compare_backends()
    except ImportError:
        print("❌ Enhanced test suite not found. Please ensure enhanced_test_suite.py exists.")
    except Exception as e:
        print(f"❌ Error during comprehensive test: {e}")

def interactive_chat():
    """Start interactive chat mode"""
    print("\n💬 Interactive Chat Mode")
    print("Type your questions below (or 'exit' to return to menu)")
    print("💡 Try asking about stocks, analysis, or investment strategies")
    print("-" * 50)
    
    try:
        agent = FinancialAgentExecutor()
        print(f"✅ Agent ready with {os.getenv('LLM_BACKEND', 'gemini').upper()} backend")
        
        while True:
            try:
                user_input = input("\n💬 Your question: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye', '']:
                    print("👋 Returning to main menu...")
                    break
                
                if not user_input:
                    continue
                
                print("🤖 Processing...")
                t0 = time.time()
                result = agent.process_query(user_input)
                dt = time.time() - t0
                
                if result["status"] == "success":
                    print(f"✅ Answer ({dt:.2f}s):")
                    print(f"📝 {result['answer']}")
                else:
                    print(f"❌ Error ({dt:.2f}s): {result['answer']}")
                
            except KeyboardInterrupt:
                print("\n👋 Returning to main menu...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")

def show_example_queries():
    """Show categorized example queries"""
    examples = get_example_queries()
    
    print("\n📊 EXAMPLE QUERIES BY CATEGORY")
    print("=" * 50)
    
    for category, queries in examples.items():
        print(f"\n📋 {category}:")
        for i, query in enumerate(queries, 1):
            print(f"  {i}. {query}")
    
    print("\n💡 Copy any query and use it in Interactive Chat mode!")

def show_system_status():
    """Show system status and configuration"""
    print("\n🔧 SYSTEM STATUS")
    print("=" * 30)
    
    # Backend info
    backend = os.getenv("LLM_BACKEND", "gemini").lower()
    print(f"🤖 LLM Backend: {backend.upper()}")
    
    # API status
    api_url = os.getenv("EXTERNAL_API_URL", "Not set")
    print(f"🌐 External API: {api_url}")
    
    # Key availability
    keys_status = {
        "GOOGLE_API_KEY": "Gemini",
        "ANTHROPIC_API_KEY": "Claude",
        "TWELVE_DATA_API_KEY": "Stock Data",
        "FMP_API_KEY": "Financial Data",
        "NEWS_API_KEY": "News Data"
    }
    
    print("\n🔑 API Keys Status:")
    for key, service in keys_status.items():
        status = "✅ Available" if os.getenv(key) else "❌ Missing"
        print(f"  {service}: {status}")
    
    # RAG status
    pdf_dir = os.getenv("PDF_DIR", "./data/financial_docs")
    if os.path.exists(pdf_dir):
        pdf_count = len([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
        print(f"📚 RAG Documents: {pdf_count} PDFs found")
    else:
        print("📚 RAG Documents: No documents directory found")

def show_help():
    """Show help and documentation"""
    print("\n📖 HELP & DOCUMENTATION")
    print("=" * 40)
    
    print("\n🚀 Getting Started:")
    print("1. Copy env.example to .env")
    print("2. Fill in your API keys")
    print("3. Run: python interactive_launcher.py")
    print("4. Choose your preferred option from the menu")
    
    print("\n🤖 LLM Backends:")
    print("- Gemini: Fast, good for general queries")
    print("- Claude: More detailed, better for complex analysis")
    print("- Switch between them using option 5")
    
    print("\n📊 Query Types:")
    print("- General Knowledge: Definitions, concepts, explanations")
    print("- Real-time Data: Current prices, earnings, news")
    print("- Investment Analysis: Company comparisons, risk assessment")
    print("- Portfolio Strategy: Investment advice, diversification")
    print("- Technical Analysis: Indicators, trading strategies")
    
    print("\n🔧 Troubleshooting:")
    print("- If queries fail, check your API keys")
    print("- For slow responses, try switching LLM backends")
    print("- For tool errors, ensure external API is running")
    
    print("\n📚 More Information:")
    print("- GitHub: [Your Repository URL]")
    print("- Documentation: README.md")
    print("- Issues: GitHub Issues page")

def main():
    """Main application loop"""
    print_banner()
    
    if not check_environment():
        print("\n❌ Environment not properly configured.")
        print("Please set up your .env file and try again.")
        return
    
    while True:
        try:
            display_menu()
            choice = input("\n🎯 Enter your choice (0-7): ").strip()
            
            if choice == "0":
                print("👋 Thank you for using Financial Copilot!")
                break
            elif choice == "1":
                quick_test()
            elif choice == "2":
                comprehensive_test()
            elif choice == "3":
                interactive_chat()
            elif choice == "4":
                show_example_queries()
            elif choice == "5":
                switch_backend()
            elif choice == "6":
                show_system_status()
            elif choice == "7":
                show_help()
            else:
                print("❌ Invalid choice. Please enter a number between 0-7.")
            
            input("\n⏸️  Press Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n👋 Thank you for using Financial Copilot!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main() 