import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

np.random.seed(42)

meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

saldo_inicial = 80_000

# -------- CULTURAS --------
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

# -------- DETALHAMENTO DO EMPRÉSTIMO --------
valor_emprestado = 150_000
taxa_juros_anual = 0.10
parcelas_meses = ['Mar', 'Ago']
n_parcelas = len(parcelas_meses)

# Cálculo simples de juros totais (juros simples proporcional)
juros_total = valor_emprestado * taxa_juros_anual * (5/12 + 10/12) / 2  # média dos prazos
total_a_pagar = valor_emprestado + juros_total
valor_parcela = total_a_pagar / n_parcelas

emprestimos = {
    'Set': valor_emprestado
}

parcelas = {mes: valor_parcela for mes in parcelas_meses}

# -------- FLUXO DE CAIXA --------
caixa_mensal = []
saldo = saldo_inicial

for mes in meses:
    receita_total = 0
    custo_total = 0
    entrada_emprestimo = emprestimos.get(mes, 0)
    pagamento_parcela = parcelas.get(mes, 0)

    for cultura, dados in culturas.items():
        if mes == dados['mes_recebimento']:
            receita_total += dados['receita_total']
        custo_total += dados['custos'].get(mes, 0)

    fluxo = receita_total + entrada_emprestimo - custo_total - pagamento_parcela
    saldo += fluxo

    caixa_mensal.append({
        'Mês': mes,
        'Receita': receita_total,
        'Custo': custo_total,
        'Empréstimo': entrada_emprestimo,
        'Parcela': pagamento_parcela,
        'Fluxo': fluxo,
        'Saldo': saldo
    })

df = pd.DataFrame(caixa_mensal)

# -------- VISUALIZAÇÃO MELHORADA --------
plt.figure(figsize=(14, 7))

plt.bar(df['Mês'], df['Receita'], color='green', alpha=0.6, label='Receita')
plt.bar(df['Mês'], -df['Custo'], color='gray', alpha=0.5, label='Custo Operacional')
plt.bar(df['Mês'], df['Empréstimo'], color='blue', alpha=0.6, label='Empréstimo')
plt.bar(df['Mês'], -df['Parcela'], color='red', alpha=0.6, label='Parcela Empréstimo')

# Linha do saldo acumulado
plt.plot(df['Mês'], df['Saldo'], color='black', marker='o', label='Saldo de Caixa')

plt.axhline(0, color='black', linestyle='--')
plt.title("Fluxo de Caixa com Financiamento Detalhado")
plt.ylabel("R$ (positivo = entrada / negativo = saída)")
plt.xlabel("Mês")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# -------- TABELA RESUMO --------
print("🧾 RESUMO DO EMPRÉSTIMO")
print(f"Valor emprestado: R$ {valor_emprestado:,.2f}")
print(f"Juros totais estimados: R$ {juros_total:,.2f}")
print(f"Total a pagar: R$ {total_a_pagar:,.2f}")
print(f"Parcelas: {n_parcelas}x de R$ {valor_parcela:,.2f}")
print("\n📊 FLUXO DE CAIXA MENSAL:")
print(df.to_string(index=False))
