import requests
import time
from typing import Dict, Optional
import config

class DataFetcher:
    def __init__(self):
        self.base_url = config.COINGECKO_BASE_URL
        self.token_id = config.TOKEN_ID
        self.headers = config.HEADERS
        
    def fetch_market_chart(self, days: int = 30) -> Optional[Dict]:
        """
        Fetch historical market data from CoinGecko
        
        Args:
            days: Number of days to fetch
            
        Returns:
            Dict with prices, volumes, and market caps or None if error
        """
        endpoint = f"{self.base_url}/coins/{self.token_id}/market_chart"
        params = {
            'vs_currency': config.VS_CURRENCY,
            'days': days,
            'interval': 'daily'
        }
        
        print(f"Fetching {days}-day market data for {self.token_id.upper()}...")
        
        try:
            response = requests.get(endpoint, params=params, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            print(f"✓ Successfully fetched {len(data.get('prices', []))} data points")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching market data: {e}")
            return None
    
    def fetch_current_data(self) -> Optional[Dict]:
        """
        Fetch current token information
        
        Returns:
            Dict with current token data or None if error
        """
        endpoint = f"{self.base_url}/coins/{self.token_id}"
        params = {
            'localization': 'false',
            'tickers': 'false',
            'market_data': 'true',
            'community_data': 'false',
            'developer_data': 'false'
        }
        
        print(f"Fetching current data for {self.token_id.upper()}...")
        
        try:
            response = requests.get(endpoint, params=params, headers=self.headers)
            response.raise_for_status()
            
            print("✓ Successfully fetched current market data")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching current data: {e}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test API connection
        
        Returns:
            True if connection successful, False otherwise
        """
        endpoint = f"{self.base_url}/ping"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            print("✓ CoinGecko API connection successful")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"✗ CoinGecko API connection failed: {e}")
            return False