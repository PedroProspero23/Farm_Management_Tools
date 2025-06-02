import os
import getpass
from fpdf import FPDF

# ============================
# VARIÁVEIS GERAIS
# ============================

cultura = "Soja"
area_total_ha = 25.0  # Área total cultivada

encargos_percentual = 0.7  # 70% de encargos sobre o salário

# ============================
# LISTA DE FUNCIONÁRIOS
# ============================

funcionarios = [
    {
        "nome": "José",
        "tipo": "diarista",
        "dias_trabalhados": 12,
        "valor_diaria": 130.00
    },
    {
        "nome": "Pedro",
        "tipo": "mensalista",
        "salario_mensal": 2800.00,
        "dias_trabalhados": 15,
        "dias_uteis_mes": 22
    },
    {
        "nome": "Administrador da propriedade",
        "tipo": "administrador",
        "valor_referencia": 3500.00  # Valor imputado ou contratado
    }
]

# ============================
# CÁLCULOS
# ============================

relatorio = []
custo_total = 0

for f in funcionarios:
    if f["tipo"] == "diarista":
        custo = f["dias_trabalhados"] * f["valor_diaria"] * (1 + encargos_percentual)
        f["custo_total"] = custo
        relatorio.append(f)

    elif f["tipo"] == "mensalista":
        salario_com_encargos = f["salario_mensal"] * (1 + encargos_percentual)
        proporcao = f["dias_trabalhados"] / f["dias_uteis_mes"]
        custo = salario_com_encargos * proporcao
        f["custo_total"] = custo
        relatorio.append(f)

    elif f["tipo"] == "administrador":
        custo = f["valor_referencia"] * (1 + encargos_percentual)
        f["custo_total"] = custo
        relatorio.append(f)

    custo_total += f["custo_total"]

custo_por_ha = custo_total / area_total_ha

# ============================
# PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - I.5 Mao de Obra e Administrador Rural", ln=True)

# Descrição técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item considera os custos com trabalhadores rurais contratados por diária ou salário, "
    "bem como o custo (real ou imputado) do administrador da propriedade. Encargos sociais foram aplicados sobre os valores."
)
pdf.multi_cell(0, 10, descricao)

# Parâmetros usados
pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Mao de Obra Utilizada:", ln=True)
pdf.set_font("Arial", size=12)
for f in relatorio:
    pdf.cell(0, 10, f"Nome: {f['nome']} ({f['tipo']})", ln=True)
    if f["tipo"] == "diarista":
        pdf.cell(0, 10, f"  Dias: {f['dias_trabalhados']}, Diária: R$ {f['valor_diaria']:.2f}", ln=True)
    elif f["tipo"] == "mensalista":
        pdf.cell(0, 10, f"  Salário: R$ {f['salario_mensal']:.2f}, Dias trabalhados: {f['dias_trabalhados']}", ln=True)
    elif f["tipo"] == "administrador":
        pdf.cell(0, 10, f"  Valor referência: R$ {f['valor_referencia']:.2f}", ln=True)
    pdf.cell(0, 10, f"  Custo total (R$): {f['custo_total']:.2f}", ln=True)
    pdf.ln(2)

# Resultados finais
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Custo Total da Mao de Obra: R$ {custo_total:.2f}", ln=True)
pdf.cell(0, 10, f"Custo por ha: R$ {custo_por_ha:.2f}", ln=True)

# Justificativa técnica
pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"Foram contratados trabalhadores e administrador para a cultura de {cultura}, com jornadas diferenciadas. "
    "Os custos foram ajustados com base nos encargos e proporcionais à área trabalhada, conforme a metodologia CONAB."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "I5_mao_obra_administrador.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
