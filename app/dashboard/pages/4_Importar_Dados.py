import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime
import io

st.set_page_config(page_title="Importar Dados", page_icon="📦", layout="wide")

st.title("Importar Dados de Vendas")
st.markdown("---")

# URL da API (mesma lógica do app.py)
API_URL = os.getenv("API_URL", "http://api:8000")

tab1, tab2, tab3, tab4 = st.tabs(["📁 Upload Arquivo", "✍️ Inserir Manual", "🔌 Integração", "🌐 Webhook"])

with tab1:
    st.subheader("Upload de Arquivo CSV ou Excel")
    arquivo = st.file_uploader(
        "Escolha um arquivo",
        type=["csv", "xlsx", "xls"],
        help="Formatos aceitos: CSV, Excel. O arquivo deve conter as colunas: date, product, category, quantity, amount, customer (opcional)"
    )
    
    if arquivo is not None:
        try:
            # Ler arquivo
            if arquivo.name.endswith(".csv"):
                df = pd.read_csv(arquivo)
            else:
                df = pd.read_excel(arquivo)
            
            st.write("### Prévia dos Dados")
            st.dataframe(df.head(10))
            
            # Verificar colunas obrigatórias
            colunas_obrigatorias = ['date', 'product', 'category', 'quantity', 'amount']
            colunas_faltando = [col for col in colunas_obrigatorias if col not in df.columns]
            
            if colunas_faltando:
                st.error(f"Colunas obrigatórias ausentes: {colunas_faltando}")
            else:
                # Mapeamento de colunas (opcional)
                with st.expander("Mapear colunas (caso os nomes sejam diferentes)"):
                    col_date = st.selectbox("Coluna de Data", df.columns, index=list(df.columns).index('date') if 'date' in df.columns else 0)
                    col_product = st.selectbox("Coluna de Produto", df.columns, index=list(df.columns).index('product') if 'product' in df.columns else 0)
                    col_category = st.selectbox("Coluna de Categoria", df.columns, index=list(df.columns).index('category') if 'category' in df.columns else 0)
                    col_quantity = st.selectbox("Coluna de Quantidade", df.columns, index=list(df.columns).index('quantity') if 'quantity' in df.columns else 0)
                    col_amount = st.selectbox("Coluna de Valor Unitário", df.columns, index=list(df.columns).index('amount') if 'amount' in df.columns else 0)
                    col_customer = st.selectbox("Coluna de Cliente (opcional)", ['Nenhum'] + list(df.columns))
                
                if st.button("📥 Importar Dados", type="primary"):
                    registros = []
                    for _, row in df.iterrows():
                        registro = {
                            "date": str(row[col_date]),
                            "product": str(row[col_product]),
                            "category": str(row[col_category]),
                            "quantity": int(row[col_quantity]),
                            "amount": float(row[col_amount])
                        }
                        if col_customer != 'Nenhum':
                            registro["customer"] = str(row[col_customer])
                        registros.append(registro)
                    
                    with st.spinner("Importando..."):
                        try:
                            response = requests.post(
                                f"{API_URL}/api/v1/sales/batch",
                                json=registros,
                                timeout=30
                            )
                            if response.status_code == 200:
                                st.success(f"✅ {len(registros)} registros importados!")
                                st.balloons()
                                # Limpar cache do dashboard e recarregar para mostrar dados atualizados
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error(f"Erro na API: {response.text}")
                        except Exception as e:
                            st.error(f"Erro de conexão: {e}")
        except Exception as e:
            st.error(f"Erro ao ler arquivo: {e}")

with tab2:
    st.subheader("Inserir Venda Manualmente")
    with st.form("manual_form"):
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input("Data", datetime.now())
            produto = st.text_input("Produto")
            categoria = st.text_input("Categoria")
        with col2:
            quantidade = st.number_input("Quantidade", min_value=1, value=1)
            valor = st.number_input("Valor Unitário (R$)", min_value=0.01, value=10.00, format="%.2f")
            cliente = st.text_input("Cliente (opcional)")
        
        submitted = st.form_submit_button("➕ Adicionar Venda")
        if submitted:
            if not produto or not categoria:
                st.error("Preencha produto e categoria.")
            else:
                registro = {
                    "date": str(data),
                    "product": produto,
                    "category": categoria,
                    "quantity": quantidade,
                    "amount": valor
                }
                if cliente:
                    registro["customer"] = cliente
                
                try:
                    response = requests.post(f"{API_URL}/api/v1/sales", json=registro, timeout=5)
                    if response.status_code == 200:
                        st.success("✅ Venda adicionada!")
                        # Limpar cache e recarregar
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Erro: {response.text}")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")

with tab3:
    st.subheader("Integração com APIs Externas (em breve)")
    st.info("Funcionalidade em desenvolvimento: integração com Shopify, Mercado Livre, etc.")

with tab4:
    st.subheader("Webhook para receber dados automáticos (em breve)")
    st.info("Funcionalidade em desenvolvimento: configure um endpoint para receber dados via webhook.")