"""
Dashboard Simples para Iniciantes
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 Sales Analytics Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Configurações")

# URL da API (lida da variável de ambiente ou digitada pelo usuário)
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_URL = st.sidebar.text_input("URL da API", value=API_URL)

# Botão de teste de conexão
if st.sidebar.button("🔄 Testar Conexão"):
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            st.sidebar.success("✅ Conectado à API!")
        else:
            st.sidebar.error("❌ Erro na conexão")
    except Exception as e:
        st.sidebar.error(f"❌ Não foi possível conectar: {e}")

st.sidebar.markdown("---")

# Seleção de período
st.sidebar.subheader("📅 Período")
period = st.sidebar.selectbox(
    "Selecionar período",
    ["Últimos 7 dias", "Últimos 15 dias", "Últimos 30 dias"]
)

days_map = {
    "Últimos 7 dias": 7,
    "Últimos 15 dias": 15,
    "Últimos 30 dias": 30
}
days = days_map[period]

# Botão de atualizar
if st.sidebar.button("🔄 Atualizar Dados"):
    st.cache_data.clear()
    st.rerun()

# Funções para carregar dados (com cache)
@st.cache_data(ttl=60)
def load_kpis():
    """Carrega KPIs da API"""
    try:
        response = requests.get(f"{API_URL}/api/v1/kpis", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro na API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao conectar: {e}")
        return None

@st.cache_data(ttl=60)
def load_daily_sales(days):
    """Carrega vendas diárias"""
    try:
        response = requests.get(
            f"{API_URL}/api/v1/sales/daily",
            params={"days": days},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

# Layout principal com abas
tab1, tab2, tab3 = st.tabs(["📈 Visão Geral", "📊 Análise Detalhada", "ℹ️ Sobre"])

with tab1:
    # KPIs principais
    st.subheader("📌 Indicadores de Performance")
    kpis = load_kpis()

    if kpis:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Receita Total", f"R$ {kpis['total_revenue']:,.2f}", f"{kpis['revenue_growth']}%")

        with col2:
            st.metric("Total de Pedidos", f"{kpis['total_orders']:,}", "8.3%")

        with col3:
            st.metric("Ticket Médio", f"R$ {kpis['average_ticket']:,.2f}", "3.2%")

        with col4:
            st.metric("Clientes Ativos", f"{kpis['active_customers']:,}", "15.7%")
    else:
        st.warning("Não foi possível carregar os KPIs. Verifique a conexão com a API.")

    st.markdown("---")

    # Gráfico de vendas diárias
    st.subheader("📅 Vendas Diárias")
    daily_sales = load_daily_sales(days)

    if not daily_sales.empty:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=daily_sales['date'], y=daily_sales['orders'], name='Pedidos', marker_color='lightblue'))
        fig.add_trace(go.Scatter(x=daily_sales['date'], y=daily_sales['revenue'], name='Receita', marker_color='red', line=dict(width=3), yaxis='y2'))

        fig.update_layout(
            title=f'Vendas Diárias - {period}',
            xaxis_title='Data',
            yaxis=dict(title='Número de Pedidos', color='blue'),
            yaxis2=dict(title='Receita (R$)', color='red', overlaying='y', side='right'),
            hovermode='x unified',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem dados de vendas diárias disponíveis")

with tab2:
    st.subheader("📊 Análise Detalhada")
    st.write("### Dados de Vendas")

    try:
        response = requests.get(f"{API_URL}/api/v1/sales", timeout=5)
        if response.status_code == 200:
            sales_data = pd.DataFrame(response.json())
            st.dataframe(
                sales_data,
                column_config={
                    "date": "Data",
                    "product": "Produto",
                    "category": "Categoria",
                    "amount": st.column_config.NumberColumn("Valor Unitário", format="R$ %.2f"),
                    "quantity": "Quantidade"
                },
                hide_index=True,
                use_container_width=True
            )

            st.write("### Estatísticas")
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Média de Valor", f"R$ {sales_data['amount'].mean():.2f}")
            with col2: st.metric("Total de Itens", sales_data['quantity'].sum())
            with col3: st.metric("Produtos Únicos", sales_data['product'].nunique())
    except:
        st.warning("Não foi possível carregar os dados detalhados")

with tab3:
    st.subheader("ℹ️ Sobre o Projeto")
    st.markdown("""
    ### Sales Analytics Platform

    Projeto educacional para demonstrar:
    - **Python**: APIs e dashboards
    - **FastAPI**: APIs REST modernas
    - **Streamlit**: Dashboards interativos
    - **Docker**: Containerização
    - **Boas Práticas**: Código organizado

    ### Como usar
    1. **API**: `http://localhost:8000/docs`
    2. **Dashboard**: Interface gráfica
    3. **Docker**: Todos os serviços em containers
    """)

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: gray;'>
        Dashboard atualizado: {datetime.now().strftime("%d/%m/%Y %H:%M")} | 
        Dados via API: {API_URL}
    </div>
    """,
    unsafe_allow_html=True
)