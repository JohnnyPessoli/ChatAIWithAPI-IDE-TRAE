import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import logging

class TrendAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def identify_product_trends(self, transaction_data, time_window=180):
        """
        Identify trending products based on transaction data
        """
        try:
            # Filter data for the specified time window
            end_date = transaction_data['purchase_date'].max()
            start_date = end_date - pd.Timedelta(days=time_window)
            recent_data = transaction_data[
                transaction_data['purchase_date'] >= start_date]
            
            # Aggregate sales by product and date
            product_daily_sales = recent_data.groupby(
                ['product_id', pd.Grouper(key='purchase_date', freq='D')]
            ).agg({
                'amount': 'sum',
                'transaction_id': 'count'
            }).rename(columns={'transaction_id': 'sales_count'}).reset_index()
            
            # Create time series for each product
            product_trends = {}
            for product_id, product_data in product_daily_sales.groupby('product_id'):
                if len(product_data) >= 14:  # Need sufficient data points
                    product_data = product_data.set_index('purchase_date').sort_index()
                    
                    # Fill missing dates with zeros
                    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
                    product_data = product_data.reindex(date_range, fill_value=0)
                    
                    # Calculate trend using moving average
                    product_data['sales_ma'] = product_data['sales_count'].rolling(
                        window=7, min_periods=1).mean()
                    
                    # Calculate growth rate (last 30 days vs previous 30 days)
                    last_30d = product_data['sales_count'][-30:].sum()
                    prev_30d = product_data['sales_count'][-60:-30].sum()
                    
                    growth_rate = ((last_30d - prev_30d) / max(prev_30d, 1)) * 100
                    
                    product_trends[product_id] = {
                        'growth_rate': growth_rate,
                        'last_30d_sales': last_30d,
                        'time_series': product_data
                    }
            
            # Sort products by growth rate
            sorted_trends = sorted(
                product_trends.items(), 
                key=lambda x: x[1]['growth_rate'], 
                reverse=True
            )
            
            return sorted_trends
            
        except Exception as e:
            self.logger.error(f"Error identifying product trends: {str(e)}")
            raise
    
    def forecast_product_demand(self, transaction_data, product_id, forecast_periods=30):
        """
        Forecast demand for a specific product
        """
        try:
            # Filter data for the specified product
            product_data = transaction_data[transaction_data['product_id'] == product_id]
            
            # Aggregate sales by date
            daily_sales = product_data.groupby(
                pd.Grouper(key='purchase_date', freq='D')
            )['transaction_id'].count().reset_index()
            
            # Ensure continuous date range
            date_range = pd.date_range(
                start=daily_sales['purchase_date'].min(),
                end=daily_sales['purchase_date'].max(),
                freq='D'
            )
            
            daily_sales = daily_sales.set_index('purchase_date')
            daily_sales = daily_sales.reindex(date_range, fill_value=0)
            
            # Apply Holt-Winters forecasting
            model = ExponentialSmoothing(
                daily_sales, 
                seasonal_periods=7,
                trend='add', 
                seasonal='add',
                use_boxcox=True
            )
            
            model_fit = model.fit(optimized=True)
            forecast = model_fit.forecast(forecast_periods)
            
            return forecast
            
        except Exception as e:
            self.logger.error(f"Error forecasting product demand: {str(e)}")
            raise