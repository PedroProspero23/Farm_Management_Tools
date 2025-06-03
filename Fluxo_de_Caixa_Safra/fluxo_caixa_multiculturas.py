import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

np.random.seed(42)

meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

saldo_inicial = 80_000

# -------- CONFIGURAÇÃO DAS CULTURAS --------
culturas = {
    'Soja': {
        'receita_total': 500_000,
        'mes_recebimento': 'Mar',
        'custos': {
            'Ago': 50_000, 'Set': 70_000, 'Out': 40_000,
            'Nov': 30_000, 'Dez': 20_000, 'Jan': 10_000, 'Fev': 30_000
        }
    },
    'Milho 2ª Safra': {
        'receita_total': 300_000,
        'mes_recebimento': 'Ago',
        'custos': {
            'Fev': 30_000, 'Mar': 50_000, 'Abr': 30_000,
            'Mai': 25_000, 'Jun': 15_000, 'Jul': 10_000
        }
    }
}

# -------- CALCULAR FLUXO MENSAL --------
caixa_mensal = []
saldo = saldo_inicial

for mes in meses:
    receita_total = 0
    custo_total = 0

    for cultura, dados in culturas.items():
        if mes == dados['mes_recebimento']:
            receita_total += dados['receita_total']
        custo_total += dados['custos'].get(mes, 0)

    fluxo = receita_total - custo_total
    saldo += fluxo

    caixa_mensal.append({
        'Mês': mes,
        'Receita Total': receita_total,
        'Custo Total': custo_total,
        'Fluxo do Mês': fluxo,
        'Saldo de Caixa': saldo
    })

df = pd.DataFrame(caixa_mensal)

# -------- VISUALIZAÇÃO --------
plt.figure(figsize=(12, 6))
plt.plot(df['Mês'], df['Saldo de Caixa'], marker='o', label='Saldo de Caixa')
plt.bar(df['Mês'], df['Fluxo do Mês'], color='gray', alpha=0.5, label='Fluxo Mensal')
plt.axhline(0, color='red', linestyle='--')
plt.title("Fluxo de Caixa com Múltiplas Culturas (Soja + Milho)")
plt.xlabel("Mês")
plt.ylabel("R$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# -------- TABELA --------
print(df.to_string(index=False))
