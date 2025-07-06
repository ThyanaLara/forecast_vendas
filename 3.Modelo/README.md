# Estratégia de Modelagem
No desenvolvimento do modelo preditivo de vendas mensais, incrementei e avaliei o impacto das variáveis adicionando em etapas.  Os principais passos realizados e comentários do processo, são:

 ### **1. Modelo Base (sem engenharia de features)**
Inicialmente, o modelo foi treinado apenas com as colunas originais da base:
 - Variáveis numéricas: onpromotion
 - Variáveis categóricas: store_nbr, family_top6, ano, mes

 | Modelo        | MAE       | RMSE      | R²     |
 |---------------|-----------|-----------|--------|
 | RandomForest  | 2.475,26  | 4.541,07  | 0.7864 |
 | XGBoost       | 2.404,39  | 4.417,45  | 0.7979 |


Os resultados iniciais foram satisfatórios, porém ao avaliar os erros mês a mês, observa-se uma grande diferença entre as vendas previstas e as reais em alguns períodos.

<p align="center">
  <img src="Anexos\mes a mes1.png" alt="tabela" width="90%" />
</p>

###     **2. Primeiras Features Criadas (de calendários e vendas ativas)**
Com base nas primeiras etapas do projeto, adicionei as variáveis externas calculadas anteriormente: qtd_feriados (número de feriados no mês) e dias_ativos_venda (quantidade de dias com movimentação de vendas por loja/família)

Essas variáveis melhoraram a capacidade preditiva do modelo ao incorporar novos comportamentos ao calendário e a frequência de vendas. Resultado otimizou um pouco o RMSE e R² do Random Forest.

| Modelo        | MAE       | RMSE      | R²     |
|---------------|-----------|-----------|--------|
| RandomForest  | 2.466,80  | 4.383,26  | 0.8010 |
| XGBoost       | 2.452,73  | 4.400,30  | 0.7995 |


###     **3. Sazonalidade e Promoção (flags binárias)**
Na tentativa de capturar padrões sazonais e comportamentos comerciais, adicionei novas variáveis binárias: has_promo (se houve promoção no mês), is_fim_ano (meses de novembro e dezembro) e sazonal_forte (meses com maiores erros identificados nos modelos passados)

| Modelo        | MAE       | RMSE      | R²     |
|---------------|-----------|-----------|--------|
| RandomForest  | 2.527,47  | 4.604,63  | 0.7838 |
| XGBoost       | 2.583,36  | 4.636,86  | 0.7807 |

Essas variáveis não melhoraram o modelo, sugerindo que os efeitos sazonais já estam sendo capturados pelas demais Features, ou elas são simplistas demais para representar os padrões reais.

###     **4. Análise Descritiva e Transformações**
Voltando um pouco na análise estatística descritiva (2.Analise Exploratoria), observei que a variável `sales` apresentava alta assimetria, com **média muito maior que a mediana** e valores **máximos extremamente altos** (outliers) e a variável `dias_ativos_venda` apresentava **grande variação mensal**, o que pode induzir o modelo ao erro em meses com menor frequência.

Para lidar com esses pontos, foram aplicadas duas transformações principais:

  - Transformação logarítmica em `sales`: suavizar o impacto dos outliers e melhorar a distribuição dos dados;

  - Criação da variável `variável dias_ativos_venda_lag3`: média móvel da frequência de vendas nos três meses anteriores, permitindo capturar padrões temporais e fornecer ao modelo um senso de memória.

| Modelo        | MAE       | RMSE      | R²     |
|---------------|-----------|-----------|--------|
| RandomForest  | 2.292,95  | 4.632,07  | 0.8948 |
| XGBoost       | 2.132,75  | 4.100,29  | 0.8973 |

Essa última etapa contribuio bastante para a melhora das métricas de avaliação. Mesmo com meses discrepantes como em fevereiro. Abaixo, observa-se o desempenho mensal do modelo com as features selecionadas:
<p align="center">
  <img src="Anexos\mes a mes 2.png" alt="tabela" width="90%" />
</p>

Entre os modelos testados, o XGBoost se destacou por apresentar os melhores resultados em todas as métricas avaliadas. Por isso, foi o algoritmo escolhido para seguir nas próximas etapas do projeto.

Para otimizar os hiperparâmetros, utilizei a técnica GridSearchCV com validação cruzada. Os principais hiperparâmetros ajustados foram:

| Hiperparâmetro     | Descrição                                                 |
|--------------------|------------------------------------------------------------|
| `n_estimators`     | Quantidade de árvores no modelo                           |
| `max_depth`        | Complexidade de cada árvore (profundidade)                |
| `learning_rate`    | Peso de cada nova árvore adicionada                       |
| `subsample`        | Porcentagem das amostras utilizadas por árvore            |
| `colsample_bytree` | Porcentagem das features utilizadas por árvore            |
| `random_state`     | Reprodutibilidade dos resultados                          |
| `n_jobs`           | Número de threads utilizadas para otimizar a performance  |


O resultado foi: *{'max_depth': 5, 'n_estimators': 300,'colsample_bytree': 1.0, 'learning_rate': 0.1, 'subsample': 0.8}*

# Cross Validate com TimeSeriesSplit

Para validar o modelo, utilizei a validação cruzada temporal `TimeSeriesSplit`, com 5 divisões de treino e teste, respeitando a ordem cronológica dos dados. 
O objetivo foi avaliar a **estabilidade e a capacidade de generalização do modelo ao longo do tempo**, simulando diferentes cenários de previsão com base no histórico.

### Resultados por Fold

| Fold | MAE      | RMSE     | R²     |
|------|----------|----------|--------|
| 1    | 1.910,25 | 4.533,59 | 0.7198 |
| 2    | 2.218,77 | 4.585,20 | 0.7598 |
| 3    | 2.254,38 | 3.758,42 | 0.8463 |
| 4    | 2.620,12 | 4.309,74 | 0.8062 |
| 5    | 2.681,02 | 4.139,55 | 0.8296 |

Esse tipo de validação é importante em problemas de séries temporais, pois:analisa como o modelo se comporta em períodos diferentes, ajuda a detectar overfitting e simular melhor a realidade, já que previsões futuras sempre são feitas com base no passado.

### Estatísticas Gerais

- **MAE médio**: 2.336,91  
  O modelo erra, em média, cerca de R$ 2.337 por mês nas previsões de vendas.

- **RMSE médio**: 4.265,30  
  Sensível a valores extremos, o RMSE indica que em meses com desvios maiores o erro pode ultrapassar R$ 4.000.

- **R² médio**: 0.7923  
  Em média, o modelo explica aproximadamente 79,2% da variabilidade das vendas reais ao longo do tempo.


# Interpretação do Modelo com SHAP

Para entender como cada variável influenciou as previsões do modelo XGBoost, utilizei a técnica SHAP (SHapley Additive exPlanations). O gráfico abaixo mostra os **impactos individuais de cada variável** para cada previsão feita pelo modelo:
<p align="center">
  <img src="Anexos\shap.png" alt="tabela" width="70%" />
</p>

Em resumo, o gráfico mostra as variáveis com maior impacto:
- `family_top6_Outros`: teve o maior peso. Famílias de produtos fora do grupo principal tendem a aumentar as vendas previstas.
- `onpromotion`: número de itens em promoção impacta positivamente as previsões.
- `dias_ativos_venda` e `dias_ativos_venda_lag3`: representam a frequência de vendas por mês e são diretamente proporcionais ao volume previsto.
- Variáveis específicas de loja, como `store_nbr_44` e `store_nbr_47`, também apresentaram influência significativa, o que indica comportamento local captado pelo modelo.

Essa análise reforça a relevância das variáveis criadas durante a etapa de feature engineering e mostra que o modelo é sensível a fatores sazonais, promocionais e à composição das famílias de produtos.

# Conclusões Finais





