import os
import sys
import subprocess
import webbrowser
import time
import getpass
from pathlib import Path

# Import authentication configuration
from auth_config import ADMIN_PASSWORD

def authenticate():
    """Authenticate user with password"""
    print("\n🔐 Authentication required to launch dashboard")
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

def check_data_exists():
    """Check if required data files exist"""
    required_files = [
        './data/kaito_market_data.csv',
        './reports/kaito_analysis.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required data files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n⚠️  Please run the market analysis first:")
        print("   python main.py")
        return False
    
    return True

def check_streamlit_installed():
    """Check if Streamlit is installed"""
    try:
        import streamlit
        return True
    except ImportError:
        print("❌ Streamlit is not installed.")
        print("   Please install requirements: pip install -r requirements.txt")
        return False

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("=" * 60)
    print(" " * 15 + "KAITO DASHBOARD LAUNCHER")
    print("=" * 60)
    print()
    
    # Authenticate user before proceeding
    if not authenticate():
        return 1
    
    # Check prerequisites
    if not check_streamlit_installed():
        return 1
    
    if not check_data_exists():
        response = input("\nWould you like to run the analysis now? (y/n): ")
        if response.lower() == 'y':
            print("\nRunning market analysis...")
            subprocess.run([sys.executable, "main.py"])
            print("\nAnalysis complete! Launching dashboard...\n")
        else:
            return 1
    
    # Launch Streamlit
    print("🚀 Launching KAITO Dashboard...")
    print("   The dashboard will open in your default browser.")
    print("   Press Ctrl+C to stop the server.\n")
    
    # Set Streamlit config
    env = os.environ.copy()
    env['STREAMLIT_THEME_PRIMARY_COLOR'] = '#1f77b4'
    env['STREAMLIT_THEME_BACKGROUND_COLOR'] = '#ffffff'
    env['STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR'] = '#f0f2f6'
    
    # Start Streamlit
    try:
        # Wait a moment before opening browser
        time.sleep(2)
        
        # Open browser automatically
        webbrowser.open('http://localhost:8501')
        
        # Run Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], env=env)
        
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped.")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(launch_dashboard())