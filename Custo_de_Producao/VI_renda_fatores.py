import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Milho"
area_ha = 130.0

# ============================
# DADOS DE RENDA DOS FATORES
# ============================

valor_aluguel_ha = 1000.00  # R$/ha por ano
capital_investido = 500000.00  # R$
juros_anual = 0.08  # 8% ao ano
pro_labore = 48000.00  # R$ anual estimado

# ============================
# CÁLCULOS
# ============================

custo_terra = valor_aluguel_ha * area_ha  # aluguel da terra própria
custo_capital = capital_investido * juros_anual  # remuneração do capital próprio
custo_total = custo_terra + custo_capital + pro_labore
custo_por_ha = custo_total / area_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - VI. Renda dos Fatores", ln=True)

# Descrição
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item considera a remuneracao dos fatores de producao que pertencem ao produtor: "
    "terra, capital e administracao. Tais custos representam o valor de oportunidade e compoem o custo total da atividade."
)
pdf.multi_cell(0, 10, descricao)

# Itens detalhados
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Fatores Considerados:", ln=True)
pdf.set_font("Arial", size=12)
pdf.cell(0, 10, f"Aluguel hipotetico da terra: R$ {valor_aluguel_ha:.2f}/ha", ln=True)
pdf.cell(0, 10, f"Area: {area_ha:.2f} ha", ln=True)
pdf.cell(0, 10, f"Custo com terra: R$ {custo_terra:.2f}", ln=True)
pdf.ln(2)
pdf.cell(0, 10, f"Capital proprio investido: R$ {capital_investido:.2f}", ln=True)
pdf.cell(0, 10, f"Taxa de juros anual: {juros_anual*100:.1f}%", ln=True)
pdf.cell(0, 10, f"Custo de capital: R$ {custo_capital:.2f}", ln=True)
pdf.ln(2)
pdf.cell(0, 10, f"Pro-labore (remuneracao da administracao): R$ {pro_labore:.2f}", ln=True)

# Resultados
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Total Renda dos Fatores: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"A cultura de {cultura} utiliza recursos proprios do produtor, como terra, capital e gestao. "
    "Para fins de analise economica completa, esses fatores sao valorados e rateados conforme area cultivada."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "VI_renda_fatores.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
