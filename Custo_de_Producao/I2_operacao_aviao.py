import os
import getpass
from fpdf import FPDF

# ============================
# DEFINIR VARIÁVEIS AQUI
# ============================

cultura = "Soja"
area_total_ha = 12.0

numero_aplicacoes = 3
preco_aplicacao = 85.00  # R$ por aplicação aérea

# Justificativa técnica
justificativa = (
    f"Foram realizadas {numero_aplicacoes} aplicacoes aereas durante o ciclo da cultura da {cultura}, "
    "incluindo operacoes para controle de pragas, doencas e plantas daninhas. "
    f"O preco medio por aplicacao foi de R$ {preco_aplicacao:.2f}, conforme praticado na regiao."
)

# ============================
# CÁLCULO
# ============================

custo_total_ha = numero_aplicacoes * preco_aplicacao

# ============================
# DADOS PARA RELATÓRIO
# ============================

dados = {
    "Cultura": cultura,
    "Área Total (ha)": area_total_ha,
    "Número de Aplicações": numero_aplicacoes,
    "Preço por Aplicação (R$)": preco_aplicacao,
    "Custo Total por ha (R$)": custo_total_ha
}

# ============================
# GERAR PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - I.2 Operacao com Aviao", ln=True)

# Descrição do item (da norma)
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla os custos com aplicacoes aereas realizadas durante o ciclo produtivo da lavoura, "
    "calculados com base no numero de aplicacoes por hectare e no preco medio praticado na regiao para esse tipo de servico."
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
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "I2_operacao_com_aviao.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
