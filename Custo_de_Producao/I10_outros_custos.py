import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Arroz irrigado"
area_total_ha = 22.0  # Área total da lavoura

# ============================
# LISTA DE OUTROS CUSTOS
# ============================

outros_custos = [
    {
        "descricao": "Ensacamento manual da produção",
        "valor_total": 750.00
    },
    {
        "descricao": "Recolhimento e enleiramento de palha",
        "valor_total": 1250.00
    },
    {
        "descricao": "Aluguel de bombas extras de irrigação",
        "valor_total": 400.00
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for c in outros_custos:
    relatorio.append(c)
    custo_total += c["valor_total"]

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - I.10 Outros Custos de Custeio", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla despesas complementares e eventuais que nao se enquadram nos itens anteriores da planilha de custeio, "
    "como servicos internos, atividades especificas ou uso de estruturas da propriedade."
)
pdf.multi_cell(0, 10, descricao)

# Lista de outros custos
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Custos Considerados:", ln=True)
pdf.set_font("Arial", size=12)
for c in relatorio:
    pdf.cell(0, 10, f"Descricao: {c['descricao']}", ln=True)
    pdf.cell(0, 10, f"  Valor total (R$): {c['valor_total']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Total de Outros Custos: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"Na cultura de {cultura}, identificaram-se custos operacionais extras como parte das rotinas internas da lavoura. "
    "Tais custos foram inseridos separadamente por sua natureza específica e recorrência na propriedade."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "I10_outros_custos.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
