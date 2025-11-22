# report_generator.py - Generate reports in various formats

import json
import os
import pandas as pd
from datetime import datetime
from typing import Dict
import config

class ReportGenerator:
    def __init__(self):
        self.data_dir = config.DATA_DIR
        self.reports_dir = config.REPORTS_DIR
        
        # Create directories if they don't exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def save_market_data(self, df: pd.DataFrame, filename: str = 'kaito_market_data.csv') -> str:
        """
        Save market data to CSV
        
        Args:
            df: Market data DataFrame
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        output_path = os.path.join(self.data_dir, filename)
        df.to_csv(output_path, index=False)
        print(f"✓ Market data saved to {output_path}")
        return output_path
    
    def save_spike_data(self, spikes_df: pd.DataFrame, filename: str = 'kaito_spikes.csv') -> str:
        """
        Save spike events to CSV
        
        Args:
            spikes_df: Spike events DataFrame
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        if spikes_df.empty:
            print("No spike data to save")
            return None
        
        output_path = os.path.join(self.data_dir, filename)
        spikes_df.to_csv(output_path, index=False)
        print(f"✓ Spike data saved to {output_path}")
        return output_path
    
    def save_json_report(self, stats: Dict, spikes_df: pd.DataFrame, 
                        filename: str = 'kaito_analysis.json') -> str:
        """
        Save comprehensive JSON report
        
        Args:
            stats: Statistics dictionary
            spikes_df: Spike events DataFrame
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        report = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'token': config.TOKEN_ID,
                'currency': config.VS_CURRENCY,
                'analysis_days': stats['period']['days']
            },
            'statistics': stats,
            'spike_summary': {
                'total_spikes': len(spikes_df),
                'price_spikes': len(spikes_df[spikes_df['metric'] == 'price']) if not spikes_df.empty else 0,
                'volume_spikes': len(spikes_df[spikes_df['metric'] == 'volume']) if not spikes_df.empty else 0,
                'largest_price_increase': spikes_df[spikes_df['direction'] == 'up']['change_pct'].max() if not spikes_df.empty else 0,
                'largest_price_decrease': spikes_df[spikes_df['direction'] == 'down']['change_pct'].min() if not spikes_df.empty else 0
            }
        }
        
        # Add spike details
        if not spikes_df.empty:
            report['spikes'] = spikes_df.to_dict('records')
        
        output_path = os.path.join(self.reports_dir, filename)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"✓ JSON report saved to {output_path}")
        return output_path
    
    def generate_text_report(self, stats: Dict, spikes_df: pd.DataFrame, 
                           filename: str = 'kaito_analysis_report.txt') -> str:
        """
        Generate human-readable text report
        
        Args:
            stats: Statistics dictionary
            spikes_df: Spike events DataFrame
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        output_path = os.path.join(self.reports_dir, filename)
        
        with open(output_path, 'w') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write(" " * 20 + "KAITO TOKEN MARKET ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Analysis Period: {stats['period']['start_date']} to {stats['period']['end_date']}\n")
            f.write(f"Duration: {stats['period']['days']} days\n\n")
            
            # Executive Summary
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 40 + "\n")
            f.write(f"• Current Price: ${stats['price']['current']:.4f}\n")
            f.write(f"• 30-Day Change: {stats['price']['change_30d']:+.2f}% (${stats['price']['change_30d_usd']:+.4f})\n")
            f.write(f"• Total Volume: ${stats['volume']['total_30d']:,.0f}\n")
            f.write(f"• Volatility: {stats['price']['volatility']:.2f}%\n")
            f.write(f"• Spike Events: {len(spikes_df)}\n\n")
            
            # Price Analysis
            f.write("PRICE ANALYSIS\n")
            f.write("-" * 40 + "\n")
            f.write(f"• Current: ${stats['price']['current']:.4f}\n")
            f.write(f"• 30-Day High: ${stats['price']['high']:.4f}\n")
            f.write(f"• 30-Day Low: ${stats['price']['low']:.4f}\n")
            f.write(f"• Average: ${stats['price']['average']:.4f}\n")
            f.write(f"• Median: ${stats['price']['median']:.4f}\n")
            f.write(f"• Standard Deviation: ${stats['price']['std_dev']:.4f}\n")
            f.write(f"• Volatility: {stats['price']['volatility']:.2f}%\n\n")
            
            # Volume Analysis
            f.write("VOLUME ANALYSIS\n")
            f.write("-" * 40 + "\n")
            f.write(f"• Total (30d): ${stats['volume']['total_30d']:,.0f}\n")
            f.write(f"• Daily Average: ${stats['volume']['average_daily']:,.0f}\n")
            f.write(f"• Daily Median: ${stats['volume']['median_daily']:,.0f}\n")
            f.write(f"• Highest: ${stats['volume']['highest']:,.0f} on {stats['volume']['highest_date']}\n")
            f.write(f"• Lowest: ${stats['volume']['lowest']:,.0f}\n\n")
            
            # Current Market Data
            if 'current_market' in stats:
                f.write("CURRENT MARKET DATA\n")
                f.write("-" * 40 + "\n")
                cm = stats['current_market']
                f.write(f"• Market Cap: ${cm['market_cap']:,.0f}\n")
                f.write(f"• FDV: ${cm['fully_diluted_valuation']:,.0f}\n")
                f.write(f"• Circulating Supply: {cm['circulating_supply']:,.0f} KAITO\n")
                f.write(f"• Total Supply: {cm['total_supply']:,.0f} KAITO\n")
                f.write(f"• 24h Change: {cm['24h_change']:+.2f}%\n")
                f.write(f"• 7d Change: {cm['7d_change']:+.2f}%\n")
                f.write(f"• 30d Change: {cm['30d_change']:+.2f}%\n\n")
            
            # Spike Events
            if not spikes_df.empty:
                f.write("SPIKE EVENTS TIMELINE\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total Events: {len(spikes_df)}\n\n")
                
                for _, spike in spikes_df.iterrows():
                    f.write(f"📍 {spike['timestamp'].strftime('%Y-%m-%d %H:%M')}\n")
                    f.write(f"   Type: {spike['type'].replace('_', ' & ').title()}\n")
                    f.write(f"   Change: {spike['change_pct']:+.2f}%\n")
                    f.write(f"   Price: ${spike.get('price', spike.get('value', 0)):.4f}\n")
                    f.write(f"   Volume: ${spike.get('volume', 0):,.0f}\n\n")
            else:
                f.write("SPIKE EVENTS\n")
                f.write("-" * 40 + "\n")
                f.write("No significant spikes detected with current thresholds.\n\n")
            
            # Footer
            f.write("=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
        
        print(f"✓ Text report saved to {output_path}")
        return output_path
    
    def generate_summary(self, stats: Dict, spikes_df: pd.DataFrame) -> None:
        """
        Print summary to console
        
        Args:
            stats: Statistics dictionary
            spikes_df: Spike events DataFrame
        """
        print("\n" + "=" * 60)
        print(" " * 15 + "ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"Token: KAITO")
        print(f"Period: {stats['period']['days']} days")
        print(f"Current Price: ${stats['price']['current']:.4f}")
        print(f"30-Day Change: {stats['price']['change_30d']:+.2f}%")
        print(f"Volatility: {stats['price']['volatility']:.2f}%")
        print(f"Total Volume: ${stats['volume']['total_30d']:,.0f}")
        print(f"Spike Events: {len(spikes_df)}")
        
        if not spikes_df.empty:
            print(f"Largest Price Spike: {spikes_df['change_pct'].max():+.2f}%")
        
        print("=" * 60 + "\n")