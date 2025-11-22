#!/bin/bash
# run_all.sh - Run KAITO Market Tracker and Dashboard

echo "======================================"
echo "    KAITO MARKET TRACKER SUITE"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Checking dependencies..."
pip install -r requirements.txt -q

# Menu
echo ""
echo "What would you like to do?"
echo "1) Run market analysis"
echo "2) Launch dashboard"
echo "3) Run analysis then launch dashboard"
echo "4) Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Starting market analysis..."
        python main.py "$@"
        ;;
    2)
        echo ""
        python run_dashboard.py
        ;;
    3)
        echo ""
        echo "Starting market analysis..."
        python main.py "$@"
        if [ $? -eq 0 ]; then
            echo ""
            echo "Analysis complete! Launching dashboard..."
            sleep 2
            python run_dashboard.py
        else
            echo "Analysis failed. Dashboard not launched."
        fi
        ;;
    4)
        echo "Exiting..."
        ;;
    *)
        echo "Invalid choice. Exiting..."
        ;;
esac

# Deactivate virtual environment
deactivate

echo ""
echo "Done!"