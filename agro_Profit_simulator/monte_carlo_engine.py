import numpy as np
import pandas as pd

class Farmer:
    def __init__(self, hectares=100, custo_fixo=20000,
                 media_custo_soja=2500, media_custo_milho=3000,
                 variacao_custo_soja=0.05, variacao_custo_milho=0.05,
                 media_prod_soja=55, media_prod_milho=140,
                 variacao_prod_soja=5, variacao_prod_milho=10):

        self.hectares = hectares
        self.custo_fixo = custo_fixo
        self.media_custo_soja = media_custo_soja
        self.media_custo_milho = media_custo_milho
        self.variacao_custo_soja = variacao_custo_soja
        self.variacao_custo_milho = variacao_custo_milho
        self.media_prod_soja = media_prod_soja
        self.media_prod_milho = media_prod_milho
        self.variacao_prod_soja = variacao_prod_soja
        self.variacao_prod_milho = variacao_prod_milho

    def alocar_culturas(self, proporcao_soja):
        ha_soja = self.hectares * proporcao_soja
        ha_milho = self.hectares * (1 - proporcao_soja)
        return ha_soja, ha_milho

    def calcular_producao(self, ha_soja, ha_milho):
        perda_soja = np.random.triangular(0.0, 0.05, 0.3)
        perda_milho = np.random.triangular(0.0, 0.05, 0.3)

        prod_soja_ha = max(0, np.random.normal(self.media_prod_soja, self.variacao_prod_soja))
        prod_milho_ha = max(0, np.random.normal(self.media_prod_milho, self.variacao_prod_milho))

        prod_total_soja = ha_soja * prod_soja_ha * (1 - perda_soja)
        prod_total_milho = ha_milho * prod_milho_ha * (1 - perda_milho)

        return prod_total_soja, prod_total_milho, perda_soja, perda_milho

    def calcular_custos_variaveis(self):
        custo_soja_real = np.random.normal(self.media_custo_soja, self.media_custo_soja * self.variacao_custo_soja)
        custo_milho_real = np.random.normal(self.media_custo_milho, self.media_custo_milho * self.variacao_custo_milho)
        return max(0, custo_soja_real), max(0, custo_milho_real)

    def calcular_custo_total(self, custo_soja_real, custo_milho_real):
        return self.custo_fixo + (custo_soja_real + custo_milho_real) * self.hectares


class MonteCarloSimulator:
    def __init__(self, preco_soja_medio=140.0, preco_milho_medio=80.0,
                 variacao_preco_soja=0.15, variacao_preco_milho=0.10, iteracoes=1000):
        self.preco_soja_medio = preco_soja_medio
        self.preco_milho_medio = preco_milho_medio
        self.variacao_preco_soja = variacao_preco_soja
        self.variacao_preco_milho = variacao_preco_milho
        self.iteracoes = iteracoes
        self.resultados = []

    def simular(self, fazendeiro: Farmer):
        for _ in range(self.iteracoes):
            proporcao_soja = np.random.uniform(0, 1)

            ha_soja, ha_milho = fazendeiro.alocar_culturas(proporcao_soja)
            prod_soja, prod_milho, perda_soja, perda_milho = fazendeiro.calcular_producao(ha_soja, ha_milho)

            preco_soja_real = max(0, np.random.normal(self.preco_soja_medio, self.preco_soja_medio * self.variacao_preco_soja))
            preco_milho_real = max(0, np.random.normal(self.preco_milho_medio, self.preco_milho_medio * self.variacao_preco_milho))

            custo_soja_real, custo_milho_real = fazendeiro.calcular_custos_variaveis()
            custo_total = fazendeiro.calcular_custo_total(custo_soja_real, custo_milho_real)

            receita = prod_soja * preco_soja_real + prod_milho * preco_milho_real
            lucro = receita - custo_total

            self.resultados.append({
                'proporcao_soja': proporcao_soja,
                'producao_soja': prod_soja,
                'producao_milho': prod_milho,
                'perda_soja': perda_soja,
                'perda_milho': perda_milho,
                'preco_soja': preco_soja_real,
                'preco_milho': preco_milho_real,
                'custo_soja_ha': custo_soja_real,
                'custo_milho_ha': custo_milho_real,
                'receita': receita,
                'custo_total': custo_total,
                'lucro': lucro
            })

        return pd.DataFrame(self.resultados)
