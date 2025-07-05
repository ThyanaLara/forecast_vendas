## Objetivo 

Este trabalho tem como objetivo desenvolver um modelo de previsão de vendas mensais (Forecast) por tipo de produto e loja, utilizando Machine Learning nos dados históricos de uma rede de lojas no Equador para identificar padrões que prevejam as vendas futuras.

O desenvolvimento seguiu a metodologia CRISP-DM, desde a compreensão do negócio e da base de dados até a preparação dos dados, modelagem, avaliação dos resultados e sugestões para futuras implementações.

Fonte dos dados está [nesse link](https://www.kaggle.com/c/store-sales-time-series-forecasting/data)


## Overview do Projeto

No contexto da área de FP&A, embora o orçamento anual seja elaborado com antecedência para projetar receitas, custos e volumes, ele frequentemente é impactado por fatores externos como sazonalidade, promoções, feriados e variações de demanda, o que pode comprometer a precisão do planejamento ao longo do ano. Por isso, o uso de forecast — revisões e atualizações periódicas das projeções — torna-se essencial para uma análise mais realista.

Com os avanços em ciência de dados, é possível aplicar modelos de Machine Learning para gerar previsões mais precisas e adaptáveis, de acordo com múltiplos fatores(dados) e aprendizado contínuo dos dados históricos.

Este trabalho propõe o desenvolvimento de um modelo preditivo de vendas mensais por loja e família de produtos, baseado em dados, com o objetivo de gerar insights para os processos financeiros,  aumentar a precisão das previsões, construir cenários realistas e fortalecer a capacidade analítica da área de FP&A para decisões mais ágeis e estratégicas.


## Bases Utilizadas

### 📁 train.csv (vendas diárias)
Os dados de treino contêm séries temporais com as seguintes variáveis: store_nbr, family, onpromotion e a variável alvo sales.

### 📁 holidays_events.csv (feriados)
Contém informações sobre feriados e eventos, juntamente com metadados

### 📁 store.csv (loja)
Contém informações sobre feriados e eventos, juntamente com metadados


## Dicionário de Dados
O dicionário completo está disponível [aqui](./DICIONARIO).
