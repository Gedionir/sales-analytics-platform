"""
API Simples para aprendizado
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import random
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar app FastAPI
app = FastAPI(
    title="Sales Analytics API",
    description="API para dados de vendas",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de dados
class SaleItem(BaseModel):
    date: str
    product: str
    category: str
    amount: float
    quantity: int
    customer: Optional[str] = None

class KPIResponse(BaseModel):
    total_revenue: float
    total_orders: int
    average_ticket: float
    active_customers: int
    revenue_growth: float

# Dados de exemplo (simulando banco de dados)
SALES_DATA = [
    {"date": "2024-01-01", "product": "Notebook", "category": "Eletrônicos", "amount": 3500.00, "quantity": 2, "customer": "João"},
    {"date": "2024-01-01", "product": "Mouse", "category": "Eletrônicos", "amount": 150.00, "quantity": 5, "customer": "Maria"},
    {"date": "2024-01-02", "product": "Teclado", "category": "Eletrônicos", "amount": 250.00, "quantity": 3, "customer": "José"},
    {"date": "2024-01-02", "product": "Monitor", "category": "Eletrônicos", "amount": 1200.00, "quantity": 1, "customer": "Ana"},
    {"date": "2024-01-03", "product": "Cadeira", "category": "Móveis", "amount": 800.00, "quantity": 2, "customer": "Carlos"},
]

@app.get("/")
def root():
    """Rota inicial"""
    return {
        "message": "Bem-vindo à API de Análise de Vendas",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/api/v1/kpis",
            "/api/v1/sales",
            "/api/v1/sales/daily",
            "/api/v1/sales/by-category",
            "/api/v1/sales/batch"
        ]
    }

@app.get("/health")
def health_check():
    """Verificar se a API está funcionando"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "connected",
            "redis": "connected"
        }
    }

@app.get("/api/v1/kpis", response_model=KPIResponse)
def get_kpis():
    """Retorna KPIs principais"""
    logger.info("Buscando KPIs...")
    
    total_revenue = sum(item["amount"] * item["quantity"] for item in SALES_DATA)
    total_orders = len(SALES_DATA)
    
    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "average_ticket": round(total_revenue / total_orders, 2) if total_orders else 0,
        "active_customers": 150,
        "revenue_growth": 12.5
    }

@app.get("/api/v1/sales", response_model=List[SaleItem])
def get_all_sales():
    """Retorna todas as vendas"""
    return SALES_DATA

@app.get("/api/v1/sales/daily")
def get_daily_sales(days: int = 7):
    """
    Retorna vendas diárias dos últimos N dias
    """
    try:
        end_date = datetime.now()
        dates = [(end_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
        dates.reverse()
        
        daily_data = []
        for date in dates:
            day_sales = [s for s in SALES_DATA if s["date"] == date]
            
            if day_sales:
                revenue = sum(s["amount"] * s["quantity"] for s in day_sales)
                orders = len(day_sales)
            else:
                revenue = random.uniform(1000, 5000)
                orders = random.randint(5, 20)
            
            daily_data.append({
                "date": date,
                "revenue": round(revenue, 2),
                "orders": orders
            })
        
        return daily_data
        
    except Exception as e:
        logger.error(f"Erro ao buscar vendas diárias: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/api/v1/sales/by-category")
def sales_by_category():
    """Vendas agrupadas por categoria"""
    categories = {}
    
    for sale in SALES_DATA:
        cat = sale["category"]
        if cat not in categories:
            categories[cat] = {
                "category": cat,
                "revenue": 0,
                "quantity": 0
            }
        categories[cat]["revenue"] += sale["amount"] * sale["quantity"]
        categories[cat]["quantity"] += sale["quantity"]
    
    return list(categories.values())

@app.post("/api/v1/sales/batch", response_model=dict)
async def import_sales_batch(sales: List[SaleItem]):
    """
    Importa múltiplas vendas em lote.
    """
    try:
        # Adicionar à lista em memória (simulando banco de dados)
        for item in sales:
            nova_venda = item.dict()
            SALES_DATA.append(nova_venda)
            logger.info(f"Venda adicionada: {nova_venda}")
        
        logger.info(f"Total de {len(sales)} vendas importadas com sucesso.")
        return {"message": "Dados importados com sucesso", "count": len(sales)}
        
        # Em produção, substitua o loop acima por inserção no banco real:
        # db = SessionLocal()
        # for item in sales:
        #     sale = Sale(**item.dict())
        #     db.add(sale)
        # db.commit()
        # db.close()
        
    except Exception as e:
        logger.error(f"Erro na importação em lote: {e}")
        raise HTTPException(status_code=500, detail=str(e))