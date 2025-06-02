import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Algodão"
area_total_ha = 12.0  # Área total cultivada

# ============================
# LISTA DE SEMENTES OU MUDAS
# ============================

insumos = [
    {
        "nome": "Semente de algodão transgênico",
        "quantidade_usada": 20,     # em kg ou mil unidades
        "preco_unitario": 45.00     # R$ por kg ou milheiro
    },
    {
        "nome": "Muda de crotalária (adubo verde)",
        "quantidade_usada": 8,
        "preco_unitario": 12.50
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for i in insumos:
    custo = i["quantidade_usada"] * i["preco_unitario"]
    i["custo_total"] = custo
    relatorio.append(i)
    custo_total += custo

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - I.6 Sementes e Mudas", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla os gastos com sementes e/ou mudas utilizadas na lavoura, sejam adquiridas ou produzidas na propriedade, "
    "incluindo os custos proporcionais ao uso por hectare cultivado."
)
pdf.multi_cell(0, 10, descricao)

# Parâmetros usados
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Sementes/Mudas Utilizadas:", ln=True)
pdf.set_font("Arial", size=12)
for i in relatorio:
    pdf.cell(0, 10, f"Nome: {i['nome']}", ln=True)
    pdf.cell(0, 10, f"  Quantidade usada: {i['quantidade_usada']}", ln=True)
    pdf.cell(0, 10, f"  Preço unitário (R$): {i['preco_unitario']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Custo total (R$): {i['custo_total']:.2f}", ln=True)
    pdf.ln(2)

# Resultados finais
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Custo Total com Sementes/Mudas: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"Na cultura de {cultura}, foram utilizadas sementes e mudas conforme as exigências técnicas da lavoura. "
    "Os valores informados refletem custos de mercado ou estimativas imputadas para materiais produzidos internamente."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "I6_sementes_mudas.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
