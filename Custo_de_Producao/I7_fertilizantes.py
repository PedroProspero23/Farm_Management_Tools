import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Milho"
area_total_ha = 40.0  # Área total da lavoura

# ============================
# LISTA DE FERTILIZANTES
# ============================

fertilizantes = [
    {
        "nome": "Fertilizante NPK 20-05-20",
        "quantidade_aplicada": 350,     # em kg/ha ou total aplicado
        "preco_unitario": 4.20          # R$/kg
    },
    {
        "nome": "Calcário dolomítico",
        "quantidade_aplicada": 2000,
        "preco_unitario": 0.35
    },
    {
        "nome": "Gesso agrícola",
        "quantidade_aplicada": 1000,
        "preco_unitario": 0.42
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for f in fertilizantes:
    custo = f["quantidade_aplicada"] * f["preco_unitario"]
    f["custo_total"] = custo
    relatorio.append(f)
    custo_total += custo

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - I.7 Fertilizantes", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla os gastos com fertilizantes quimicos, organicos, calcario e gesso, "
    "utilizados na lavoura, com base na quantidade aplicada e valores de mercado praticados na regiao."
)
pdf.multi_cell(0, 10, descricao)

# Lista de fertilizantes
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Fertilizantes Utilizados:", ln=True)
pdf.set_font("Arial", size=12)
for f in relatorio:
    pdf.cell(0, 10, f"Nome: {f['nome']}", ln=True)
    pdf.cell(0, 10, f"  Quantidade aplicada: {f['quantidade_aplicada']}", ln=True)
    pdf.cell(0, 10, f"  Preço unitário (R$): {f['preco_unitario']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Custo total (R$): {f['custo_total']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Custo Total com Fertilizantes: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"Para a cultura do {cultura}, foram utilizados diferentes corretivos e fertilizantes conforme as exigencias do solo "
    "e da produtividade esperada. O custo total foi calculado com base na quantidade aplicada e nos precos unitarios informados."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "I7_fertilizantes.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
