import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import getpass

# ============================
# INPUT MANUAL DE VALORES
# ============================

# Área total (necessária para cálculo de custo por ha)
area_total_ha = 30.0

# Valores fictícios por item (em R$)
custos = {
    # Bloco I – Despesas de Custeio da Lavoura
    "I1_operacao_animal": 3500,
    "I2_operacao_aviao": 2700,
    "I3_op_maq_proprias": 4100,
    "I4_aluguel_maq": 3000,
    "I5_mao_de_obra": 5600,
    "I6_sementes_e_mudas": 2200,
    "I7_fertilizantes": 6800,
    "I8_agrotoxicos": 4000,
    "I9_receita_subproduto": -1000,
    "I10_outros_custos": 850,

    # Bloco II – Outras Despesas
    "II1_transporte_externo": 1300,
    "II2_despesas_adm": 900,
    "II3_despesas_armazenagem": 700,
    "II4_taxas_contribuicoes": 600,
    "II5_custo_beneficiamento": 1200,
    "II6_seguros_agricolas": 850,

    # Bloco III – Despesas Financeiras
    "III1_despesas_financeiras": 1100,

    # Bloco IV – Depreciações
    "IV1_depreciacao_benfeitorias": 950,
    "IV2_depreciacao_maquinas": 1800,
    "IV3_depreciacao_outiva": 750,

    # Bloco V – Outros Custos Fixos
    "V_outros_custos_fixos": 2100,

    # Bloco VI – Renda dos Fatores
    "VI_renda_fatores": 9200
}

# ============================
# AGRUPAMENTO POR BLOCO
# ============================

grupos = {
    "I": [k for k in custos if k.startswith("I") and not k.startswith("II")],
    "II": [k for k in custos if k.startswith("II")],
    "III": [k for k in custos if k.startswith("III")],
    "IV": [k for k in custos if k.startswith("IV")],
    "V": [k for k in custos if k.startswith("V")],
    "VI": [k for k in custos if k.startswith("VI")]
}

resumo_blocos = {bloco: sum(custos[item] for item in itens) for bloco, itens in grupos.items()}

# Cálculo final
COE = resumo_blocos["I"] + resumo_blocos["II"]
COT = COE + resumo_blocos["III"] + resumo_blocos["IV"]
CT = COT + resumo_blocos["V"] + resumo_blocos["VI"]

# ============================
# GRÁFICO DE PIZZA POR BLOCO
# ============================

fig1, ax1 = plt.subplots()
ax1.pie(resumo_blocos.values(), labels=resumo_blocos.keys(), autopct="%1.1f%%", startangle=90)
ax1.axis("equal")
plt.title("Distribuição dos Custos por Bloco")
pizza_path = "grafico_pizza_blocos.png"
plt.savefig(pizza_path)

# ============================
# GRÁFICO DE BARRAS POR ITEM
# ============================

fig2, ax2 = plt.subplots(figsize=(10, 6))
itens = list(custos.keys())
valores = list(custos.values())
ax2.barh(itens, valores)
plt.title("Custo por Item (R$)")
plt.xlabel("Valor em R$")
plt.tight_layout()
barras_path = "grafico_barras_itens.png"
plt.savefig(barras_path)

# ============================
# RELATÓRIO EM PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Consolidado de Custo de Producao - Norma CONAB 30.302", ln=True)

# Sumário
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Sumario dos Blocos:", ln=True)
pdf.set_font("Arial", size=12)
for bloco, valor in resumo_blocos.items():
    pdf.cell(0, 10, f"Bloco {bloco} - Total: R$ {valor:,.2f}", ln=True)

pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Custo Operacional Efetivo (COE): R$ {COE:,.2f}", ln=True)
pdf.cell(0, 10, f"Custo Operacional Total (COT): R$ {COT:,.2f}", ln=True)
pdf.cell(0, 10, f"Custo Total (CT): R$ {CT:,.2f}", ln=True)

# Custo por hectare
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Custo por ha:", ln=True)
pdf.set_font("Arial", size=12)
pdf.cell(0, 10, f"COE/ha: R$ {COE / area_total_ha:,.2f}", ln=True)
pdf.cell(0, 10, f"COT/ha: R$ {COT / area_total_ha:,.2f}", ln=True)
pdf.cell(0, 10, f"CT/ha: R$ {CT / area_total_ha:,.2f}", ln=True)

# Inserção de gráficos
pdf.ln(10)
pdf.image(pizza_path, w=pdf.w / 2)
pdf.add_page()
pdf.image(barras_path, w=pdf.w - 20)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
output_pdf = os.path.join("C:/Users", usuario, "Downloads", "Relatorio_Consolidado_CONAB.pdf")
pdf.output(output_pdf)
print(f"✅ Relatório salvo em: {output_pdf}")
