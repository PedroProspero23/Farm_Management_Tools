import os
import getpass
from fpdf import FPDF

# ============================
# DEFINIR VARIÁVEIS AQUI
# ============================

cultura = "Feijao"
area_total_ha = 8.0

tipo_animal = "Boi"
quantidade_animais = 2
dias_trabalho_total = 12

# Custo mensal por animal
alimentacao_mensal = 300.00
saude_mensal = 40.00
equipamentos_mensal = 25.00
outros_mensal = 20.00
dias_trabalho_mes = 20

# Justificativa técnica
justificativa = (
    f"Foram utilizados {quantidade_animais} {tipo_animal.lower()}s durante {dias_trabalho_total} dias "
    f"na cultura do {cultura}, especialmente para tracao e transporte. "
    "O custo da diaria foi estimado a partir dos custos mensais medios com alimentacao, saude, manutencao e equipamentos, "
    "distribuidos conforme dias efetivamente trabalhados por mes."
)

# ============================
# CÁLCULOS
# ============================

custo_mensal_animal = alimentacao_mensal + saude_mensal + equipamentos_mensal + outros_mensal
custo_diaria = custo_mensal_animal / dias_trabalho_mes
diarias_total = quantidade_animais * dias_trabalho_total
diarias_por_ha = diarias_total / area_total_ha
custo_total_ha = diarias_por_ha * custo_diaria

# ============================
# DADOS PARA RELATÓRIO
# ============================

dados = {
    "Cultura": cultura,
    "Área Total (ha)": area_total_ha,
    "Tipo de Animal": tipo_animal,
    "Quantidade de Animais": quantidade_animais,
    "Dias de Trabalho Total": dias_trabalho_total,
    "Custo Mensal por Animal (R$)": custo_mensal_animal,
    "Dias Trabalhados por Mês": dias_trabalho_mes,
    "Custo por Diária (R$)": custo_diaria,
    "Total de Diárias": diarias_total,
    "Diárias por ha": diarias_por_ha,
    "Custo Total por ha (R$)": custo_total_ha
}

# ============================
# GERAR PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - I.1 Operacao com Animal", ln=True)

# Descrição do item (da norma)
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item considera os custos relacionados a utilizacao de tracao animal na lavoura, "
    "como transporte, preparo de solo ou movimentacao de insumos, calculados com base em "
    "numero de diarias e custo por diaria de manutencao e uso do animal."
)
pdf.multi_cell(0, 10, descricao)

# Dados técnicos
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Parametros Utilizados:", ln=True)
pdf.set_font("Arial", size=12)
for chave, valor in dados.items():
    if isinstance(valor, float):
        texto = f"{chave}: R$ {valor:.2f}" if "R$" in chave or "Custo" in chave else f"{chave}: {valor:.2f}"
    else:
        texto = f"{chave}: {valor}"
    pdf.cell(0, 10, texto, ln=True)

# Justificativa
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR EM DOWNLOADS
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "I1_operacao_com_animal.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
