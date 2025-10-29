# =======================================================
# 🩺 Painel de Consultas Médicas
# Desenvolvido por Claudinez | Python + Streamlit + Plotly
# =======================================================

import streamlit as st
import pandas as pd
import plotly.express as px

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
st.markdown(
    """
    <style>
    /* Fundo geral */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }

    /* Títulos e textos */
    h1, h2, h3, h4, p, span, div {
        color: #e8e8e8 !important;
    }

    /* Container dos cards de métricas */
    div[data-testid="stMetric"] {
        background-color: #1e1e1e;
        border-radius: 15px;
        padding: 20px;
        text-align: center;              /* ✅ Centraliza o conteúdo */
        box-shadow: 0 0 10px rgba(0, 255, 127, 0.2);
        display: flex;
        flex-direction: column;
        align-items: center;             /* ✅ Centraliza horizontalmente */
        justify-content: center;         /* ✅ Centraliza verticalmente */
        height: 100%;
    }

    /* Rótulo (título pequeno) */
    [data-testid="stMetricLabel"] {
        color: #d3d3d3 !important;
        text-align: center;              /* ✅ Centraliza o texto do rótulo */
        font-weight: 600;
    }

    /* Valor numérico */
    [data-testid="stMetricValue"] {
        color: #90EE90 !important;       /* Verde suave */
        text-align: center;              /* ✅ Centraliza valor */
        font-size: 28px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)



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

# Intervalo de datas
data_range = st.sidebar.date_input("Período", [min_date, max_date])
if len(data_range) == 2:
    data_inicial, data_final = data_range
else:
    data_inicial, data_final = min_date, max_date

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
    data=csv,
    file_name="consultas_filtradas.csv",
    mime="text/csv"
)

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
