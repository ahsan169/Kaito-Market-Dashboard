import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
from typing import Dict
import os
import config

class Visualizer:
    def __init__(self):
        self.fig_size = config.FIGURE_SIZE
        self.dpi = config.DPI
        plt.style.use(config.CHART_STYLE)
        
    def create_market_charts(self, df: pd.DataFrame, spikes_df: pd.DataFrame, stats: Dict) -> str:
        """
        Create comprehensive market analysis charts
        
        Args:
            df: Market data
            spikes_df: Spike events
            stats: Calculated statistics
            
        Returns:
            Path to saved chart
        """
        fig, axes = plt.subplots(3, 1, figsize=self.fig_size)
        fig.suptitle('KAITO Token Market Analysis (30-Day Period)', fontsize=16, fontweight='bold')
        
        # 1. Price Chart
        ax1 = axes[0]
        ax1.plot(df['timestamp'], df['price'], 'b-', linewidth=2, label='Price')
        ax1.plot(df['timestamp'], df['price_ma7'], 'r--', alpha=0.7, label='7-day MA')
        
        # Mark price spikes
        if not spikes_df.empty:
            price_spikes = spikes_df[spikes_df['metric'] == 'price']
            for _, spike in price_spikes.iterrows():
                color = 'green' if spike['direction'] == 'up' else 'red'
                ax1.scatter(spike['timestamp'], spike['value'], 
                           color=color, s=100, zorder=5, alpha=0.8)
                ax1.annotate(f"{spike['change_pct']:.1f}%",
                           (spike['timestamp'], spike['value']),
                           xytext=(5, 5), textcoords='offset points',
                           fontsize=9, color=color)
        
        ax1.set_ylabel('Price (USD)', fontsize=12)
        ax1.set_title(f'Price Movement (Current: ${stats["price"]["current"]:.4f})', fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='best')
        
        # 2. Volume Chart
        ax2 = axes[1]
        colors = ['green' if df['volume'].iloc[i] > df['volume'].iloc[i-1] else 'red' 
                  for i in range(1, len(df))]
        colors = ['gray'] + colors  # First bar is gray
        
        ax2.bar(df['timestamp'], df['volume'], color=colors, alpha=0.7, width=0.8)
        ax2.plot(df['timestamp'], df['volume_ma7'], 'orange', linewidth=2, label='7-day MA')
        
        # Mark volume spikes
        if not spikes_df.empty:
            volume_spikes = spikes_df[spikes_df['metric'] == 'volume']
            for _, spike in volume_spikes.iterrows():
                ax2.axvline(spike['timestamp'], color='red', linestyle='--', alpha=0.7)
        
        ax2.set_ylabel('Volume (USD)', fontsize=12)
        ax2.set_title('Trading Volume', fontsize=14)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.legend(loc='best')
        
        # Format y-axis for millions
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        
        # 3. Price vs Volume Correlation
        ax3 = axes[2]
        
        # Normalize for comparison
        price_norm = (df['price'] - df['price'].min()) / (df['price'].max() - df['price'].min())
        volume_norm = (df['volume'] - df['volume'].min()) / (df['volume'].max() - df['volume'].min())
        
        ax3.plot(df['timestamp'], price_norm, 'b-', linewidth=2, label='Price (normalized)')
        ax3.plot(df['timestamp'], volume_norm, 'orange', linewidth=2, alpha=0.7, label='Volume (normalized)')
        
        # Add correlation coefficient
        correlation = df['price'].corr(df['volume'])
        ax3.text(0.02, 0.95, f'Correlation: {correlation:.3f}', 
                transform=ax3.transAxes, fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        ax3.set_ylabel('Normalized Value', fontsize=12)
        ax3.set_xlabel('Date', fontsize=12)
        ax3.set_title('Price-Volume Correlation Analysis', fontsize=14)
        ax3.legend(loc='best')
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim(-0.1, 1.1)
        
        # Format x-axis for all subplots
        for ax in axes:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        # Save
        os.makedirs(config.VISUALIZATIONS_DIR, exist_ok=True)
        output_path = os.path.join(config.VISUALIZATIONS_DIR, 'kaito_market_analysis.png')
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Chart saved to {output_path}")
        return output_path
    
    def create_spike_distribution_chart(self, spikes_df: pd.DataFrame) -> str:
        """
        Create spike distribution chart
        
        Args:
            spikes_df: Spike events data
            
        Returns:
            Path to saved chart
        """
        if spikes_df.empty:
            print("No spikes to visualize")
            return None
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('KAITO Spike Event Analysis', fontsize=14, fontweight='bold')
        
        # Spike types distribution
        spike_types = spikes_df['type'].value_counts()
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        ax1.pie(spike_types.values, labels=spike_types.index, autopct='%1.1f%%',
                colors=colors, startangle=90)
        ax1.set_title('Spike Types Distribution')
        
        # Spike intensity distribution
        ax2.hist(spikes_df['change_pct'], bins=10, color='skyblue', edgecolor='black', alpha=0.7)
        ax2.set_xlabel('Change Percentage (%)')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Spike Intensity Distribution')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = os.path.join(config.VISUALIZATIONS_DIR, 'kaito_spike_analysis.png')
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Spike analysis chart saved to {output_path}")
        return output_path