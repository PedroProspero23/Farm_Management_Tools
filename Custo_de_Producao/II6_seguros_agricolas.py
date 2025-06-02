import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Milho"
area_total_ha = 85.0  # Área total da lavoura

# ============================
# LISTA DE SEGUROS CONTRATADOS
# ============================

seguros = [
    {
        "descricao": "Seguro agrícola contra granizo e seca",
        "valor_pago": 1300.00
    },
    {
        "descricao": "Seguro de máquina exclusiva para pulverização",
        "valor_pago": 450.00
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for s in seguros:
    relatorio.append(s)
    custo_total += s["valor_pago"]

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - II.6 Seguros Agricolas", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla os custos com a contratacao de seguros especificos para a atividade agricola, "
    "como protecao contra perdas climaticas, danos a maquinas operacionais da lavoura e risco de credito agricola."
)
pdf.multi_cell(0, 10, descricao)

# Lista de seguros
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Seguros Contratados:", ln=True)
pdf.set_font("Arial", size=12)
for s in relatorio:
    pdf.cell(0, 10, f"Descricao: {s['descricao']}", ln=True)
    pdf.cell(0, 10, f"  Valor pago (R$): {s['valor_pago']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Total com Seguros Agricolas: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"Para a cultura de {cultura}, foram contratados seguros visando a protecao da producao e equipamentos essenciais. "
    "Esses custos foram incorporados ao custo operacional total conforme a metodologia CONAB."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "II6_seguros_agricolas.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
