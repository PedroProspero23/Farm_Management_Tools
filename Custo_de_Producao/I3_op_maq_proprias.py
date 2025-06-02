import os
import getpass
from fpdf import FPDF

# ============================
# DEFINIR VARIÁVEIS GERAIS
# ============================

cultura = "Milho"
area_total_ha = 20.0  # Área total em hectares

# Salário do operador
salario_mensal = 3000.00
encargos_percentual = 0.7
horas_mes = 220  # Carga horária mensal

# ============================
# LISTA DE MÁQUINAS USADAS
# ============================

maquinas = [
    {
        "tipo": "Trator 110cv",
        "valor": 250000.00,
        "vida_util_anos": 10,
        "horas_ano": 1000,
        "horas_utilizadas": 16,
        "consumo_litro_hora": 11,
        "preco_diesel": 5.80,
        "percentual_manutencao": 0.05
    },
    {
        "tipo": "Colhedora",
        "valor": 600000.00,
        "vida_util_anos": 12,
        "horas_ano": 900,
        "horas_utilizadas": 12,
        "consumo_litro_hora": 18,
        "preco_diesel": 5.80,
        "percentual_manutencao": 0.07
    }
]

# ============================
# CÁLCULOS
# ============================

total_custo = 0
relatorio_detalhado = []

for m in maquinas:
    tipo = m["tipo"]
    
    # Depreciação
    deprec_ano = m["valor"] / m["vida_util_anos"]
    deprec_hora = deprec_ano / m["horas_ano"]
    custo_depreciacao = deprec_hora * m["horas_utilizadas"]

    # Combustível
    litros = m["consumo_litro_hora"] * m["horas_utilizadas"]
    custo_combustivel = litros * m["preco_diesel"]

    # Manutenção
    manut_ano = m["valor"] * m["percentual_manutencao"]
    custo_manutencao = (manut_ano / m["horas_ano"]) * m["horas_utilizadas"]

    # Operador
    salario_total = salario_mensal * (1 + encargos_percentual)
    valor_hora_op = salario_total / horas_mes
    custo_operador = valor_hora_op * m["horas_utilizadas"]

    # Soma
    custo_total_maquina = custo_depreciacao + custo_combustivel + custo_manutencao + custo_operador
    total_custo += custo_total_maquina

    # Guardar dados para o relatório
    relatorio_detalhado.append({
        "Máquina": tipo,
        "Horas utilizadas": m["horas_utilizadas"],
        "Depreciação (R$)": custo_depreciacao,
        "Combustível (R$)": custo_combustivel,
        "Manutenção (R$)": custo_manutencao,
        "Operador (R$)": custo_operador,
        "Total Máquina (R$)": custo_total_maquina
    })

# Custo final por hectare
custo_por_ha = total_custo / area_total_ha

# ============================
# GERAR PDF
# ============================

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatorio Tecnico - I.3 Operacao com Maquinas Proprias (Multiplas)", ln=True)

pdf.set_font("Arial", "B", 12)
pdf.ln(6)
pdf.cell(0, 10, "Descricao do Item:", ln=True)
pdf.set_font("Arial", size=12)
descricao = (
    "Este item contempla o custo de utilizacao de tratores, colhedoras e outros equipamentos proprios, "
    "incluindo depreciacao, combustivel, manutencao e operador, considerando o uso de multiplas maquinas na cultura."
)
pdf.multi_cell(0, 10, descricao)

pdf.ln(4)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Parametros Utilizados:", ln=True)

pdf.set_font("Arial", size=12)
for item in relatorio_detalhado:
    pdf.ln(2)
    for k, v in item.items():
        if isinstance(v, float):
            texto = f"{k}: R$ {v:.2f}" if "R$" in k else f"{k}: {v:.2f}"
        else:
            texto = f"{k}: {v}"
        pdf.cell(0, 10, texto, ln=True)
    pdf.ln(2)

pdf.set_font("Arial", "B", 12)
pdf.ln(4)
pdf.cell(0, 10, f"Custo Total de Todas as Máquinas: R$ {total_custo:.2f}", ln=True)
pdf.cell(0, 10, f"Custo Final por ha: R$ {custo_por_ha:.2f}", ln=True)

pdf.ln(6)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Justificativa Tecnica:", ln=True)
pdf.set_font("Arial", size=12)
justificativa = (
    f"Para a cultura do {cultura}, foram utilizadas multiplas maquinas proprias ao longo do ciclo produtivo. "
    "Todos os custos foram proporcionalmente calculados por horas de uso e distribuidos por hectare, conforme metodologia da CONAB."
)
pdf.multi_cell(0, 10, justificativa)

# ============================
# SALVAR EM DOWNLOADS
# ============================

usuario = getpass.getuser()
caminho_pdf = os.path.join("C:/Users", usuario, "Downloads", "I3_maquinas_multiplas.pdf")
pdf.output(caminho_pdf)

print(f"✅ Relatorio salvo em: {caminho_pdf}")
