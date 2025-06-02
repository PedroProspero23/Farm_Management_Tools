import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Feijão"
area_total_ha = 18.0  # Área total em hectares

# ============================
# LISTA DE ITENS ALUGADOS
# ============================

itens_alugados = [
    {
        "equipamento": "Trator 120cv alugado",
        "horas_usadas": 10,
        "preco_hora": 160.00
    },
    {
        "equipamento": "Pá-carregadeira",
        "horas_usadas": 5,
        "preco_hora": 220.00
    },
    {
        "equipamento": "Boi de tração",
        "horas_usadas": 8,
        "preco_hora": 75.00
    }
]

# ============================
# CÁLCULO
# ============================

relatorio = []
custo_total = 0

for item in itens_alugados:
    custo = item["horas_usadas"] * item["preco_hora"]  # Horas * valor hora
    item["custo_total"] = custo
    custo_total += custo
    relatorio.append(item)

custo_por_ha = custo_total / area_total_ha  # Total dividido pela área

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - I.4 Aluguel de Maquinas e Animais", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla o custo com o aluguel de maquinas, implementos ou animais utilizados na lavoura, "
    "calculado com base nas horas contratadas e valores praticados na regiao. O custo total foi proporcionalizado por hectare."
)
pdf.multi_cell(0, 10, descricao)

# Parâmetros usados
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Itens Alugados:", ln=True)
pdf.set_font("Arial", size=12)
for item in relatorio:
    pdf.cell(0, 10, f"Equipamento: {item['equipamento']}", ln=True)
    pdf.cell(0, 10, f"  Horas usadas: {item['horas_usadas']}", ln=True)
    pdf.cell(0, 10, f"  Preço por hora (R$): {item['preco_hora']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Custo total (R$): {item['custo_total']:.2f}", ln=True)
    pdf.ln(2)

# Resultado final
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Custo Total: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"Foram utilizados {len(itens_alugados)} equipamentos alugados na cultura do {cultura}, "
    "em operacoes complementares onde nao foi viavel utilizar bens proprios. O custo foi distribuido pela area cultivada."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "I4_aluguel_maquinas_animais.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
