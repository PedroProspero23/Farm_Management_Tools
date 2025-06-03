import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# -------- ENTRADA DE CONTRATOS --------
contratos = pd.DataFrame([
    ['Gado de Corte', '2025-01-10', 150000, 0.13, 'simples', 12, 3, 'anual'],
    ['Cana-de-Açúcar', '2025-03-15', 300000, 0.11, 'composto', 6, 4, 'anual'],
    ['Milho', '2025-02-01', 100000, 0.12, 'simples', 0, 6, 'mensal'],
    ['Batata', '2025-04-20', 90000, 0.14, 'composto', 3, 3, 'mensal']
], columns=['Atividade', 'Data de Entrada', 'Valor (R$)', 'Taxa Juros Anual', 'Tipo de Juros',
            'Carência (meses)', 'Parcelas', 'Periodicidade'])

contratos['Data de Entrada'] = pd.to_datetime(contratos['Data de Entrada'])

# -------- GERAÇÃO DAS PARCELAS --------
parcelas_todas = []

for _, row in contratos.iterrows():
    atividade = row['Atividade']
    entrada = row['Data de Entrada']
    valor = row['Valor (R$)']
    taxa = row['Taxa Juros Anual']
    tipo_juros = row['Tipo de Juros']
    carencia = row['Carência (meses)']
    parcelas = row['Parcelas']
    periodicidade = row['Periodicidade']

    if periodicidade == 'anual':
        intervalo = pd.DateOffset(years=1)
        t = 1
    else:
        intervalo = pd.DateOffset(months=1)
        t = 1 / 12

    data_base = entrada + pd.DateOffset(months=carencia)

    if tipo_juros == 'simples':
        prazo_total = t * parcelas
        juros_total = valor * taxa * prazo_total
        valor_total = valor + juros_total
        parcela_valor = round(valor_total / parcelas, 2)
    elif tipo_juros == 'composto':
        taxa_periodica = (1 + taxa) ** t - 1
        parcela_valor = round(valor * taxa_periodica / (1 - (1 + taxa_periodica) ** -parcelas), 2)

    for i in range(parcelas):
        vencimento = data_base + intervalo * i
        parcelas_todas.append([atividade, vencimento, parcela_valor])

parcelas_df = pd.DataFrame(parcelas_todas, columns=['Atividade', 'Data de Pagamento', 'Parcela (R$)'])
parcelas_df['Data de Pagamento'] = pd.to_datetime(parcelas_df['Data de Pagamento'])

# -------- CRIAR BASE MENSAL COMPLETA --------
data_inicio = parcelas_df['Data de Pagamento'].min().replace(day=1)
data_fim = parcelas_df['Data de Pagamento'].max().replace(day=1)
todos_os_meses = pd.date_range(data_inicio, data_fim, freq='MS')
atividades = contratos['Atividade'].unique().tolist()

# Criar base com todas combinações de meses x atividades
base = pd.MultiIndex.from_product([todos_os_meses, atividades], names=['Data', 'Atividade']).to_frame(index=False)
parcelas_df['Data'] = parcelas_df['Data de Pagamento'].dt.to_period('M').dt.to_timestamp()
base['Data'] = base['Data'].dt.to_period('M').dt.to_timestamp()

# Somar parcelas por mês/atividade e combinar
pagamentos = parcelas_df.groupby(['Data', 'Atividade'])['Parcela (R$)'].sum().reset_index()
fluxo = pd.merge(base, pagamentos, on=['Data', 'Atividade'], how='left').fillna(0)

# Pivot para gráfico
fluxo_plot = fluxo.pivot(index='Data', columns='Atividade', values='Parcela (R$)')
fluxo_plot['Total'] = fluxo_plot.sum(axis=1)

# -------- GRÁFICO --------
plt.figure(figsize=(14, 6))
bottom = np.zeros(len(fluxo_plot))

for atividade in atividades:
    valores = fluxo_plot[atividade].values
    plt.bar(fluxo_plot.index.strftime('%b/%Y'), valores, bottom=bottom, label=atividade)
    bottom += valores

plt.title("Parcelas de Empréstimos por Atividade e Tipo de Contrato")
plt.xlabel("Mês/Ano")
plt.ylabel("Valor das Parcelas (R$)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", ".")))
plt.tight_layout()
plt.show()
