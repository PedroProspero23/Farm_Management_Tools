import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Milho"
area_total_ha = 150.0  # Área da propriedade agrícola

# ============================
# LISTA DE OUTROS CUSTOS FIXOS
# ============================

custos_fixos = [
    {
        "descricao": "Serviços contábeis (mensalidade)",
        "valor_anual": 3600.00  # R$300/mês
    },
    {
        "descricao": "Telefonia rural e internet",
        "valor_anual": 1200.00
    },
    {
        "descricao": "Manutenção de sede administrativa",
        "valor_anual": 4800.00
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for item in custos_fixos:
    item["custo_ha"] = item["valor_anual"] / area_total_ha
    relatorio.append(item)
    custo_total += item["valor_anual"]

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - V. Outros Custos Fixos", ln=True)

# Descrição
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla custos administrativos e estruturais recorrentes que nao estao diretamente ligados a operacoes especificas da lavoura, "
    "mas sao essenciais para a gestao da atividade agricola. O custo e rateado por hectare."
)
pdf.multi_cell(0, 10, descricao)

# Lista
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Custos Fixos Considerados:", ln=True)
pdf.set_font("Arial", size=12)
for item in relatorio:
    pdf.cell(0, 10, f"Descricao: {item['descricao']}", ln=True)
    pdf.cell(0, 10, f"  Valor anual: R$ {item['valor_anual']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Custo por ha: R$ {item['custo_ha']:.2f}", ln=True)
    pdf.ln(2)

# Resultados
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Total de Outros Custos Fixos: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"A producao de {cultura} depende da estrutura organizacional e de apoio da propriedade. "
    "Os custos fixos recorrentes foram considerados e proporcionalmente distribuidos por hectare."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "V_outros_custos_fixos.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
