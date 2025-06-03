import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# -------- CONFIGURAÇÕES --------
np.random.seed(42)
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Receita estimada
receita_total = 500_000
mes_recebimento = 3  # Março do ano seguinte (índice 2)

# Custos mensais planejados (desembolso da safra)
custos_mensais = {
    'Ago': 50_000,  # preparo
    'Set': 70_000,  # sementes + plantio
    'Out': 40_000,  # adubação
    'Nov': 30_000,  # defensivos
    'Dez': 20_000,  # manejo
    'Jan': 10_000,  # tratos finais
    'Fev': 30_000,  # colheita
}

# Saldo inicial de caixa
saldo_inicial = 100_000

# -------- GERANDO O FLUXO DE CAIXA --------
caixa_mensal = []
saldo = saldo_inicial

for i, mes in enumerate(meses):
    custo = custos_mensais.get(mes, 0)
    receita = receita_total if i == mes_recebimento else 0
    fluxo = receita - custo
    saldo += fluxo
    caixa_mensal.append({'Mês': mes, 'Receita': receita, 'Custo': custo, 'Fluxo': fluxo, 'Saldo': saldo})

df = pd.DataFrame(caixa_mensal)

# -------- VISUALIZAÇÃO --------
plt.figure(figsize=(10, 6))
plt.plot(df['Mês'], df['Saldo'], marker='o', label='Saldo de Caixa')
plt.bar(df['Mês'], df['Fluxo'], color='gray', alpha=0.5, label='Fluxo do mês')
plt.axhline(0, color='red', linestyle='--')
plt.title("Fluxo de Caixa - Ciclo da Safra (Soja)")
plt.xlabel("Mês")
plt.ylabel("R$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# -------- TABELA RESUMO --------
print(df.to_string(index=False))
