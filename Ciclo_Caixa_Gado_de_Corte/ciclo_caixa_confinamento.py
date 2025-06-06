import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime, timedelta

# ---------- Função auxiliar ----------
def dias_para_data(base, dias):
    return base + timedelta(days=dias)

# ---------- Dados base ----------
base_data = datetime(2024, 7, 1)

eventos = [
    # Lote 1
    ["Compra Bois", "L1", 0, 1, "compra_bois", -120_000],
    ["Engorda 90d", "L1", 0, 90, "engorda", 0],
    ["Venda", "L1", 90, 1, "venda", 0],
    ["Recebimento", "L1", 100, 1, "recebimento", 180_000],

    # Lote 2
    ["Compra Bois", "L2", 20, 1, "compra_bois", -110_000],
    ["Engorda 90d", "L2", 20, 90, "engorda", 0],
    ["Venda", "L2", 110, 1, "venda", 0],
    ["Recebimento", "L2", 140, 1, "recebimento", 165_000],

    # Insumos compartilhados
    ["Compra Ração Inicial", "", 0, 1, "insumo", -40_000],
    ["Compra Núcleo Mineral", "", 10, 1, "insumo", -15_000],
    ["Reposição Ração", "", 35, 1, "insumo", -30_000],
    ["Reposição Núcleo", "", 65, 1, "insumo", -10_000],
    ["Reposição Final Ração", "", 95, 1, "insumo", -25_000],
]

# ---------- DataFrame ----------
dados = []
for desc, lote, d_ini, dur, tipo, valor in eventos:
    dados.append({
        "Descrição": f"{desc} ({lote})" if lote else desc,
        "Lote": lote,
        "Início": dias_para_data(base_data, d_ini),
        "Fim": dias_para_data(base_data, d_ini + dur),
        "Tipo": tipo,
        "Valor": valor
    })
df = pd.DataFrame(dados)

# ---------- Cores ----------
cores = {
    "compra_bois": "#cce5ff",
    "insumo": "#e6f2cc",
    "engorda": "#fff3cd",
    "venda": "#f4cccc",
    "recebimento": "#c1e1e6"
}

# ---------- Gráfico ----------
fig, ax = plt.subplots(figsize=(14, 8))

for i, row in df.iterrows():
    cor = cores.get(row["Tipo"], "#dddddd")
    ax.barh(
        y=i,
        width=row["Fim"] - row["Início"],
        left=row["Início"],
        height=0.8,
        color=cor,
        edgecolor='black'
    )
    ax.text(row["Início"] + (row["Fim"] - row["Início"]) / 2,
            i, row["Descrição"], ha='center', va='center', fontsize=8, weight='bold')
    if row["Valor"] != 0:
        cor_valor = "green" if row["Valor"] > 0 else "red"
        offset_y = 0.5 if i % 2 == 0 else -0.5
        ax.text(row["Início"] + (row["Fim"] - row["Início"]) / 2,
                i + offset_y,
                f"R$ {row['Valor'] / 1_000:.1f} mil",
                ha='center', va='center', fontsize=8, color=cor_valor, weight='bold')

# ---------- Estética ----------
ax.set_yticks([])
ax.set_title("📊 Ciclo de Caixa com Insumos Compartilhados e Valores em R$", fontsize=14, weight='bold')
ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
plt.xticks(rotation=45)

# ---------- Legenda ----------
legenda = [
    mpatches.Patch(color=cores["compra_bois"], label="Compra Bois"),
    mpatches.Patch(color=cores["insumo"], label="Compra/Recompra Insumos (compartilhados)"),
    mpatches.Patch(color=cores["engorda"], label="Engorda/Confinamento"),
    mpatches.Patch(color=cores["venda"], label="Venda"),
    mpatches.Patch(color=cores["recebimento"], label="Recebimento"),
]
ax.legend(handles=legenda, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.12))

plt.tight_layout()
plt.show()
