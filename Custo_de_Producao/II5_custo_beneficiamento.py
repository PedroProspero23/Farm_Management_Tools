import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Feijão"
area_total_ha = 60.0  # Área total da lavoura

# ============================
# LISTA DE CUSTOS DE BENEFICIAMENTO
# ============================

beneficiamentos = [
    {
        "descricao": "Secagem e limpeza pós-colheita",
        "quantidade_beneficiada": 15000,  # em kg ou sacas
        "preco_unitario": 0.18            # R$/kg ou R$/saca
    },
    {
        "descricao": "Classificação e ensacamento",
        "quantidade_beneficiada": 15000,
        "preco_unitario": 0.12
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for b in beneficiamentos:
    custo = b["quantidade_beneficiada"] * b["preco_unitario"]
    b["custo_total"] = custo
    relatorio.append(b)
    custo_total += custo

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - II.5 Custo de Beneficiamento", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla os custos com beneficiamento obrigatorio da producao antes da comercializacao, "
    "incluindo secagem, limpeza, classificacao, selecao e outros processos necessarios para padronizacao do produto final."
)
pdf.multi_cell(0, 10, descricao)

# Lista de beneficiamentos
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Serviços de Beneficiamento Considerados:", ln=True)
pdf.set_font("Arial", size=12)
for b in relatorio:
    pdf.cell(0, 10, f"Descricao: {b['descricao']}", ln=True)
    pdf.cell(0, 10, f"  Quantidade beneficiada: {b['quantidade_beneficiada']}", ln=True)
    pdf.cell(0, 10, f"  Preço unitário (R$): {b['preco_unitario']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Custo total (R$): {b['custo_total']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Custo Total com Beneficiamento: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"O beneficiamento da cultura de {cultura} foi necessario para atender aos requisitos de comercializacao, "
    "incluindo padronizacao visual e qualidade. Os servicos executados foram registrados e considerados como parte do COT."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "II5_custo_beneficiamento.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
