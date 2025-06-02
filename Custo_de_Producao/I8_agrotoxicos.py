import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Soja"
area_total_ha = 45.0  # Área total da lavoura

# ============================
# LISTA DE AGROTÓXICOS
# ============================

agrotoxicos = [
    {
        "nome": "Herbicida Glifosato",
        "quantidade_aplicada": 12,     # litros ou kg
        "preco_unitario": 35.00        # R$/litro ou kg
    },
    {
        "nome": "Inseticida Lambda-cialotrina",
        "quantidade_aplicada": 8,
        "preco_unitario": 42.50
    },
    {
        "nome": "Fungicida Triazol",
        "quantidade_aplicada": 10,
        "preco_unitario": 55.90
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for p in agrotoxicos:
    custo = p["quantidade_aplicada"] * p["preco_unitario"]
    p["custo_total"] = custo
    relatorio.append(p)
    custo_total += custo

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - I.8 Agrotoxicos", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla os gastos com produtos fitossanitarios utilizados na lavoura, "
    "incluindo herbicidas, inseticidas, fungicidas e acaricidas, com base nas quantidades aplicadas e precos unitarios praticados."
)
pdf.multi_cell(0, 10, descricao)

# Lista de produtos
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Agrotoxicos Utilizados:", ln=True)
pdf.set_font("Arial", size=12)
for p in relatorio:
    pdf.cell(0, 10, f"Nome: {p['nome']}", ln=True)
    pdf.cell(0, 10, f"  Quantidade aplicada: {p['quantidade_aplicada']}", ln=True)
    pdf.cell(0, 10, f"  Preço unitário (R$): {p['preco_unitario']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Custo total (R$): {p['custo_total']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Custo Total com Agrotoxicos: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"Na cultura de {cultura}, foram aplicados produtos fitossanitarios para controle de plantas daninhas, pragas e doencas. "
    "Os custos refletem a quantidade aplicada por produto e seus respectivos valores de mercado."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "I8_agrotoxicos.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
