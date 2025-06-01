import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from monte_carlo_engine import Farmer, MonteCarloSimulator

st.set_page_config(page_title="Simulador Agrícola", layout="wide")
st.title("🌾 Simulador de Lucro Agrícola com Monte Carlo")

abas = st.tabs(["📈 Simulação", "📚 Explicação do Modelo"])

# -------- ABA 1: SIMULAÇÃO --------
with abas[0]:
    st.header("📈 Simulação de Safras")

    # Sidebar: parâmetros da simulação
    st.sidebar.header("⚙️ Parâmetros da Simulação")
    hectares = st.sidebar.number_input("Área da fazenda (hectares)", 10, 10000, 100, step=10)
    custo_fixo = st.sidebar.number_input("Custo fixo total (R$)", 0, 100000, 20000, step=1000)

    custo_soja_medio = st.sidebar.number_input("Custo médio da soja (R$/ha)", 500, 5000, 2500, step=100)
    variacao_custo_soja = st.sidebar.slider("Variação no custo da soja (%)", 0, 100, 10) / 100

    custo_milho_medio = st.sidebar.number_input("Custo médio do milho (R$/ha)", 500, 5000, 3000, step=100)
    variacao_custo_milho = st.sidebar.slider("Variação no custo do milho (%)", 0, 100, 10) / 100

    media_soja = st.sidebar.number_input("Produtividade média da soja (sacas/ha)", 30.0, 100.0, 55.0)
    variacao_prod_soja = st.sidebar.slider("Variação produtividade soja (%)", 0, 100, 10) / 100 * media_soja

    media_milho = st.sidebar.number_input("Produtividade média do milho (sacas/ha)", 80.0, 200.0, 140.0)
    variacao_prod_milho = st.sidebar.slider("Variação produtividade milho (%)", 0, 100, 10) / 100 * media_milho

    preco_soja = st.sidebar.number_input("Preço médio da soja (R$)", 50.0, 200.0, 140.0)
    variacao_preco_soja = st.sidebar.slider("Variação preço soja (%)", 0, 100, 15) / 100

    preco_milho = st.sidebar.number_input("Preço médio do milho (R$)", 30.0, 150.0, 80.0)
    variacao_preco_milho = st.sidebar.slider("Variação preço milho (%)", 0, 100, 10) / 100

    iteracoes = st.sidebar.slider("Número de simulações", 100, 10000, 1000, step=100)

    # Botão de simular
    if st.button("🚀 Rodar Simulação"):
        fazendeiro = Farmer(
            hectares=hectares,
            custo_fixo=custo_fixo,
            media_custo_soja=custo_soja_medio,
            media_custo_milho=custo_milho_medio,
            variacao_custo_soja=variacao_custo_soja,
            variacao_custo_milho=variacao_custo_milho,
            media_prod_soja=media_soja,
            media_prod_milho=media_milho,
            variacao_prod_soja=variacao_prod_soja,
            variacao_prod_milho=variacao_prod_milho
        )

        sim = MonteCarloSimulator(
            preco_soja_medio=preco_soja,
            preco_milho_medio=preco_milho,
            variacao_preco_soja=variacao_preco_soja,
            variacao_preco_milho=variacao_preco_milho,
            iteracoes=iteracoes
        )

        resultados = sim.simular(fazendeiro)

        # Estatísticas e interpretação
        lucro_medio = resultados["lucro"].mean()
        lucro_p25 = resultados["lucro"].quantile(0.25)
        lucro_max = resultados["lucro"].max()
        lucro_min = resultados["lucro"].min()

        st.subheader("📊 Resultados da Simulação")
        st.write(resultados[["lucro", "receita", "custo_total", "proporcao_soja"]].describe())

        st.markdown(f"""
### 🧠 Interpretação do Resultado

Após **{iteracoes} simulações**, temos os seguintes destaques:

- 💵 **Lucro médio esperado**: R$ {lucro_medio:,.2f}
- ⚠️ Em **25% dos casos**, o lucro foi **menor que R$ {lucro_p25:,.2f}**
- 🏆 **Melhor cenário**: R$ {lucro_max:,.2f}
- 🛑 **Pior cenário**: R$ {lucro_min:,.2f}
""")

        # --------- Painel de insights adicionais ---------
        st.subheader("🔎 Insights Estratégicos")

        correlacao_soja = resultados["lucro"].corr(resultados["proporcao_soja"])
        st.markdown(f"**Correlação lucro vs proporção de soja:** `{correlacao_soja:.2f}`")

        if correlacao_soja > 0.1:
            st.info("💡 Cultivar **mais soja** tende a aumentar o lucro.")
        elif correlacao_soja < -0.1:
            st.info("💡 Cultivar **mais milho** tende a aumentar o lucro.")
        else:
            st.info("⚖️ A proporção entre soja e milho não impacta muito o lucro.")

        top_10 = resultados.sort_values(by="lucro", ascending=False).head(10)
        bottom_10 = resultados.sort_values(by="lucro", ascending=True).head(10)

        media_top = top_10[["lucro", "preco_soja", "producao_soja", "custo_soja_ha"]].mean()
        media_bottom = bottom_10[["lucro", "preco_soja", "producao_soja", "custo_soja_ha"]].mean()

        df_comp = pd.DataFrame({
            "Top 10 Lucros": media_top,
            "Bottom 10 Lucros": media_bottom
        })

        st.markdown("**🔍 Comparativo entre os melhores e piores cenários:**")
        st.dataframe(df_comp.style.format("{:.2f}"))

        proporcao_negativo = (resultados["lucro"] < 0).mean()
        st.markdown(f"📉 **{proporcao_negativo:.1%} das simulações resultaram em prejuízo.**")

        if proporcao_negativo > 0.3:
            st.warning("⚠️ Alta chance de prejuízo! Reavalie os custos ou tente reduzir variabilidade.")
        elif proporcao_negativo > 0:
            st.info("🟡 Risco moderado de prejuízo. Considere estratégias de mitigação.")
        else:
            st.success("✅ Nenhum prejuízo simulado. Ótimo cenário!")

        if st.checkbox("📈 Mostrar gráfico: Proporção de soja vs Lucro"):
            fig2, ax2 = plt.subplots()
            ax2.scatter(resultados["proporcao_soja"], resultados["lucro"], alpha=0.5)
            ax2.set_xlabel("Proporção de Soja")
            ax2.set_ylabel("Lucro (R$)")
            ax2.set_title("Dispersão: Proporção Soja vs Lucro")
            st.pyplot(fig2)

        # Histograma do lucro
        fig, ax = plt.subplots()
        ax.hist(resultados["lucro"], bins=30, color="green", edgecolor="black")
        ax.set_title("Distribuição de Lucro")
        ax.set_xlabel("Lucro (R$)")
        ax.set_ylabel("Frequência")
        st.pyplot(fig)

        # Top 5 melhores lucros
        st.subheader("🏆 Top 5 Resultados de Lucro")
        st.dataframe(resultados.sort_values(by="lucro", ascending=False).head(5))

        # Exportar CSV
        csv = resultados.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar CSV", csv, "resultados_simulacao.csv", "text/csv")

    else:
        st.info("Configure os parâmetros e clique em **Rodar Simulação**.")

# -------- ABA 2: EXPLICAÇÃO --------
with abas[1]:
    st.header("📚 Como funciona a Simulação de Monte Carlo?")
    st.markdown("""
Monte Carlo é uma técnica que simula **diversos cenários possíveis** para entender os **riscos e incertezas** do seu negócio.

### 🔁 O que acontece em cada simulação?
1. O sistema escolhe uma **proporção aleatória entre soja e milho**
2. Aplica **perdas climáticas** simuladas
3. Aplica **produtividades variáveis**
4. Define **preços de venda com flutuação**
5. Aplica **custos variáveis com incerteza**
6. Calcula: `Lucro = Receita - Custo Total`

Isso é feito **milhares de vezes**, gerando uma distribuição como essa:
""")

    fig, ax = plt.subplots()
    ax.hist([1,2,3,4,5,5,5,5,6,7,8,9,10,10,11,11,11,12,13,14,15], bins=10, color="gray", edgecolor="black")
    ax.set_title("Exemplo de Distribuição Simulada")
    ax.set_xlabel("Lucro (R$ mil)")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)

    st.markdown("""
---

### 🧠 Para que serve?
- Entender **o lucro médio esperado**
- Saber **quanto pode perder no pior cenário**
- Ver a **probabilidade de ter lucro** ou prejuízo

---

### 🔍 Glossário das variáveis

| Variável                | O que representa                            |
|-------------------------|---------------------------------------------|
| `proporcao_soja`        | % da área total usada com soja              |
| `produtividade`         | Sacas por hectare (com variação)            |
| `preço`                 | Valor de mercado com oscilação              |
| `custo variável`        | Insumos, mão de obra, etc. com incerteza    |
| `perda climática`       | Redução na produção por fatores naturais    |
| `lucro`                 | Receita total menos custo total             |

---

### 📌 Como definir os percentuais de variação?

- **Produtividade**: use histórico da sua fazenda ou dados da **CONAB**
- **Preço**: use CEPEA, mercado futuro ou médias de 3 anos
- **Custo**: estimativa baseada em notas fiscais anteriores

---

### 📈 Quantas simulações usar?

- 100 a 500: testes rápidos
- 1000: boa estimativa
- 5000+: análises de risco mais sérias

---

**Dica:** você pode usar essa ferramenta para decidir **qual cultura plantar**, **qual proporção adotar**, ou **qual margem de segurança manter** no seu caixa 💰.
""")

