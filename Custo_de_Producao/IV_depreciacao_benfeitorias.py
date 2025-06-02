import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Soja"
area_total_ha = 120.0  # Área total da lavoura

# ============================
# LISTA DE BENFEITORIAS E INSTALAÇÕES
# ============================

benfeitorias = [
    {
        "descricao": "Galpão de insumos",
        "valor_aquisicao": 90000.00,
        "valor_residual": 9000.00,
        "vida_util_anos": 20,
        "fracao_uso": 0.6  # 60% de uso na cultura de soja
    },
    {
        "descricao": "Poço artesiano",
        "valor_aquisicao": 35000.00,
        "valor_residual": 3500.00,
        "vida_util_anos": 25,
        "fracao_uso": 1.0  # 100% uso na cultura
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for b in benfeitorias:
    depre_ano = (b["valor_aquisicao"] - b["valor_residual"]) / b["vida_util_anos"]
    depre_uso = depre_ano * b["fracao_uso"]
    depre_por_ha = depre_uso / area_total_ha
    b["depreciacao_ano"] = depre_ano
    b["depreciacao_uso"] = depre_uso
    b["depreciacao_ha"] = depre_por_ha
    relatorio.append(b)
    custo_total += depre_uso

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - IV.1 Depreciacao de Benfeitorias e Instalacoes", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item considera a depreciacao de estruturas permanentes da propriedade utilizadas na cultura, "
    "tais como galpoes, depositos e estruturas de irrigacao fixas. Os valores sao proporcionais ao uso na lavoura analisada."
)
pdf.multi_cell(0, 10, descricao)

# Atenção à fração de uso
pdf.ln(2)
pdf.set_font("Arial", "B", 12)
pdf.set_text_color(200, 50, 50)
pdf.cell(0, 10, "ATENCAO:", ln=True)
pdf.set_text_color(0, 0, 0)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10,
    "A depreciação é calculada com base na fracao de uso da estrutura na cultura analisada. "
    "Insira corretamente esse dado para garantir a fidelidade dos custos.")

# Lista de benfeitorias
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Benfeitorias Consideradas:", ln=True)
pdf.set_font("Arial", size=12)
for b in relatorio:
    pdf.cell(0, 10, f"Descricao: {b['descricao']}", ln=True)
    pdf.cell(0, 10, f"  Valor de aquisição: R$ {b['valor_aquisicao']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Valor residual: R$ {b['valor_residual']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Vida útil: {b['vida_util_anos']} anos", ln=True)
    pdf.cell(0, 10, f"  Fração de uso: {b['fracao_uso']*100:.1f}%", ln=True)
    pdf.cell(0, 10, f"  Depreciação anual proporcional: R$ {b['depreciacao_uso']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Total anual de Depreciacao: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"As estruturas utilizadas na producao da lavoura de {cultura} apresentam desgaste tecnico anual, "
    "cujo valor de depreciacao foi calculado com base na vida util e fracao de uso atribuida a esta cultura. "
    "Os valores foram rateados por hectare para fins de composicao do custo operacional total."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "IV1_depreciacao_benfeitorias.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
