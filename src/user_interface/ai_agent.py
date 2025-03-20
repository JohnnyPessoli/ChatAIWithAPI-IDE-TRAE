import logging
from datetime import datetime
import json

class CustomerBehaviorAIAgent:
    def __init__(self, data_collector, data_preprocessor, prediction_models, 
                 trend_analyzer, insights_generator, report_generator):
        self.data_collector = data_collector
        self.data_preprocessor = data_preprocessor
        self.prediction_models = prediction_models
        self.trend_analyzer = trend_analyzer
        self.insights_generator = insights_generator
        self.report_generator = report_generator
        self.logger = logging.getLogger(__name__)
        
        # Pre-defined prompts by category
        self.predefined_prompts = {
            'prediction_trends': [
                "Quais clientes têm maior probabilidade de fazer uma nova compra nos próximos 30 dias?",
                "Quais produtos/serviços estão mais propensos a serem comprados nos próximos meses?",
                "Que padrões de compra emergentes podemos observar com base nos últimos 6 meses?"
            ],
            'customer_segmentation': [
                "Quais são os clientes mais valiosos (com maior ticket médio e recorrência)?",
                "Quais clientes reduziram significativamente suas compras nos últimos 3 meses?",
                "Quais são os clientes inativos que podem ser reativados com uma campanha especial?"
            ],
            'sales_marketing': [
                "Quais canais de aquisição estão gerando os clientes mais fiéis e lucrativos?",
                "Qual é o melhor momento para oferecer promoções com base no comportamento de compra?",
                "Que tipo de oferta personalizada pode aumentar a conversão de clientes indecisos?"
            ],
            'reports_analysis': [
                "Gere um relatório detalhado sobre o comportamento de compra nos últimos 12 meses.",
                "Crie uma comparação entre os padrões de compra deste trimestre e do trimestre anterior.",
                "Quais são os principais fatores que influenciam a decisão de compra dos clientes?"
            ]
        }
        
        # Initialize data
        self.customer_data = None
        self.transaction_data = None
        self.last_data_update = None
    
    def initialize(self, force_refresh=False):
        """
        Initialize the AI agent by loading and processing data
        """
        try:
            # Check if we need to refresh data
            if self.customer_data is None or self.transaction_data is None or force_refresh:
                self.logger.info("Initializing AI agent with fresh data")
                
                # Collect data
                self.transaction_data = self.data_collector.collect_transaction_data(time_period=365)
                self.customer_data = self.data_collector.collect_customer_data()
                
                # Preprocess data
                self.customer_data = self.data_preprocessor.preprocess_transaction_data(self.transaction_data)
                
                # Train models
                self.prediction_models.train_purchase_probability_model(
                    self.customer_data, self.transaction_data)
                self.prediction_models.train_customer_segmentation_model(self.customer_data)
                
                self.last_data_update = datetime.now()
                self.logger.info("AI agent initialized successfully")
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing AI agent: {str(e)}")
            raise
    
    def process_query(self, query):
        """
        Process a user query and return appropriate response
        """
        try:
            # Ensure data is initialized
            if self.customer_data is None or self.transaction_data is None:
                self.initialize()
            
            # Check if we need to refresh data (e.g., if it's more than a day old)
            if (datetime.now() - self.last_data_update).days >= 1:
                self.logger.info("Refreshing data due to age")
                self.initialize(force_refresh=True)
            
            # Process the query based on its content
            response = self._analyze_query(query)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return {
                "error": f"Failed to process query: {str(e)}",
                "success": False
            }
    
    def get_suggested_prompts(self, category=None):
        """
        Return suggested prompts for the user
        """
        if category and category in self.predefined_prompts:
            return self.predefined_prompts[category]
        else:
            # Return all prompts organized by category
            return self.predefined_prompts
    
    def _analyze_query(self, query):
        """
        Analyze the query and route to appropriate handler
        """
        query = query.lower()
        
        # Purchase likelihood queries
        if "probabilidade" in query and "compra" in query and "30 dias" in query:
            return self._handle_purchase_likelihood_query()
        
        # Product trend queries
        elif "produtos" in query and ("tendências" in query or "propensos" in query):
            return self._handle_product_trend_query()
        
        # Customer segmentation queries
        elif "clientes" in query and ("valiosos" in query or "ticket médio" in query):
            return self._handle_valuable_customers_query()
        elif "clientes" in query and "reduziram" in query:
            return self._handle_declining_customers_query()
        elif "clientes" in query and "inativos" in query:
            return self._handle_inactive_customers_query()
        
        # Channel performance queries
        elif "canais" in query and "aquisição" in query:
            return self._handle_channel_performance_query()
        
        # Purchase timing queries
        elif "melhor momento" in query and "promoções" in query:
            return self._handle_purchase_timing_query()
        
        # Report generation queries
        elif "relatório" in query and "12 meses" in query:
            return self._handle_annual_report_query()
        elif "comparação" in query and "trimestre" in query:
            return self._handle_quarterly_comparison_query()
        
        # Emerging patterns query
        elif "padrões" in query and "emergentes" in query:
            return self._handle_emerging_patterns_query()
        
        # Fallback for unrecognized queries
        else:
            return {
                "message": "Não consegui entender completamente sua consulta. Por favor, tente reformular ou escolha uma das sugestões de prompts.",
                "suggested_prompts": self.get_suggested_prompts(),
                "success": True
            }
    
    def _handle_purchase_likelihood_query(self):
        """
        Handle query about customers likely to purchase
        """
        insights, high_probability_customers = self.insights_generator.generate_purchase_likelihood_insights(
            self.customer_data, self.transaction_data)
        
        # Format the response
        top_customers = high_probability_customers.head(10).reset_index()
        
        customer_list = [
            {
                "customer_id": row['customer_id'],
                "purchase_probability": float(row['purchase_probability']),
                "recency_days": int(row['recency']),
                "frequency": int(row['frequency']),
                "monetary_value": float(row['monetary'])
            }
            for _, row in top_customers.iterrows()
        ]
        
        return {
            "message": f"Identifiquei {insights['customers_above_threshold']} clientes com alta probabilidade (>70%) de fazer uma compra nos próximos 30 dias.",
            "top_customers": customer_list,
            "avg_purchase_probability": float(insights['avg_purchase_probability']),
            "recommendation": "Recomendo focar em campanhas personalizadas para estes clientes de alta probabilidade, oferecendo produtos complementares aos que já compraram.",
            "success": True
        }
    
    def _handle_product_trend_query(self):
        """
        Handle query about product trends
        """
        product_insights = self.insights_generator.generate_product_trend_insights(self.transaction_data)
        
        return {
            "message": "Análise de tendências de produtos concluída.",
            "trending_products": product_insights['top_trending_products'][:5],
            "declining_products": product_insights['declining_products'][:5],
            "recommendation": "Recomendo aumentar o estoque e visibilidade dos produtos em alta, e considerar promoções para os produtos em queda.",
            "success": True
        }