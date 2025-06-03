import streamlit as st
import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt
from datetime import date

# ==== CONFIG ====
db_dir = os.path.join(os.path.dirname(__file__), "db")
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "diario_bordo.db")

st.set_page_config(page_title="📒 Diário de Bordo da Fazenda", layout="wide")

# ==== CUSTO/HORA DOS OPERADORES ====
CUSTO_HORA_OPERADOR = {
    "João": 25.0,
    "Maria": 30.0,
    "Carlos": 28.5,
    "Equipe Temporária": 22.0
}

# ==== BANCO DE DADOS ====
def criar_tabela():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Verifica se a tabela existe
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='atividades'")
    if c.fetchone():
        # Verifica colunas e adiciona se necessário
        c.execute("PRAGMA table_info(atividades)")
        colunas_existentes = [col[1] for col in c.fetchall()]
        colunas_necessarias = [
            ("maquina", "TEXT"),
            ("custo_hora", "REAL"),
            ("custo_estimado", "REAL"),
            ("insumo_qtd", "REAL"),
            ("insumo_nome", "TEXT")
        ]
        for nome_coluna, tipo_coluna in colunas_necessarias:
            if nome_coluna not in colunas_existentes:
                c.execute(f"ALTER TABLE atividades ADD COLUMN {nome_coluna} {tipo_coluna}")
    else:
        c.execute('''
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                operador TEXT,
                atividade TEXT,
                talhao TEXT,
                maquina TEXT,
                horas REAL,
                custo_hora REAL,
                custo_estimado REAL,
                insumo_qtd REAL,
                insumo_nome TEXT,
                observacoes TEXT
            )
        ''')
    conn.commit()
    conn.close()
    

def inserir_registro(data, operador, atividade, talhao, maquina, horas, custo_hora, custo_estimado, insumo_qtd, insumo_nome, observacoes):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO atividades 
        (data, operador, atividade, talhao, maquina, horas, custo_hora, custo_estimado, insumo_qtd, insumo_nome, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data, operador, atividade, talhao, maquina, horas, custo_hora, custo_estimado, insumo_qtd, insumo_nome, observacoes))
    conn.commit()
    conn.close()

def carregar_dados():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM atividades", conn, parse_dates=["data"])
    conn.close()
    return df

def excluir_registros(ids):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.executemany("DELETE FROM atividades WHERE id = ?", [(i,) for i in ids])
    conn.commit()
    conn.close()

# ==== INICIALIZA TABELA ====
criar_tabela()

# ==== FORMULÁRIO ====
st.sidebar.header("Registrar Nova Atividade")
with st.sidebar.form("registro_form"):
    data = st.date_input("Data da Atividade", value=date.today())
    operador = st.selectbox("Operador", list(CUSTO_HORA_OPERADOR.keys()))
    atividade = st.selectbox("Atividade", ["Plantio", "Trato", "Colheita", "Aplicação de Insumo", "Revisão de Equipamento", "Vacinação", "Transporte", "Outros"])
    talhao = st.text_input("Talhão ou Lote")
    maquina = st.text_input("Máquina Utilizada")
    horas = st.number_input("Horas Trabalhadas", min_value=0.0, step=0.5)
    insumo_qtd = st.number_input("Quantidade de Insumo Usado (kg ou L)", min_value=0.0, step=0.1)
    insumo_nome = st.text_input("Nome(s) do(s) Insumo(s)")
    observacoes = st.text_area("Observações")

    submitted = st.form_submit_button("Salvar Registro")
    if submitted:
        custo_hora = CUSTO_HORA_OPERADOR[operador]
        custo_estimado = horas * custo_hora
        inserir_registro(str(data), operador, atividade, talhao, maquina, horas, custo_hora, custo_estimado, insumo_qtd, insumo_nome, observacoes)
        st.success(f"✅ Registro salvo com sucesso!")

# ==== DADOS ====
st.title("📒 Diário de Bordo da Fazenda")
df = carregar_dados()
if not df.empty:
    df = df.sort_values(by="data", ascending=False)

    # ==== FILTROS ====
    st.subheader("🔍 Filtro de Registros")
    col1, col2 = st.columns(2)
    with col1:
        filtro_atividade = st.multiselect("Filtrar por Atividade", df["atividade"].unique(), default=list(df["atividade"].unique()))
    with col2:
        filtro_talhao = st.multiselect("Filtrar por Talhão/Lote", df["talhao"].unique(), default=list(df["talhao"].unique()))

    df_filtrado = df[(df["atividade"].isin(filtro_atividade)) & (df["talhao"].isin(filtro_talhao))]

    # ==== SELEÇÃO PARA EXCLUSÃO ====
    st.subheader("📋 Registros (Selecione para Excluir)")
    df_filtrado["Selecionar"] = False
    selected_ids = []
    for i in df_filtrado.index:
        df_filtrado.at[i, "Selecionar"] = st.checkbox(
            f"{df_filtrado.at[i, 'data']} - {df_filtrado.at[i, 'atividade']} ({df_filtrado.at[i, 'talhao']})",
            key=f"check_{df_filtrado.at[i, 'id']}"
        )
        if df_filtrado.at[i, "Selecionar"]:
            selected_ids.append(int(df_filtrado.at[i, "id"]))

    if selected_ids:
        if st.button("🗑️ Excluir Registros Selecionados"):
            excluir_registros(selected_ids)
            st.success(f"{len(selected_ids)} registro(s) excluído(s). Recarregue a página manualmente para ver os resultados atualizados.")

    # ==== TABELA ====
    st.subheader("📊 Tabela de Atividades")
    st.dataframe(df_filtrado.drop(columns="Selecionar"), use_container_width=True)

    # ==== GRÁFICOS ====
    st.subheader("📈 Análise Operacional")
    col3, col4 = st.columns(2)

    df_graficos = df_filtrado.drop(columns=["Selecionar"], errors="ignore")

    with col3:
        st.write("Horas por Atividade")
        if "horas" in df_graficos.columns:
            horas_atividade = df_graficos.groupby("atividade")["horas"].sum()
            fig1, ax1 = plt.subplots()
            horas_atividade.plot(kind="bar", ax=ax1, color="orange")
            ax1.set_ylabel("Horas")
            ax1.set_title("Horas por Atividade")
            st.pyplot(fig1)
        else:
            st.info("Coluna 'horas' não disponível.")

    with col4:
        st.write("Custo por Talhão")
        if "custo_estimado" in df_graficos.columns:
            custo_talhao = df_graficos.groupby("talhao")["custo_estimado"].sum()
            fig2, ax2 = plt.subplots()
            custo_talhao.plot(kind="bar", ax=ax2, color="green")
            ax2.set_ylabel("R$")
            ax2.set_title("Custo por Talhão")
            st.pyplot(fig2)
        else:
            st.info("Coluna 'custo_estimado' não disponível.")
else:
    st.warning("Nenhum registro ainda. Use o formulário lateral para começar.")
