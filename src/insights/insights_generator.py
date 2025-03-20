import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import json

class InsightsGenerator:
    def __init__(self, prediction_models, trend_analyzer):
        self.prediction_models = prediction_models
        self.trend_analyzer = trend_analyzer
        self.logger = logging.getLogger(__name__)
    
    def generate_purchase_likelihood_insights(self, customers, threshold=0.7):
        """
        Generate insights about customers with high purchase likelihood
        
        Args:
            customers (list): List of customer data
            threshold (float): Probability threshold for high likelihood
            
        Returns:
            dict: Insights about high-likelihood customers
        """
        try:
            self.logger.info(f"Generating purchase likelihood insights with threshold {threshold}")
            
            # Convert customers to DataFrame if it's not already
            if not isinstance(customers, pd.DataFrame):
                customers_df = pd.DataFrame(customers)
            else:
                customers_df = customers
            
            # Get purchase probabilities for each customer
            probabilities = self.prediction_models.predict_purchase_probability(customers_df)
            
            # Identify high-likelihood customers
            high_likelihood = customers_df[probabilities >= threshold].copy()
            high_likelihood['purchase_probability'] = probabilities[probabilities >= threshold]
            
            # Calculate percentage of customers with high purchase likelihood
            percentage = len(high_likelihood) / len(customers_df) * 100 if len(customers_df) > 0 else 0
            
            # Get common characteristics of high-likelihood customers
            characteristics = self._extract_common_characteristics(high_likelihood)
            
            # Generate recommended actions
            actions = self._generate_actions_for_high_likelihood(high_likelihood)
            
            # Prepare insights
            insights = {
                'high_likelihood_customers': high_likelihood.to_dict('records'),
                'count': len(high_likelihood),
                'percentage': percentage,
                'common_characteristics': characteristics,
                'recommended_actions': actions,
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"Generated insights for {len(high_likelihood)} high-likelihood customers")
            return insights
            
        except Exception as e:
            self.logger.error(f"Error generating purchase likelihood insights: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _extract_common_characteristics(self, customer_group):
        """
        Extract common characteristics from a group of customers
        
        Args:
            customer_group (DataFrame): Group of customers to analyze
            
        Returns:
            dict: Common characteristics
        """
        if len(customer_group) == 0:
            return {}
        
        characteristics = {}
        
        # Analyze demographic data if available
        if 'age' in customer_group.columns:
            characteristics['avg_age'] = customer_group['age'].mean()
            characteristics['age_range'] = [customer_group['age'].min(), customer_group['age'].max()]
        
        if 'gender' in customer_group.columns:
            gender_counts = customer_group['gender'].value_counts(normalize=True) * 100
            characteristics['gender_distribution'] = gender_counts.to_dict()
        
        # Analyze purchase behavior
        if 'purchase_frequency' in customer_group.columns:
            characteristics['avg_purchase_frequency'] = customer_group['purchase_frequency'].mean()
        
        if 'avg_order_value' in customer_group.columns:
            characteristics['avg_order_value'] = customer_group['avg_order_value'].mean()
        
        if 'last_purchase_date' in customer_group.columns:
            characteristics['avg_days_since_purchase'] = (
                datetime.now() - pd.to_datetime(customer_group['last_purchase_date'])
            ).mean().days
        
        return characteristics
    
    def _generate_actions_for_high_likelihood(self, high_likelihood_customers):
        """
        Generate recommended actions for high likelihood customers
        
        Args:
            high_likelihood_customers (DataFrame): High likelihood customers
            
        Returns:
            list: Recommended actions
        """
        actions = []
        
        if len(high_likelihood_customers) > 0:
            # Add personalized email campaign action
            actions.append({
                'action': 'Send personalized email campaign',
                'description': 'Target these high-likelihood customers with personalized offers based on their past purchases',
                'priority': 'High'
            })
            
            # Add special discount action
            actions.append({
                'action': 'Offer time-limited discount',
                'description': 'Create urgency with a special time-limited discount for these customers',
                'priority': 'Medium'
            })
            
            # Add product recommendation action
            actions.append({
                'action': 'Provide personalized product recommendations',
                'description': 'Use purchase history to recommend complementary products',
                'priority': 'Medium'
            })
            
            # Add loyalty program action
            actions.append({
                'action': 'Invite to loyalty program',
                'description': 'For high-value customers, consider inviting them to an exclusive loyalty program',
                'priority': 'Low'
            })
        
        return actions