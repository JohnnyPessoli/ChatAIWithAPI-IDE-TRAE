import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import logging

class DataPreprocessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.encoders = {}
        self.scalers = {}
        
    def preprocess_transaction_data(self, transaction_df):
        """
        Preprocess transaction data for analysis
        """
        try:
            # Convert date columns
            transaction_df['purchase_date'] = pd.to_datetime(transaction_df['purchase_date'])
            
            # Extract time features
            transaction_df['day_of_week'] = transaction_df['purchase_date'].dt.dayofweek
            transaction_df['month'] = transaction_df['purchase_date'].dt.month
            transaction_df['hour'] = transaction_df['purchase_date'].dt.hour
            
            # Calculate recency, frequency, monetary metrics per customer
            rfm_data = self._calculate_rfm(transaction_df)
            
            # Process channel data
            if 'channel' in transaction_df.columns:
                channel_encoded = self._encode_categorical_feature(transaction_df, 'channel')
                rfm_data = pd.concat([rfm_data, channel_encoded], axis=1)
            
            return rfm_data
            
        except Exception as e:
            self.logger.error(f"Error preprocessing transaction data: {str(e)}")
            raise
    
    def _calculate_rfm(self, transaction_df):
        """
        Calculate Recency, Frequency, Monetary metrics
        """
        # Current date for recency calculation
        current_date = transaction_df['purchase_date'].max() + pd.Timedelta(days=1)
        
        # Group by customer
        customer_data = transaction_df.groupby('customer_id').agg({
            'purchase_date': lambda x: (current_date - x.max()).days,  # Recency
            'transaction_id': 'count',  # Frequency
            'amount': 'sum'  # Monetary
        }).rename(columns={
            'purchase_date': 'recency',
            'transaction_id': 'frequency',
            'amount': 'monetary'
        })
        
        # Scale RFM values
        for column in ['recency', 'frequency', 'monetary']:
            if column not in self.scalers:
                self.scalers[column] = StandardScaler()
                customer_data[f'{column}_scaled'] = self.scalers[column].fit_transform(
                    customer_data[[column]])
            else:
                customer_data[f'{column}_scaled'] = self.scalers[column].transform(
                    customer_data[[column]])
        
        return customer_data
    
    def _encode_categorical_feature(self, df, feature_name):
        """
        One-hot encode categorical features
        """
        if feature_name not in self.encoders:
            self.encoders[feature_name] = OneHotEncoder(sparse=False, handle_unknown='ignore')
            encoded_data = self.encoders[feature_name].fit_transform(df[[feature_name]])
        else:
            encoded_data = self.encoders[feature_name].transform(df[[feature_name]])
            
        # Create DataFrame with encoded values
        feature_names = [f"{feature_name}_{cat}" for cat in 
                         self.encoders[feature_name].categories_[0]]
        encoded_df = pd.DataFrame(encoded_data, columns=feature_names, index=df.index)
        
        # Group by customer_id if needed
        if 'customer_id' in df.columns:
            encoded_df['customer_id'] = df['customer_id']
            encoded_df = encoded_df.groupby('customer_id').mean()
            
        return encoded_df