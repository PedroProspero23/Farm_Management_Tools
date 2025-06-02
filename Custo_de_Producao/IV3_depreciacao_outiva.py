import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Cana-de-açúcar"
area_total_ha = 100.0  # Área total do cultivo

# ============================
# DADOS DO CULTIVO EM OUTIVA
# ============================

cultivos_outiva = [
    {
        "descricao": "Implantação de cana-de-açúcar soqueira (3 cortes)",
        "custo_implantacao": 9000.00,  # Custo total por hectare
        "vida_util_anos": 3,
        "fracao_area_em_producao": 1.0  # 100% da área já em produção
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for c in cultivos_outiva:
    depre_ano = c["custo_implantacao"] / c["vida_util_anos"]
    depre_uso = depre_ano * c["fracao_area_em_producao"]
    depre_por_ha = depre_uso / area_total_ha
    c["depreciacao_ano"] = depre_ano
    c["depreciacao_uso"] = depre_uso
    c["depreciacao_ha"] = depre_por_ha
    relatorio.append(c)
    custo_total += depre_uso

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - IV.3 Depreciacao de Cultivos em Outiva", ln=True)

# Descrição
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla a depreciacao do custo de implantacao de culturas perenes ou semiperenes, "
    "como cana-de-acucar soqueira, cafe e frutas. O valor deve ser anualizado conforme vida util produtiva."
)
pdf.multi_cell(0, 10, descricao)

# Alerta técnico
pdf.ln(2)
pdf.set_font("Arial", "B", 12)
pdf.set_text_color(200, 50, 50)
pdf.cell(0, 10, "ATENCAO:", ln=True)
pdf.set_text_color(0, 0, 0)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10,
    "A fracao da area em producao permite ajustar o valor da depreciação conforme a proporção efetiva de uso da lavoura. "
    "Muito útil quando a plantação ainda está se estabelecendo.")

# Lista de cultivos
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Cultivos Considerados:", ln=True)
pdf.set_font("Arial", size=12)
for c in relatorio:
    pdf.cell(0, 10, f"Descricao: {c['descricao']}", ln=True)
    pdf.cell(0, 10, f"  Custo de implantacao (R$/ha): R$ {c['custo_implantacao']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Vida util: {c['vida_util_anos']} anos", ln=True)
    pdf.cell(0, 10, f"  Fracao da area em producao: {c['fracao_area_em_producao']*100:.1f}%", ln=True)
    pdf.cell(0, 10, f"  Depreciacao anual: R$ {c['depreciacao_ano']:.2f}", ln=True)
    pdf.ln(2)

# Resultado
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Total anual de Depreciacao: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"A cultura de {cultura}, por ser semiperene, requer a depreciacao do custo de implantacao ao longo de sua vida util. "
    "Neste relatorio, o valor foi proporcionalmente ajustado pela area efetivamente em producao e dividido por hectare."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "IV3_depreciacao_outiva.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
