import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Milho"
area_total_ha = 50.0  # Área total da lavoura

# ============================
# LISTA DE TRANSPORTES
# ============================

transportes = [
    {
        "descricao": "Transporte até a cooperativa",
        "quantidade_transportada": 20000,  # em kg ou toneladas
        "preco_unitario": 0.16             # R$ por kg ou tonelada
    },
    {
        "descricao": "Frete até armazém intermediário",
        "quantidade_transportada": 8000,
        "preco_unitario": 0.12
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for t in transportes:
    custo = t["quantidade_transportada"] * t["preco_unitario"]
    t["custo_total"] = custo
    relatorio.append(t)
    custo_total += custo

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - II.1 Transporte Externo da Producao", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla os custos com transporte externo da producao agricola, do campo ate o destino de entrega, "
    "como armazens, cooperativas ou industrias. Inclui fretes contratados e operacoes proprias com custo atribuido."
)
pdf.multi_cell(0, 10, descricao)

# Lista de transportes
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Transportes Realizados:", ln=True)
pdf.set_font("Arial", size=12)
for t in relatorio:
    pdf.cell(0, 10, f"Descricao: {t['descricao']}", ln=True)
    pdf.cell(0, 10, f"  Quantidade transportada: {t['quantidade_transportada']}", ln=True)
    pdf.cell(0, 10, f"  Preço unitário do frete (R$): {t['preco_unitario']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Custo total (R$): {t['custo_total']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Custo Total com Transporte: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"A cultura de {cultura} exigiu deslocamento da producao ate unidades de armazenamento e beneficiamento, "
    "o que gerou custos logísticos diretos considerados no cálculo total do custo operacional."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "II1_transporte_externo.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
