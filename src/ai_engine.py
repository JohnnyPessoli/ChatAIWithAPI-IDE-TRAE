import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AIEngine:
    def __init__(self, database):
        self.db = database
        
    def process_query(self, query):
        """
        Process natural language query and return response
        
        Args:
            query (str): Natural language query from user
            
        Returns:
            dict: Response with analysis results
        """
        # Get database information to understand the schema
        db_info = self.db.get_database_info()
        
        # Simple keyword-based query processing
        query = query.lower()
        
        # Default response structure
        response = {
            "message": "Análise realizada com sucesso.",
        }
        
        try:
            # Example query handling based on keywords
            if any(word in query for word in ["valioso", "valiosos", "valor", "lucrativos"]):
                response.update(self._analyze_valuable_customers())
                
            elif any(word in query for word in ["padrão", "padrões", "compra", "comportamento"]):
                response.update(self._analyze_purchase_patterns())
                
            elif any(word in query for word in ["probabilidade", "propensos", "próximos"]):
                response.update(self._analyze_purchase_probability())
                
            elif any(word in query for word in ["venda cruzada", "cross-sell", "relacionados"]):
                response.update(self._analyze_cross_sell_opportunities())
                
            else:
                # Generic database summary if no specific query is matched
                response["message"] = "Aqui está um resumo geral do banco de dados."
                response["database_summary"] = self._get_database_summary()
                
        except Exception as e:
            response = {
                "message": f"Ocorreu um erro ao processar sua consulta: {str(e)}",
                "recommendation": "Verifique se o banco de dados contém as tabelas e colunas necessárias para esta análise."
            }
            
        return response
    
    def _get_database_summary(self):
        """Generate a summary of the database"""
        tables = self.db.get_tables()
        summary = []
        
        for table in tables:
            row_count = self.db.get_table_count(table)
            summary.append({
                "table": table,
                "rows": row_count,
                "sample": self.db.get_sample_data(table, 3).to_dict('records')
            })
            
        return summary
    
    def _analyze_valuable_customers(self):
        """Analyze and identify most valuable customers"""
        try:
            # This is a simplified example. In a real application, you would:
            # 1. Check if customer and order tables exist
            # 2. Perform RFM (Recency, Frequency, Monetary) analysis
            
            # Example query assuming a standard e-commerce schema
            query = """
            SELECT 
                c.customer_id,
                c.name,
                COUNT(o.order_id) as order_count,
                SUM(o.total_amount) as total_spent,
                MAX(o.order_date) as last_order_date
            FROM 
                customers c
            JOIN 
                orders o ON c.customer_id = o.customer_id
            GROUP BY 
                c.customer_id, c.name
            ORDER BY 
                total_spent DESC
            LIMIT 10
            """
            
            try:
                top_customers = self.db.execute_query(query)
                
                # Convert to dictionary for JSON response
                customers_list = top_customers.to_dict('records')
                
                return {
                    "message": "Aqui estão os clientes mais valiosos com base no valor total gasto.",
                    "top_customers": customers_list,
                    "recommendation": "Considere criar um programa de fidelidade para estes clientes de alto valor."
                }
                
            except Exception:
                # Fallback if the specific query fails - create simulated data
                return {
                    "message": "Simulação de análise de clientes valiosos (dados de exemplo).",
                    "top_customers": self._generate_sample_valuable_customers(),
                    "recommendation": "Nota: Estes são dados simulados. Configure seu banco de dados com tabelas de clientes e pedidos para análises reais."
                }
                
        except Exception as e:
            return {
                "message": f"Erro ao analisar clientes valiosos: {str(e)}",
                "recommendation": "Verifique se seu banco de dados possui tabelas de clientes e pedidos."
            }
    
    def _analyze_purchase_patterns(self):
        """Analyze customer purchase patterns"""
        try:
            # Simulated data for demonstration
            return {
                "message": "Análise de padrões de compra (dados de exemplo).",
                "patterns": [
                    {"category": "Eletrônicos", "peak_days": "Fim de semana", "avg_order_value": 450.75},
                    {"category": "Roupas", "peak_days": "Segunda e Terça", "avg_order_value": 120.30},
                    {"category": "Alimentos", "peak_days": "Quarta a Sexta", "avg_order_value": 85.50}
                ],
                "recommendation": "Os clientes tendem a comprar eletrônicos nos fins de semana. Considere promoções específicas nesses dias."
            }
        except Exception as e:
            return {
                "message": f"Erro ao analisar padrões de compra: {str(e)}",
                "recommendation": "Verifique se seu banco de dados possui tabelas de pedidos com datas e categorias de produtos."
            }
    
    def _analyze_purchase_probability(self):
        """Analyze purchase probability for customers"""
        try:
            # Simulated data for demonstration
            return {
                "message": "Análise de probabilidade de compra (dados de exemplo).",
                "top_customers": self._generate_sample_purchase_probability(),
                "recommendation": "Envie ofertas personalizadas para os clientes com alta probabilidade de compra nos próximos 30 dias."
            }
        except Exception as e:
            return {
                "message": f"Erro ao analisar probabilidade de compra: {str(e)}",
                "recommendation": "Verifique se seu banco de dados possui histórico de compras de clientes."
            }
    
    def _analyze_cross_sell_opportunities(self):
        """Analyze cross-sell opportunities"""
        try:
            # Simulated data for demonstration
            return {
                "message": "Análise de oportunidades de venda cruzada (dados de exemplo).",
                "cross_sell_pairs": [
                    {"product1": "Smartphone", "product2": "Fones de ouvido", "confidence": 0.78},
                    {"product1": "Laptop", "product2": "Mouse sem fio", "confidence": 0.65},
                    {"product1": "Câmera", "product2": "Cartão de memória", "confidence": 0.82}
                ],
                "recommendation": "Ofereça fones de ouvido com desconto para clientes que compraram smartphones recentemente."
            }
        except Exception as e:
            return {
                "message": f"Erro ao analisar oportunidades de venda cruzada: {str(e)}",
                "recommendation": "Verifique se seu banco de dados possui tabelas de itens de pedido com produtos relacionados."
            }
    
    def _generate_sample_valuable_customers(self):
        """Generate sample data for valuable customers"""
        customers = []
        for i in range(1, 11):
            customers.append({
                "customer_id": f"CUST{i:03d}",
                "name": f"Cliente Exemplo {i}",
                "order_count": np.random.randint(5, 30),
                "total_spent": round(np.random.uniform(1000, 10000), 2),
                "last_order_date": (datetime.now() - timedelta(days=np.random.randint(1, 60))).strftime("%Y-%m-%d")
            })
        
        # Sort by total spent
        customers.sort(key=lambda x: x["total_spent"], reverse=True)
        return customers
    
    def _generate_sample_purchase_probability(self):
        """Generate sample data for purchase probability"""
        customers = []
        for i in range(1, 11):
            # RFM values
            recency_days = np.random.randint(1, 100)
            frequency = np.random.randint(1, 20)
            monetary_value = round(np.random.uniform(100, 2000), 2)
            
            # Simple probability calculation based on RFM
            # Lower recency, higher frequency and monetary value = higher probability
            probability = round(0.9 * (1 - recency_days/100) + 0.05 * (frequency/20) + 0.05 * (monetary_value/2000), 2)
            
            customers.append({
                "customer_id": f"CUST{i:03d}",
                "purchase_probability": probability,
                "recency_days": recency_days,
                "frequency": frequency,
                "monetary_value": monetary_value
            })
        
        # Sort by probability
        customers.sort(key=lambda x: x["purchase_probability"], reverse=True)
        return customers