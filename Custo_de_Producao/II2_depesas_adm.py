import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Soja"
area_total_ha = 80.0  # Área total da lavoura

# ============================
# LISTA DE DESPESAS ADMINISTRATIVAS
# ============================

despesas = [
    {
        "descricao": "Energia elétrica do escritório rural",
        "valor_total": 420.00
    },
    {
        "descricao": "Mensalidade de software de gestão",
        "valor_total": 199.00
    },
    {
        "descricao": "Telefone e internet",
        "valor_total": 185.00
    },
    {
        "descricao": "Material de escritório e papelaria",
        "valor_total": 115.00
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for d in despesas:
    relatorio.append(d)
    custo_total += d["valor_total"]

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - II.2 Despesas Administrativas", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla as despesas administrativas da atividade rural, como energia do escritorio, sistemas de gestao, telefonia, "
    "material de escritorio e servicos de apoio administrativo, que sao essenciais ao funcionamento organizacional da propriedade."
)
pdf.multi_cell(0, 10, descricao)

# Lista de despesas
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Despesas Consideradas:", ln=True)
pdf.set_font("Arial", size=12)
for d in relatorio:
    pdf.cell(0, 10, f"Descricao: {d['descricao']}", ln=True)
    pdf.cell(0, 10, f"  Valor total (R$): {d['valor_total']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Total de Despesas Administrativas: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"As despesas administrativas na lavoura de {cultura} incluem o funcionamento do escritorio rural e o suporte operacional indireto, "
    "necessario para a gestao e controle da atividade agricola, sendo contabilizadas como parte do custo operacional total."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "II2_despesas_administrativas.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
