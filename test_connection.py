import requests
import json

def test_coingecko_connection():
    """Test basic CoinGecko API connectivity"""
    print("Testing CoinGecko API connection...")
    
    # Test 1: Ping
    try:
        response = requests.get("https://api.coingecko.com/api/v3/ping")
        if response.status_code == 200:
            print("✓ API ping successful")
        else:
            print(f"✗ API ping failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False
    
    # Test 2: Check KAITO token exists
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/kaito")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ KAITO token found")
            print(f"  - Name: {data.get('name', 'N/A')}")
            print(f"  - Symbol: {data.get('symbol', 'N/A').upper()}")
            print(f"  - Current Price: ${data.get('market_data', {}).get('current_price', {}).get('usd', 'N/A')}")
        else:
            print(f"✗ KAITO token not found: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error fetching KAITO data: {e}")
        return False
    
    # Test 3: Check market chart endpoint
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/coins/kaito/market_chart",
            params={'vs_currency': 'usd', 'days': '1'}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Market chart endpoint working")
            print(f"  - Price points: {len(data.get('prices', []))}")
            print(f"  - Volume points: {len(data.get('total_volumes', []))}")
        else:
            print(f"✗ Market chart endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error fetching market chart: {e}")
        return False
    
    print("\n✅ All tests passed! You can run the main script.")
    return True

if __name__ == "__main__":
    test_coingecko_connection()