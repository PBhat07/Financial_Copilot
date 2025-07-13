import requests
import json

def test_api():
    """Test your API endpoints"""
    base_url = "http://localhost:8000"
    
    # Test endpoints
    tests = [
        ("Health Check", f"{base_url}/"),
        ("Stock Price", f"{base_url}/stock/AAPL"),
        ("Earnings", f"{base_url}/earnings/MSFT"),
        ("News", f"{base_url}/news/Tesla?limit=2"),
        ("Dividend", f"{base_url}/dividend/AAPL")
    ]
    
    print("🧪 Testing Financial API...")
    print("=" * 50)
    
    for name, url in tests:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: SUCCESS")
                # Pretty print first few lines
                data = response.json()
                print(f"   Sample: {json.dumps(data, indent=2)[:100]}...")
            else:
                print(f"❌ {name}: FAILED ({response.status_code})")
        except Exception as e:
            print(f"❌ {name}: ERROR - {e}")
        print()

if __name__ == "__main__":
    test_api()
