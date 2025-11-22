import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
import config

class DataProcessor:
    def __init__(self):
        self.price_threshold = config.PRICE_SPIKE_THRESHOLD
        self.volume_threshold = config.VOLUME_SPIKE_THRESHOLD
    
    def process_market_data(self, raw_data: Dict) -> pd.DataFrame:
        """
        Convert raw API data to structured DataFrame
        
        Args:
            raw_data: Raw data from CoinGecko API
            
        Returns:
            Processed DataFrame
        """
        if not raw_data:
            return pd.DataFrame()
        
        # Extract price data
        prices = raw_data.get('prices', [])
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Add volume data
        volumes = raw_data.get('total_volumes', [])
        if volumes:
            volume_df = pd.DataFrame(volumes, columns=['timestamp', 'volume'])
            volume_df['timestamp'] = pd.to_datetime(volume_df['timestamp'], unit='ms')
            df = df.merge(volume_df, on='timestamp', how='left')
        
        # Add market cap data
        market_caps = raw_data.get('market_caps', [])
        if market_caps:
            mcap_df = pd.DataFrame(market_caps, columns=['timestamp', 'market_cap'])
            mcap_df['timestamp'] = pd.to_datetime(mcap_df['timestamp'], unit='ms')
            df = df.merge(mcap_df, on='timestamp', how='left')
        
        # Calculate daily changes
        df['price_change'] = df['price'].diff()
        df['price_change_pct'] = df['price'].pct_change() * 100
        df['volume_change_pct'] = df['volume'].pct_change() * 100
        
        # Add date column
        df['date'] = df['timestamp'].dt.date
        
        # Add moving averages
        df['price_ma7'] = df['price'].rolling(window=7, min_periods=1).mean()
        df['volume_ma7'] = df['volume'].rolling(window=7, min_periods=1).mean()
        
        print(f"✓ Processed {len(df)} days of market data")
        return df
    
    def identify_spikes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Identify significant price and volume spikes
        
        Args:
            df: Processed market data
            
        Returns:
            DataFrame with spike events
        """
        spikes = []
        
        # Price spikes
        price_spikes = df[abs(df['price_change_pct']) > self.price_threshold].copy()
        
        for _, row in price_spikes.iterrows():
            spikes.append({
                'timestamp': row['timestamp'],
                'date': row['date'],
                'type': 'price',
                'metric': 'price',
                'direction': 'up' if row['price_change_pct'] > 0 else 'down',
                'change_pct': row['price_change_pct'],
                'absolute_change': row['price_change'],
                'value': row['price'],
                'volume': row['volume']
            })
        
        # Volume spikes
        volume_spikes = df[df['volume_change_pct'] > self.volume_threshold].copy()
        
        for _, row in volume_spikes.iterrows():
            # Check if we already have a price spike for this date
            existing = any(s['date'] == row['date'] for s in spikes)
            
            if existing:
                # Update existing spike
                for s in spikes:
                    if s['date'] == row['date']:
                        s['type'] = 'price_and_volume'
                        s['volume_change_pct'] = row['volume_change_pct']
            else:
                spikes.append({
                    'timestamp': row['timestamp'],
                    'date': row['date'],
                    'type': 'volume',
                    'metric': 'volume',
                    'direction': 'up',
                    'change_pct': row['volume_change_pct'],
                    'absolute_change': row['volume'] - df['volume'].shift(1).loc[row.name],
                    'value': row['volume'],
                    'price': row['price']
                })
        
        spike_df = pd.DataFrame(spikes)
        if not spike_df.empty:
            spike_df = spike_df.sort_values('timestamp')
            print(f"✓ Identified {len(spike_df)} spike events")
            print(f"  - Price spikes: {len(spike_df[spike_df['metric'] == 'price'])}")
            print(f"  - Volume spikes: {len(spike_df[spike_df['metric'] == 'volume'])}")
        else:
            print("✓ No significant spikes detected with current thresholds")
        
        return spike_df
    
    def calculate_statistics(self, df: pd.DataFrame, current_data: Dict = None) -> Dict:
        """
        Calculate comprehensive statistics
        
        Args:
            df: Market data DataFrame
            current_data: Current token data from API
            
        Returns:
            Dictionary with calculated statistics
        """
        stats = {
            'period': {
                'start_date': df['timestamp'].min().strftime('%Y-%m-%d'),
                'end_date': df['timestamp'].max().strftime('%Y-%m-%d'),
                'days': len(df)
            },
            'price': {
                'current': df['price'].iloc[-1],
                'high': df['price'].max(),
                'low': df['price'].min(),
                'average': df['price'].mean(),
                'median': df['price'].median(),
                'std_dev': df['price'].std(),
                'volatility': (df['price'].std() / df['price'].mean() * 100),
                'change_30d': ((df['price'].iloc[-1] - df['price'].iloc[0]) / df['price'].iloc[0] * 100),
                'change_30d_usd': (df['price'].iloc[-1] - df['price'].iloc[0])
            },
            'volume': {
                'total_30d': df['volume'].sum(),
                'average_daily': df['volume'].mean(),
                'median_daily': df['volume'].median(),
                'highest': df['volume'].max(),
                'lowest': df['volume'].min(),
                'highest_date': df.loc[df['volume'].idxmax(), 'date'].strftime('%Y-%m-%d')
            }
        }
        
        # Add current market data if available
        if current_data and 'market_data' in current_data:
            md = current_data['market_data']
            stats['current_market'] = {
                'market_cap': md.get('market_cap', {}).get('usd', 0),
                'fully_diluted_valuation': md.get('fully_diluted_valuation', {}).get('usd', 0),
                'circulating_supply': md.get('circulating_supply', 0),
                'total_supply': md.get('total_supply', 0),
                'max_supply': md.get('max_supply', 0),
                '24h_change': md.get('price_change_percentage_24h', 0),
                '7d_change': md.get('price_change_percentage_7d', 0),
                '14d_change': md.get('price_change_percentage_14d', 0),
                '30d_change': md.get('price_change_percentage_30d', 0),
                '1y_change': md.get('price_change_percentage_1y', 0)
            }
        
        print("✓ Calculated comprehensive statistics")
        return stats