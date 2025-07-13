import os
import subprocess
import sys
from dotenv import load_dotenv

def main():
    """Launch the Financial API server with all features"""
    
    # Load environment variables
    load_dotenv()
    
    # Check if required packages are installed
    try:
        import fastapi
        import uvicorn
        import pyngrok
        import fastapi_mcp
    except ImportError as e:
        print("❌ Missing required packages. Please install:")
        print("pip install -r requirements.txt")
        print(f"Missing: {e}")
        return
    
    # Check for API keys
    required_keys = ["TWELVE_DATA_API_KEY", "FMP_API_KEY", "NEWS_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print("⚠️ Warning: Missing API keys:")
        for key in missing_keys:
            print(f"  - {key}")
        print("Some features may not work properly.")
        print("")
    
    # Check ngrok token
    if not os.getenv("NGROK_AUTH_TOKEN"):
        print("⚠️ NGROK_AUTH_TOKEN not set. API will only be accessible locally.")
        print("Get a free token at: https://dashboard.ngrok.com/get-started/your-authtoken")
        print("")
    
    print("🚀 Launching Financial Copilot API...")
    print("="*50)
    
    # Run the API server
    try:
        subprocess.run([sys.executable, "api_server.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
