"""
Script para popular banco de dados com dados iniciais
"""

import psycopg2
from datetime import datetime, timedelta
import random

def init_database():
    """Inicializa banco de dados com dados de exemplo"""
    
    # Conectar ao PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        database="sales_db",
        user="admin",
        password="admin123",
        port="5432"
    )
    
    cursor = conn.cursor()
    
    # Criar tabelas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            category VARCHAR(50),
            price DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER,
            total_amount DECIMAL(10,2),
            sale_date DATE,
            customer_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Inserir produtos de exemplo
    products = [
        ("Notebook Dell", "Eletrônicos", 3500.00),
        ("Mouse Logitech", "Eletrônicos", 150.00),
        ("Teclado Mecânico", "Eletrônicos", 250.00),
        ("Monitor LG", "Eletrônicos", 1200.00),
        ("Cadeira Gamer", "Móveis", 800.00),
        ("Mesa Escritório", "Móveis", 450.00),
        ("Smartphone Samsung", "Eletrônicos", 2500.00),
        ("Fone Bluetooth", "Eletrônicos", 200.00),
        ("Webcam HD", "Eletrônicos", 300.00),
        ("Impressora", "Eletrônicos", 600.00)
    ]
    
    for product in products:
        cursor.execute(
            "INSERT INTO products (name, category, price) VALUES (%s, %s, %s)",
            product
        )
    
    # Inserir vendas de exemplo (últimos 30 dias)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    current_date = start_date
    while current_date <= end_date:
        # Gerar 5-20 vendas por dia
        num_sales = random.randint(5, 20)
        
        for _ in range(num_sales):
            product_id = random.randint(1, 10)
            quantity = random.randint(1, 5)
            
            # Buscar preço do produto
            cursor.execute("SELECT price FROM products WHERE id = %s", (product_id,))
            price = cursor.fetchone()[0]
            
            total_amount = price * quantity
            customer_id = random.randint(1, 100)
            
            cursor.execute("""
                INSERT INTO sales (product_id, quantity, total_amount, sale_date, customer_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (product_id, quantity, total_amount, current_date.date(), customer_id))
        
        current_date += timedelta(days=1)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("✅ Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_database()