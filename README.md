# KAITO Market Dashboard Guide

## 🚀 Quick Start

### Prerequisites
1. Run the market analysis first to generate data:
   ```bash
   python main.py
   ```

2. Install Streamlit (included in requirements.txt):
   ```bash
   pip install -r requirements.txt
   ```

### Launch Dashboard

#### Option 1: Using the launcher script
```bash
python run_dashboard.py
```

#### Option 2: Using the all-in-one script
```bash
# Linux/Mac
./run.sh

# Windows
run.bat
```

#### Option 3: Direct Streamlit command
```bash
streamlit run streamlit_app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## 📊 Dashboard Features

### 1. **Overview Page**
- **Key Metrics**: Current price, 30-day change, total volume, volatility, spike count
- **Main Chart**: Interactive price and volume chart with spike markers
- **Volatility Analysis**: 7-day and 14-day rolling volatility
- **Correlation Matrix**: Relationships between price, volume, and changes

### 2. **Price Analysis**
- **Price Statistics**: High, low, average, standard deviation
- **Bollinger Bands**: Price with upper/lower bands for volatility visualization
- **Price Distribution**: Histogram of daily price changes
- **Detailed price movement tracking**

### 3. **Volume Analysis**
- **Volume Metrics**: Total, average, highest, lowest volumes
- **Volume Chart**: Color-coded bars (green for increase, red for decrease)
- **Volume-Price Scatter**: Relationship between volume and price
- **Moving averages for trend identification**

### 4. **Spike Detection**
- **Spike Summary**: Count of price and volume spikes
- **Timeline View**: Visual representation of spike events on price chart
- **Spike Details Table**: Comprehensive list with timestamps and magnitudes
- **Color coding**: Green for upward spikes, red for downward

### 5. **Statistics**
- **Price Stats Tab**: Comprehensive price metrics
- **Volume Stats Tab**: Detailed volume analysis
- **Market Stats Tab**: Current market cap, supply, and recent changes

## 🎨 Interactive Features

### Date Range Filter
- Use the sidebar date picker to filter data
- Analyze specific time periods
- All charts update dynamically

### Chart Interactions
- **Hover**: See detailed information for any data point
- **Zoom**: Click and drag to zoom into specific areas
- **Pan**: Hold shift and drag to pan across the chart
- **Double-click**: Reset zoom to full view

### Export Options
- **Download Charts**: Use the camera icon on any chart
- **Save as PNG**: Export individual visualizations
- **Full Screen**: Expand charts for detailed view

## 🔧 Customization

### Modify Thresholds
To change spike detection thresholds, run:
```bash
python main.py --price-threshold 15 --volume-threshold 75
```

### Update Data
1. Re-run the analysis to fetch latest data:
   ```bash
   python main.py
   ```

2. Click "🔄 Refresh Data" in the dashboard sidebar

### Change Time Period
Analyze different periods:
```bash
# 60-day analysis
python main.py --days 60
```

## 📱 Dashboard Controls

### Sidebar Options
- **Date Range**: Filter data by date
- **View Mode**: Switch between different analysis pages
- **Refresh Button**: Reload data without restarting

### Keyboard Shortcuts
- `R`: Rerun the app (when focused on Streamlit)
- `C`: Clear cache
- `Esc`: Exit fullscreen mode

## 🎯 Use Cases

### 1. **Daily Monitoring**
- Check Overview page for quick market status
- Review spike alerts for significant events
- Monitor volatility trends

### 2. **Deep Analysis**
- Use Price Analysis for technical indicators
- Volume Analysis for liquidity assessment
- Statistics page for comprehensive metrics

### 3. **Report Generation**
- Export charts for presentations
- Use statistics for written reports
- Document spike events with the details table

## 🐛 Troubleshooting

### Common Issues

1. **"Data not found" error**
   - Run `python main.py` first to generate data
   - Check that files exist in `data/` and `reports/` folders

2. **Dashboard won't start**
   - Ensure Streamlit is installed: `pip install streamlit`
   - Check port 8501 is not in use
   - Try: `streamlit run streamlit_app.py --server.port 8502`

3. **Charts not displaying**
   - Clear browser cache
   - Try a different browser
   - Check console for JavaScript errors

4. **Slow performance**
   - Reduce date range in sidebar
   - Clear Streamlit cache: Click "Clear cache" in menu
   - Close other browser tabs

### Debug Mode
Run with additional logging:
```bash
streamlit run streamlit_app.py --logger.level debug
```
