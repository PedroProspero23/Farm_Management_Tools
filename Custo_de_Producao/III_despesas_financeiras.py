import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Soja"
area_total_ha = 90.0  # Área total da lavoura

# ============================
# LISTA DE FINANCIAMENTOS
# ============================

financiamentos = [
    {
        "descricao": "Crédito de custeio - Banco do Brasil",
        "valor_financiado": 50000.00,
        "taxa_juros_anual": 0.08,  # 8% ao ano
        "dias_do_financiamento": 180
    },
    {
        "descricao": "Investimento em maquinário agrícola",
        "valor_financiado": 30000.00,
        "taxa_juros_anual": 0.12,
        "dias_do_financiamento": 240
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for f in financiamentos:
    encargos = f["valor_financiado"] * f["taxa_juros_anual"] * (f["dias_do_financiamento"] / 365)
    f["encargos"] = encargos
    relatorio.append(f)
    custo_total += encargos

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - III.1 Despesas Financeiras (Creditos Rurais)", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla os encargos financeiros pagos em decorrencia de operacoes de credito rural, "
    "como juros e taxas sobre financiamentos destinados ao custeio, investimento ou comercializacao da producao."
)
pdf.multi_cell(0, 10, descricao)

# Lista de financiamentos
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Operacoes Consideradas:", ln=True)
pdf.set_font("Arial", size=12)
for f in relatorio:
    pdf.cell(0, 10, f"Descricao: {f['descricao']}", ln=True)
    pdf.cell(0, 10, f"  Valor financiado: R$ {f['valor_financiado']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Taxa de juros anual: {f['taxa_juros_anual']*100:.2f}%", ln=True)
    pdf.cell(0, 10, f"  Dias de financiamento: {f['dias_do_financiamento']} dias", ln=True)
    pdf.cell(0, 10, f"  Encargos financeiros: R$ {f['encargos']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Total de Encargos Financeiros: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"A lavoura de {cultura} utilizou financiamentos que geraram encargos financeiros calculados proporcionalmente "
    "ao prazo de uso dos recursos, os quais foram incorporados ao custo operacional total conforme a metodologia da CONAB."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "III1_despesas_financeiras.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
