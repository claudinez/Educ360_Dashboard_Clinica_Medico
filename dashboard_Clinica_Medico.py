# =======================================================
# 🩺 Painel de Consultas Médicas
# Desenvolvido por Claudinez | Python + Streamlit + Plotly
# =======================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime, date
# Removido componente externo não utilizado

# -------------------------
# 🎨 Configuração da página e tema
# -------------------------
st.set_page_config(
    page_title="Painel de Consultas Médicas",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema de cores suaves
# 🌙 Estilo personalizado para modo escuro
st.markdown("""
<style>
/* ===========================================
   🎨 AJUSTE DE CAMPOS DE SELEÇÃO E DATA
   =========================================== */
div[data-baseweb="select"] > div {
    background-color: #1e1e1e !important;
    color: #fafafa !important;
    border-radius: 8px;
    border: 1px solid #444 !important;
}

ul[data-baseweb="menu"] {
    background-color: #1e1e1e !important;
    color: #fafafa !important;
}

li[data-baseweb="option"] {
    background-color: #1e1e1e !important;
    color: #fafafa !important;
}

li[data-baseweb="option"]:hover {
    background-color: #333 !important;
}

div[data-baseweb="datepicker"] {
    background-color: #1e1e1e !important;
    color: #fafafa !important;
}

input[type="text"], input[type="date"] {
    background-color: #1e1e1e !important;
    color: #fafafa !important;
    border: 1px solid #444 !important;
}

::placeholder {
    color: #ccc !important;
    opacity: 0.7 !important;
}

/* ===========================================
   💳 ESTILO DOS CARDS DE MÉTRICAS
   =========================================== */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1e1e1e, #151515);
    border: 1px solid #3a3a3a;
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 4px 20px rgba(0, 255, 127, 0.1);
    text-align: center;
    transition: all 0.3s ease-in-out;
}

/* Efeito hover */
div[data-testid="stMetric"]:hover {
    box-shadow: 0 0 25px rgba(0, 255, 127, 0.3);
    transform: translateY(-4px);
}

/* Rótulo das métricas */
[data-testid="stMetricLabel"] {
    color: #d3d3d3 !important;
    font-weight: 600;
    text-align: center;
    font-size: 16px;
    margin-bottom: 8px;
}

/* Valor principal */
[data-testid="stMetricValue"] {
    color: #90EE90 !important;
    font-size: 30px;
    font-weight: bold;
}

/* Espaçamento entre os 3 cards */
section[data-testid="stHorizontalBlock"] {
    gap: 25px !important;
}
</style>
""", unsafe_allow_html=True)


st.title("🩺 Painel de Consultas Médicas")
st.write("Visualize o desempenho de consultas, faturamento e especialidades de forma interativa e intuitiva.")

# -------------------------
# 📂 Carregar dados
# -------------------------
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados/consultas_medico_especialidade.csv")
    df["dataconsulta"] = pd.to_datetime(df["dataconsulta"], errors="coerce")
    return df.dropna(subset=["dataconsulta"])

df = carregar_dados()

# -------------------------
# 🎛️ Filtros
# -------------------------
st.sidebar.header("🎚️ Filtros")

min_date = df["dataconsulta"].min().date()
max_date = df["dataconsulta"].max().date()

# Seleção por calendário (mais intuitivo). O formato exibido segue o locale do navegador.
# 📅 Forçar formato brasileiro (DD/MM/AAAA)
# O parâmetro format="DD/MM/YYYY" foi adicionado para exibir corretamente no Streamlit
data_range = st.sidebar.date_input(
    "Período (DD/MM/AAAA)",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    format="DD/MM/YYYY"
)

# Garantir que sempre tenha dois valores e tratar fim vazio
if data_range is None:
    data_inicial, data_final = min_date, max_date
elif isinstance(data_range, (list, tuple)):
    if len(data_range) == 2 and all(d is not None for d in data_range):
        data_inicial, data_final = data_range
    elif len(data_range) >= 1 and data_range[0] is not None:
        data_inicial = data_range[0]
        data_final = data_range[0]
    else:
        data_inicial, data_final = min_date, max_date
else:
    data_inicial = data_range
    data_final = data_range

# Resumo do período no padrão brasileiro
st.sidebar.info(
    f"Período selecionado: {pd.to_datetime(data_inicial).strftime('%d/%m/%Y')} — {pd.to_datetime(data_final).strftime('%d/%m/%Y')}"
)

# Multiselects
unidades = st.sidebar.multiselect("Unidades", df["unidade"].unique(), default=list(df["unidade"].unique()))
especialidades = st.sidebar.multiselect("Especialidades", df["tipoconsulta"].unique(), default=list(df["tipoconsulta"].unique()))

# -------------------------
# 🔍 Aplicar filtros
# -------------------------
df_filtrado = df[
    (df["dataconsulta"].dt.date >= data_inicial) &
    (df["dataconsulta"].dt.date <= data_final) &
    (df["unidade"].isin(unidades)) &
    (df["tipoconsulta"].isin(especialidades))
]

# -------------------------
# ⚠️ Tratamento de dataset vazio
# -------------------------
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados. Ajuste os parâmetros e tente novamente.")
    st.stop()

# Versões para exibição/exportação com data formatada
df_view = df_filtrado.copy()
df_view["dataconsulta"] = df_view["dataconsulta"].dt.strftime("%d/%m/%Y")

# -------------------------
# 📈 Métricas principais
# -------------------------
col1, col2, col3 = st.columns(3)
col1.metric("💰 Faturamento Total", f"R$ {df_filtrado['valor'].sum():,.2f}")
col2.metric("📋 Total de Consultas", f"{df_filtrado.shape[0]}")
col3.metric("⚖️ Valor Médio", f"R$ {df_filtrado['valor'].mean():.2f}")

st.divider()

# -------------------------
# 📤 Botão de Exportação
# -------------------------
csv = df_filtrado.to_csv(index=False).encode("utf-8")
st.download_button(
    label="💾 Baixar dados filtrados (CSV)",
    data=df_view.to_csv(index=False).encode("utf-8"),
    file_name="consultas_filtradas.csv",
    mime="text/csv"
)

# Exibir tabela opcional com datas no padrão brasileiro
if st.sidebar.checkbox("Mostrar dados filtrados (DD/MM/AAAA)", value=False):
    st.subheader("📄 Dados filtrados")
    st.dataframe(df_view, width='stretch')

st.divider()

# ===============================
# 🎨  📊 Gráficos lado a lado
# ===============================

# Paleta de cores suaves
cores = ['#4C78A8', '#72B7B2', '#F58518', '#E45756', '#54A24B', '#EECA3B']

# --- 1️⃣ Consultas por Unidade (Gráfico de Barras)
consultas_unidade = df_filtrado.groupby("unidade")["valor"].sum().reset_index()
fig_bar = px.bar(
    consultas_unidade,
    x="unidade",
    y="valor",
    text="valor",
    color="unidade",
    color_discrete_sequence=cores,
    title="🏥 Consultas por Unidade"
)
fig_bar.update_traces(texttemplate="R$ %{text:.2s}", textposition="outside")
fig_bar.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="#fafafa",
    showlegend=False,
     margin=dict(t=80, b=40),    # ⬅️ margem superior extra
    yaxis=dict(showgrid=False, automargin=True)
)

# --- 2️⃣ Distribuição de Especialidades (Gráfico de Pizza)
consultas_tipo = df_filtrado.groupby("tipoconsulta").size().reset_index(name="Total")
fig_pie = px.pie(
    consultas_tipo,
    names="tipoconsulta",
    values="Total",
    color_discrete_sequence=cores,
    title="🩺 Distribuição de Especialidades"
)
fig_pie.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="#fafafa"
)

# --- Layout lado a lado
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.plotly_chart(fig_pie, use_container_width=True)


# 3️⃣ Faturamento por Médico
faturamento_medico = df_filtrado.groupby("medico")["valor"].sum().reset_index()
fig3 = px.bar(
    faturamento_medico,
    x="medico", y="valor",
    title="💵 Faturamento por Médico",
    text_auto=True,
    color_discrete_sequence=["#66cc99"]
)
st.plotly_chart(fig3, use_container_width=True)

# 4️⃣ Evolução Temporal
consultas_data = df_filtrado.groupby("dataconsulta").size().reset_index(name="Total")
fig4 = px.line(
    consultas_data,
    x="dataconsulta", y="Total",
    markers=True,
    title="📆 Evolução de Consultas ao Longo do Tempo",
    color_discrete_sequence=["#0099cc"]
)
fig4.update_xaxes(tickformat="%d/%m/%Y")
fig4.update_traces(hovertemplate="Data: %{x|%d/%m/%Y}<br>Total: %{y}")
st.plotly_chart(fig4, use_container_width=True)

# 5️⃣ Relação entre Valor e Retornos
fig5 = px.scatter(
    df_filtrado,
    x="valor", y="retornodaconsulta",
    color="tipoconsulta",
    hover_data=["medico", "unidade"],
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title="🔁 Relação entre Valor da Consulta e Retornos"
)
st.plotly_chart(fig5, use_container_width=True)

# -------------------------
# 📄 Rodapé
# -------------------------
st.markdown("""
---
👨‍⚕️ **Painel desenvolvido por Claudinez**
💻 Tecnologias: *Python, Pandas, Streamlit, Plotly*
🎨 Tema suave, gráficos verticais e design responsivo.
""")
