import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Cana-de-açúcar"
area_total_ha = 60.0  # Área total da lavoura

# ============================
# LISTA DE RECEITAS DE SUBPRODUTOS/COPRODUTOS
# ============================

receitas = [
    {
        "nome": "Vinhaça para fertirrigação vendida",
        "quantidade_vendida": 12000,  # em litros ou toneladas
        "preco_unitario": 0.05        # R$/litro ou tonelada
    },
    {
        "nome": "Bagaço seco para energia",
        "quantidade_vendida": 8000,
        "preco_unitario": 0.08
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
receita_total = 0

for r in receitas:
    receita = r["quantidade_vendida"] * r["preco_unitario"]
    r["receita_total"] = receita
    relatorio.append(r)
    receita_total += receita

receita_por_ha = receita_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - I.9 Receita de Subproduto ou Coproduto", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item representa as receitas geradas com a comercializacao de subprodutos ou coprodutos da lavoura, "
    "como vinhaça, palhada, sementes ou outros materiais valorizados comercialmente, deduzindo esses valores do custo final."
)
pdf.multi_cell(0, 10, descricao)

# Lista de receitas
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Receitas Consideradas:", ln=True)
pdf.set_font("Arial", size=12)
for r in relatorio:
    pdf.cell(0, 10, f"Nome: {r['nome']}", ln=True)
    pdf.cell(0, 10, f"  Quantidade vendida: {r['quantidade_vendida']}", ln=True)
    pdf.cell(0, 10, f"  Preço unitário (R$): {r['preco_unitario']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Receita total (R$): {r['receita_total']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Receita Total com Subprodutos: R$ {receita_total:.2f}", ln=True)
pdf.cell(0, 10, f"Receita por ha: R$ {receita_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"A lavoura de {cultura} gerou materiais valorizados no mercado como subprodutos. "
    "Essas receitas foram contabilizadas como dedução no custo total de produção conforme a metodologia CONAB."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "I9_receita_subproduto.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
