import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Soja"
area_total_ha = 110.0  # Área da cultura

# ============================
# LISTA DE MÁQUINAS E IMPLEMENTOS
# ============================

maquinas = [
    {
        "descricao": "Trator Massey 70cv",
        "valor_aquisicao": 150000.00,
        "valor_residual": 30000.00,
        "vida_util_anos": 15,
        "fracao_uso": 0.7  # 70% de uso na soja
    },
    {
        "descricao": "Pulverizador Costal Motorizado",
        "valor_aquisicao": 8000.00,
        "valor_residual": 1000.00,
        "vida_util_anos": 8,
        "fracao_uso": 1.0  # 100% soja
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for m in maquinas:
    depre_ano = (m["valor_aquisicao"] - m["valor_residual"]) / m["vida_util_anos"]
    depre_uso = depre_ano * m["fracao_uso"]
    depre_por_ha = depre_uso / area_total_ha
    m["depreciacao_ano"] = depre_ano
    m["depreciacao_uso"] = depre_uso
    m["depreciacao_ha"] = depre_por_ha
    relatorio.append(m)
    custo_total += depre_uso

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - IV.2 Depreciacao de Maquinas e Implementos", ln=True)

# Descrição
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item considera a depreciacao tecnica anual de maquinas, equipamentos e sistemas de irrigacao "
    "utilizados na cultura agricola em estudo. A fracao de uso deve refletir a participacao do bem na lavoura analisada."
)
pdf.multi_cell(0, 10, descricao)

# Alerta
pdf.ln(2)
pdf.set_font("Arial", "B", 12)
pdf.set_text_color(200, 50, 50)
pdf.cell(0, 10, "ATENCAO:", ln=True)
pdf.set_text_color(0, 0, 0)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10,
    "A fracao de uso informa qual parte da depreciação anual do bem é atribuída à cultura considerada. "
    "Essa proporcao é essencial para evitar distorcoes no custo operacional.")

# Lista
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Maquinas e Equipamentos:", ln=True)
pdf.set_font("Arial", size=12)
for m in relatorio:
    pdf.cell(0, 10, f"Descricao: {m['descricao']}", ln=True)
    pdf.cell(0, 10, f"  Valor de aquisição: R$ {m['valor_aquisicao']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Valor residual: R$ {m['valor_residual']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Vida útil: {m['vida_util_anos']} anos", ln=True)
    pdf.cell(0, 10, f"  Fração de uso: {m['fracao_uso']*100:.1f}%", ln=True)
    pdf.cell(0, 10, f"  Depreciação anual proporcional: R$ {m['depreciacao_uso']:.2f}", ln=True)
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
    f"A cultura de {cultura} utiliza equipamentos especificos cuja depreciação tecnica foi considerada "
    "com base na fracao de uso real desses bens na lavoura. Isso garante acuracia no custo operacional total."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "IV2_depreciacao_maquinas.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
