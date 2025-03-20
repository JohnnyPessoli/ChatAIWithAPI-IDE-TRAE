import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import logging
import json
import os

class ReportGenerator:
    def __init__(self, output_dir='reports'):
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_customer_behavior_report(self, transaction_data, customer_data, time_period=365):
        """
        Generate a comprehensive report on customer behavior
        """
        try:
            # Filter data for the specified time period
            end_date = transaction_data['purchase_date'].max()
            start_date = end_date - pd.Timedelta(days=time_period)
            report_data = transaction_data[transaction_data['purchase_date'] >= start_date]
            
            # Generate report sections
            overview = self._generate_overview_section(report_data)
            customer_segments = self._generate_segment_section(customer_data)
            purchase_patterns = self._generate_purchase_patterns_section(report_data)
            product_analysis = self._generate_product_analysis_section(report_data)
            
            # Combine sections into a complete report
            report = {
                'title': f'Customer Behavior Report - {start_date.date()} to {end_date.date()}',
                'generated_at': datetime.now().isoformat(),
                'time_period_days': time_period,
                'overview': overview,
                'customer_segments': customer_segments,
                'purchase_patterns': purchase_patterns,
                'product_analysis': product_analysis
            }
            
            # Save report to file
            report_filename = f'customer_behavior_{datetime.now().strftime("%Y%m%d")}.json'
            with open(os.path.join(self.output_dir, report_filename), 'w') as f:
                json.dump(report, f, indent=2)
            
            self.logger.info(f"Customer behavior report generated: {report_filename}")
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating customer behavior report: {str(e)}")
            raise
    
    def generate_quarterly_comparison_report(self, transaction_data):
        """
        Generate a report comparing the current quarter with the previous quarter
        """
        try:
            # Determine current and previous quarter date ranges
            end_date = transaction_data['purchase_date'].max()
            current_q_start = end_date - pd.Timedelta(days=90)
            prev_q_start = current_q_start - pd.Timedelta(days=90)
            
            # Filter data for each quarter
            current_q_data = transaction_data[
                (transaction_data['purchase_date'] >= current_q_start) & 
                (transaction_data['purchase_date'] <= end_date)
            ]
            
            prev_q_data = transaction_data[
                (transaction_data['purchase_date'] >= prev_q_start) & 
                (transaction_data['purchase_date'] < current_q_start)
            ]
            
            # Generate comparison metrics
            comparison = self._generate_quarterly_comparison(current_q_data, prev_q_data)
            
            # Generate report
            report = {
                'title': f'Quarterly Comparison Report - {prev_q_start.date()} to {end_date.date()}',
                'generated_at': datetime.now().isoformat(),
                'current_quarter': {
                    'start_date': current_q_start.date().isoformat(),
                    'end_date': end_date.date().isoformat()
                },
                'previous_quarter': {
                    'start_date': prev_q_start.date().isoformat(),
                    'end_date': current_q_start.date().isoformat()
                },
                'comparison': comparison
            }
            
            # Save report to file
            report_filename = f'quarterly_comparison_{datetime.now().strftime("%Y%m%d")}.json'
            with open(os.path.join(self.output_dir, report_filename), 'w') as f:
                json.dump(report, f, indent=2)
            
            self.logger.info(f"Quarterly comparison report generated: {report_filename}")
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating quarterly comparison report: {str(e)}")
            raise
    
    def _generate_overview_section(self, transaction_data):
        """
        Generate overview section for the report
        """
        # Calculate key metrics
        total_customers = transaction_data['customer_id'].nunique()
        total_transactions = len(transaction_data)
        total_revenue = transaction_data['amount'].sum()
        avg_order_value = total_revenue / total_transactions
        
        # Calculate monthly trends
        monthly_data = transaction_data.groupby(
            pd.Grouper(key='purchase_date', freq='M')
        ).agg({
            'transaction_id': 'count',
            'customer_id': 'nunique',
            'amount': 'sum'
        }).reset_index()
        
        monthly_data['month'] = monthly_data['purchase_date'].dt.strftime('%Y-%m')
        
        # Format for report
        monthly_trends = [
            {
                'month': row['month'],
                'transactions': int(row['transaction_id']),
                'customers': int(row['customer_id']),
                'revenue': float(row['amount'])
            }
            for _, row in monthly_data.iterrows()
        ]
        
        return {
            'total_customers': total_customers,
            'total_transactions': total_transactions,
            'total_revenue': float(total_revenue),
            'avg_order_value': float(avg_order_value),
            'monthly_trends': monthly_trends
        }
    
    def _generate_segment_section(self, customer_data):
        """
        Generate customer segment
        This is likely the docstring that wasn't properly closed.
        Make sure it ends with triple quotes.
        """