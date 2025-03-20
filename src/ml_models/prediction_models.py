import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
import joblib
import logging
from datetime import datetime, timedelta

class CustomerPredictionModels:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.purchase_probability_model = None
        self.customer_value_model = None
        self.customer_segment_model = None
        self.product_affinity_model = {}
        
    def train_purchase_probability_model(self, customer_data, transaction_data):
        """
        Train model to predict probability of purchase in next 30 days
        """
        try:
            # Prepare training data
            features, labels = self._prepare_purchase_probability_data(
                customer_data, transaction_data)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                features, labels, test_size=0.2, random_state=42)
            
            # Train model
            self.purchase_probability_model = RandomForestClassifier(
                n_estimators=100, random_state=42)
            self.purchase_probability_model.fit(X_train, y_train)
            
            # Evaluate model
            accuracy = self.purchase_probability_model.score(X_test, y_test)
            self.logger.info(f"Purchase probability model accuracy: {accuracy:.4f}")
            
            return accuracy
            
        except Exception as e:
            self.logger.error(f"Error training purchase probability model: {str(e)}")
            raise
    
    def train_customer_segmentation_model(self, customer_data):
        """
        Train customer segmentation model using K-means clustering
        """
        try:
            # Select features for clustering
            features = customer_data[['recency_scaled', 'frequency_scaled', 'monetary_scaled']]
            
            # Determine optimal number of clusters (simplified)
            n_clusters = 4
            
            # Train K-means model
            self.customer_segment_model = KMeans(n_clusters=n_clusters, random_state=42)
            self.customer_segment_model.fit(features)
            
            # Add cluster labels to customer data
            customer_data['segment'] = self.customer_segment_model.labels_
            
            # Analyze segments
            segment_analysis = customer_data.groupby('segment').agg({
                'recency': 'mean',
                'frequency': 'mean',
                'monetary': 'mean'
            })
            
            self.logger.info(f"Customer segmentation complete. Segments:\n{segment_analysis}")
            
            return segment_analysis
            
        except Exception as e:
            self.logger.error(f"Error training customer segmentation model: {str(e)}")
            raise
    
    def predict_purchase_probability(self, customer_features):
        """
        Predict probability of purchase in next 30 days
        """
        if self.purchase_probability_model is None:
            raise ValueError("Purchase probability model not trained")
            
        probabilities = self.purchase_probability_model.predict_proba(customer_features)
        return probabilities[:, 1]  # Return probability of positive class
    
    def _prepare_purchase_probability_data(self, customer_data, transaction_data):
        """
        Prepare data for purchase probability model
        """
        # Get the latest date in the transaction data
        max_date = transaction_data['purchase_date'].max()
        
        # Define the prediction window (30 days)
        prediction_cutoff = max_date - timedelta(days=30)
        
        # Split transactions into training and label periods
        historical_transactions = transaction_data[
            transaction_data['purchase_date'] <= prediction_cutoff]
        future_transactions = transaction_data[
            transaction_data['purchase_date'] > prediction_cutoff]
        
        # Create features from historical transactions
        features_df = self._create_customer_features(
            customer_data, historical_transactions)
        
        # Create labels: did customer purchase in the next 30 days?
        customers_who_purchased = future_transactions['customer_id'].unique()
        features_df['purchased_next_30d'] = features_df.index.isin(customers_who_purchased)
        
        # Split features and labels
        X = features_df.drop('purchased_next_30d', axis=1)
        y = features_df['purchased_next_30d']
        
        return X, y
    
    def _create_customer_features(self, customer_data, transaction_data):
        """
        Create features for customer prediction models
        """
        # Start with RFM metrics
        features = customer_data.copy()
        
        # Add additional features as needed
        # ...
        
        return features