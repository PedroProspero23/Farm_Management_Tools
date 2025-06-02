import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Milho"
area_total_ha = 70.0  # Área total da lavoura

# ============================
# LISTA DE DESPESAS DE ARMAZENAGEM
# ============================

armazenagens = [
    {
        "descricao": "Armazenagem em silo da cooperativa",
        "quantidade_armazenada": 25000,  # em kg ou toneladas
        "preco_unitario": 0.10            # R$/kg ou R$/ton
    },
    {
        "descricao": "Armazenagem em silo comercial",
        "quantidade_armazenada": 18000,
        "preco_unitario": 0.12
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for a in armazenagens:
    custo = a["quantidade_armazenada"] * a["preco_unitario"]
    a["custo_total"] = custo
    relatorio.append(a)
    custo_total += custo

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - II.3 Despesas de Armazenagem", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla os custos relacionados ao armazenamento da producao agricola fora da propriedade, "
    "incluindo taxas de armazenagem em cooperativas, armazens e estruturas comerciais contratadas."
)
pdf.multi_cell(0, 10, descricao)

# Lista de armazenagens
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Serviços de Armazenagem Considerados:", ln=True)
pdf.set_font("Arial", size=12)
for a in relatorio:
    pdf.cell(0, 10, f"Descricao: {a['descricao']}", ln=True)
    pdf.cell(0, 10, f"  Quantidade armazenada: {a['quantidade_armazenada']}", ln=True)
    pdf.cell(0, 10, f"  Preço unitário (R$): {a['preco_unitario']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Custo total (R$): {a['custo_total']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Custo Total com Armazenagem: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"Durante a colheita da cultura de {cultura}, parte da producao foi armazenada fora da propriedade, "
    "gerando custos com taxas de armazenagem que foram corretamente atribuídos ao custo operacional total."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "II3_despesas_armazenagem.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
