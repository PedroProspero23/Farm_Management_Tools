import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Soja"
area_total_ha = 100.0  # Área total da lavoura

# ============================
# LISTA DE TAXAS E CONTRIBUIÇÕES
# ============================

taxas = [
    {
        "descricao": "Licenciamento ambiental estadual",
        "valor_total": 450.00
    },
    {
        "descricao": "Contribuição sindical rural (FAESP)",
        "valor_total": 300.00
    },
    {
        "descricao": "ITR - Imposto Territorial Rural",
        "valor_total": 700.00
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for t in taxas:
    relatorio.append(t)
    custo_total += t["valor_total"]

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - II.4 Taxas e Contribuicoes Obrigatorias", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla todas as taxas e contribuicoes exigidas legalmente para a atividade agricola, "
    "como licencas ambientais, impostos territoriais, e contribuicoes sindicais obrigatorias."
)
pdf.multi_cell(0, 10, descricao)

# Lista de taxas
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Taxas Consideradas:", ln=True)
pdf.set_font("Arial", size=12)
for t in relatorio:
    pdf.cell(0, 10, f"Descricao: {t['descricao']}", ln=True)
    pdf.cell(0, 10, f"  Valor total (R$): {t['valor_total']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Total de Taxas Obrigatórias: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"Para a cultura de {cultura}, foram consideradas taxas e contribuicoes exigidas pela legislacao vigente. "
    "Esses custos obrigatorios integram o custo operacional da lavoura conforme orientacao da CONAB."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "II4_taxas_contribuicoes.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
