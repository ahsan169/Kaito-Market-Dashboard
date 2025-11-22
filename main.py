import sys
import argparse
import getpass
from datetime import datetime
import config
from data_fetcher import DataFetcher
from data_processor import DataProcessor
from visualizer import Visualizer
from report_generator import ReportGenerator

# Import authentication configuration
from auth_config import ADMIN_PASSWORD

def print_header():
    """Print application header"""
    print("\n" + "=" * 60)
    print(" " * 15 + "KAITO MARKET TRACKER v1.0")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def authenticate():
    """Authenticate user with password"""
    if __name__ != "__main__":
        return True
        
    print("\n🔐 Authentication required to access market analysis")
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        password = getpass.getpass("Enter password: ")
        if password == ADMIN_PASSWORD:
            print("✅ Authentication successful!\n")
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            print(f"❌ Incorrect password! {remaining} attempts remaining.")
    
    print("\n🛑 Authentication failed. Access denied.")
    return False

def main(days: int = None, price_threshold: float = None, volume_threshold: float = None):
    """
    Main execution function
    
    Args:
        days: Number of days to analyze
        price_threshold: Price spike threshold percentage
        volume_threshold: Volume spike threshold percentage
    """
    # Authenticate user before proceeding
    if not authenticate():
        return 1
    # Use default values if not provided
    days = days or config.DEFAULT_DAYS
    price_threshold = price_threshold or config.PRICE_SPIKE_THRESHOLD
    volume_threshold = volume_threshold or config.VOLUME_SPIKE_THRESHOLD
    
    print_header()
    
    # Step 1: Initialize components
    print("🔧 Initializing components...")
    fetcher = DataFetcher()
    processor = DataProcessor()
    processor.price_threshold = price_threshold
    processor.volume_threshold = volume_threshold
    visualizer = Visualizer()
    reporter = ReportGenerator()
    
    # Step 2: Test API connection
    print("\n📡 Testing API connection...")
    if not fetcher.test_connection():
        print("❌ Failed to connect to CoinGecko API. Please check your internet connection.")
        return 1
    
    # Step 3: Fetch market data
    print(f"\n📊 Fetching {days}-day market data...")
    market_data = fetcher.fetch_market_chart(days)
    if not market_data:
        print("❌ Failed to fetch market data.")
        return 1
    
    current_data = fetcher.fetch_current_data()
    
    # Step 4: Process data
    print("\n🔍 Processing market data...")
    df = processor.process_market_data(market_data)
    if df.empty:
        print("❌ No data to process.")
        return 1
    
    # Step 5: Identify spikes
    print(f"\n🎯 Identifying spikes (price: >{price_threshold}%, volume: >{volume_threshold}%)...")
    spikes_df = processor.identify_spikes(df)
    
    # Step 6: Calculate statistics
    print("\n📈 Calculating statistics...")
    stats = processor.calculate_statistics(df, current_data)
    
    # Step 7: Generate visualizations
    print("\n🎨 Creating visualizations...")
    visualizer.create_market_charts(df, spikes_df, stats)
    if not spikes_df.empty:
        visualizer.create_spike_distribution_chart(spikes_df)
    
    # Step 8: Generate reports
    print("\n📝 Generating reports...")
    reporter.save_market_data(df)
    reporter.save_spike_data(spikes_df)
    reporter.save_json_report(stats, spikes_df)
    reporter.generate_text_report(stats, spikes_df)
    
    # Step 9: Display summary
    reporter.generate_summary(stats, spikes_df)
    
    print("✅ Analysis complete!\n")
    print("📁 Output files:")
    print(f"   • Data: {config.DATA_DIR}/")
    print(f"   • Reports: {config.REPORTS_DIR}/")
    print(f"   • Charts: {config.VISUALIZATIONS_DIR}/")
    print("\n" + "=" * 60 + "\n")
    
    return 0

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='KAITO Token Market Activity Tracker')
    parser.add_argument('-d', '--days', type=int, default=config.DEFAULT_DAYS,
                       help=f'Number of days to analyze (default: {config.DEFAULT_DAYS})')
    parser.add_argument('-p', '--price-threshold', type=float, default=config.PRICE_SPIKE_THRESHOLD,
                       help=f'Price spike threshold %% (default: {config.PRICE_SPIKE_THRESHOLD})')
    parser.add_argument('-v', '--volume-threshold', type=float, default=config.VOLUME_SPIKE_THRESHOLD,
                       help=f'Volume spike threshold %% (default: {config.VOLUME_SPIKE_THRESHOLD})')
    
    args = parser.parse_args()
    
    # Run main function
    exit_code = main(args.days, args.price_threshold, args.volume_threshold)
    sys.exit(exit_code)