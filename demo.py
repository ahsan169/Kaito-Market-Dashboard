import subprocess
import sys
import time
import os

def print_banner():
    """Print demo banner"""
    print("\n" + "=" * 60)
    print(" " * 10 + "KAITO MARKET TRACKER - DEMO")
    print("=" * 60)
    print("\nThis demo will:")
    print("1. Test API connection")
    print("2. Run 30-day market analysis")
    print("3. Generate reports and visualizations")
    print("4. Launch interactive dashboard")
    print("\n" + "=" * 60 + "\n")

def run_demo():
    """Run complete demo"""
    print_banner()
    
    # Step 1: Test connection
    print("📡 Step 1: Testing API connection...")
    result = subprocess.run([sys.executable, "test_connection.py"])
    if result.returncode != 0:
        print("\n❌ Connection test failed. Please check your internet connection.")
        return 1
    
    print("\n✅ Connection test passed!\n")
    time.sleep(2)
    
    # Step 2: Run analysis
    print("📊 Step 2: Running market analysis (30 days)...")
    print("-" * 40)
    result = subprocess.run([sys.executable, "main.py", "--days", "30"])
    if result.returncode != 0:
        print("\n❌ Analysis failed.")
        return 1
    
    print("\n✅ Analysis complete!\n")
    time.sleep(2)
    
    # Step 3: Show generated files
    print("📁 Step 3: Generated files:")
    print("-" * 40)
    
    files = {
        "Data Files": [
            "./data/kaito_market_data.csv",
            "./data/kaito_spikes.csv"
        ],
        "Reports": [
            "./reports/kaito_analysis.json",
            "./reports/kaito_analysis_report.txt"
        ],
        "Visualizations": [
            "./visualizations/kaito_market_analysis.png",
            "./visualizations/kaito_spike_analysis.png"
        ]
    }
    
    for category, file_list in files.items():
        print(f"\n{category}:")
        for file in file_list:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"  ✓ {file} ({size:,} bytes)")
            else:
                print(f"  ✗ {file} (not found)")
    
    print("\n" + "-" * 40)
    time.sleep(3)
    
    # Step 4: Launch dashboard
    print("\n🚀 Step 4: Launching interactive dashboard...")
    print("  → Dashboard will open in your browser")
    print("  → Press Ctrl+C to stop the dashboard\n")
    time.sleep(2)
    
    # Run dashboard
    subprocess.run([sys.executable, "run_dashboard.py"])
    
    print("\n✅ Demo complete!")
    print("\nNext steps:")
    print("- Run with different parameters: python main.py --days 60")
    print("- Check generated reports in ./reports/")
    print("- View charts in ./visualizations/")
    print("- Customize thresholds: python main.py --price-threshold 15")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(run_demo())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)