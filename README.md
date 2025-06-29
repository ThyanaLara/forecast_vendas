## Objetivo 

Este trabalho tem como objetivo desenvolver um modelo de previsão de vendas mensais (Forecast) por tipo de produto e loja, utilizando Machine Learning nos dados históricos de uma rede de lojas no Equador para identificar padrões que prevejam as vendas futuras. 

O desenvolvimento do projeto seguiu a metodologia CRISP-DM, desde a compreensão do negócio e da base de dados até a preparação dos dados, modelagem, avaliação dos resultados e sugestões para futuras implementações.

Através da análise exploratória de variáveis como promoções, sazonalidade e tipos  e quantidade de feriados, espera-se gerar insights e um modelo preditivo que ajude a construir cenários realistas com base em dados históricos e features de influência para apoiar projeções financeiras mais precisas.

Fonte dos dados está [nesse link](https://www.kaggle.com/c/store-sales-time-series-forecasting/data)



## Overview do Projeto

Na área de FP&A (Financial Planning & Analysis), é normal realizarmos o orçamento anual com antecedência, projetando receitas, custos e volumes. No entanto, por mais detalhado que esse planejamento seja, ele inevitavelmente sofre impactos de fatores externos como a sazonalidade, promoções, feriados e oscilações na demanda do consumidor. 
Assim, confiar apenas no orçamento fixo pode gerar distorções e vieses ao longo do ano, dificultando a análise em tempo real e levando a justificativas recorrentes para variações e erros de phasing no planejamento financeiro.

Nesse contexto o forecast (atualização recorrente das projeções ao longo do ano) ganha relevância estratégica. Com o avanço das tecnologias de dados e modelagem preditiva, tornou-se possível criar modelos de Machine Learning capazes de gerar previsões mais assertivas e adaptáveis, de acordo com múltiplos fatores(dados) e aprendizado contínuo dos dados históricos.

A proposta deste trabalho é justamente desenvolver um modelo de previsão de vendas mensais por loja e família de produtos, utilizando dados reais de uma rede varejista com foco em apoiar e aprimorar os processos da área financeira. Ele visa, não apenas, melhora a precisão das previsões, como também fortalece a capacidade analítica da área de FP&A, promovendo decisões mais rápidas, embasadas e alinhadas com os objetivos estratégicos da organização.


## Bases Utilizadas

# 📁 train.csv (vendas diárias)
Os dados de treino contêm séries temporais com as seguintes variáveis: store_nbr, family, onpromotion e a variável alvo sales.

- date: data da venda por dia
- store_nbr: id da loja onde os produtos foram vendidos
- family: tipo de produto vendido
- sales: representa o total de vendas de uma determinada família de produtos em uma loja específica, em uma data específica
- onpromotion: indica o total de itens da família de produtos que estavam em promoção em uma loja, em uma determinada data

# 📁 holidays_events.csv (feriados)
Contém informações sobre feriados e eventos, juntamente com metadados

- type: caracteristica do feriado (Nacional, regional ou local)
- locale: tipo de feriado (Nacional, regional ou local)
- locale_name: nome da localidade (pode ser: cidade ou estado)
- description: descrição do feriado (Natl, Páscoa...)

# Período de análises: 
**Histórico** (treino):2013, 2014 e 2015
**Previsão**: 2016


## Tratamento inicial dos dados 
Antes de iniciar a análise exploratória e a modelagem, foi realizado um tratamento inicial nas base:

- Integração das bases de vendas e feriados: As duas fontes foram cruzadas para calcular, por uma lógica em Python, a quantidade de feriados em cada mês, considerando o tipo (nacional, regional ou local) e a cidade de cada loja.
- Agregação mensal: Como a base original é diária, os dados foram agrupados por loja, família e mês, resultando em uma base consolidada para previsão mensal. Nessa etapa, foram calculadas:
    - Vendas totais (sales) por mês;
    - Ticket médio (tkm), obtido pela divisão da receita pelo volume vendido;
    - Quantidade de feriados (qtd_feriados) no mês, conforme a localidade da loja.
- Tratamento de valores ausentes e zeros: Os valores nulos e igual a zero em variáveis como vendas, tkm e promoções foram substituídos por 0.1. Essa escolha teve dois objetivos:
    - Evitar erros técnicos em cálculos como logaritmos e divisões;
    - Preservar a estrutura completa da série temporal, garantindo que todas as combinações de loja e família estivessem presentes em todos os meses, o que é essencial para análises de sazonalidade, criação de lags e janelas móveis.