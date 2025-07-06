# Estratégia de Modelagem
No desenvolvimento do modelo preditivo de vendas mensais, incrementei e avaliei o impacto das variáveis adicionando em etapas.  Os principais passos realizados e comentários do processo, são:

###     **1. Modelo Base (sem engenharia de features)**
Inicialmente, o modelo foi treinado apenas com as colunas originais da base:

Variáveis numéricas: onpromotion
Variáveis categóricas: store_nbr, family_top6, ano, mes

<p align="center">
  <img src="Anexos\tabela_comparacao1.png" alt="tabela" width="50%" />
</p>

Os resultados iniciais foram satisfatórios, porém ao avaliar os erros mês a mês, observou-se uma grande diferença entre as vendas previstas e as reais em alguns períodos.

<p align="center">
  <img src="Anexos\mes a mes1.png" alt="tabela" width="90%" />
</p>

###     **2. Primeiras Features Criadas (de calendários e vendas ativas)**
Com base nas primeiras etapas do projeto, adicionei as variáveis externas calculadas anteriormente: qtd_feriados (número de feriados no mês) e dias_ativos_venda (quantidade de dias com movimentação de vendas por loja/família)

Essas variáveis melhoraram a capacidade preditiva do modelo ao incorporar novos comportamentos ao calendário e a frequência de vendas. Resultado otimizou um pouco o RMSE e R² do Random Forest.

<p align="center">
  <img src="Anexos\tabela_comparacao2.png" alt="tabela" width="50%" />
</p>


###     **3. Sazonalidade e Promoção (flags binárias)**
Na tentativa de capturar padrões sazonais e comportamentos comerciais, adicionei novas variáveis binárias: has_promo (se houve promoção no mês), is_fim_ano (meses de novembro e dezembro) e sazonal_forte (meses com maiores erros identificados nos modelos passados)

<p align="center">
  <img src="Anexos\tabela_comparacao3.png" alt="tabela" width="50%" />
</p>

Essas variáveis não melhoraram o modelo, sugerindo que os efeitos sazonais já estam sendo capturados capturados pelas demais Features, ou as Features são simplistas para representar os padrões reais.

###     **4. Análise Descritiva e Transformações**
Voltando um pouco na análise estatística descritiva (2.Analise Exploratoria), observei que a variável sales apresentava alta assimetria, com **média muito maior que a mediana** e valores **máximos extremamente altos** (outliers) e a variável dias_ativos_venda apresentava **grande variação mensal**, o que pode induzir o modelo ao erro em meses com menor frequência.

Dessa forma, apliquei a transformação logarítmica em `sales` para suavizar os efeitos dos outliers e criei a `variável dias_ativos_venda_lag3` (média móvel da frequência de vendas nos últimos 3 meses), fornecendo memória temporal ao modelo.

<p align="center">
  <img src="Anexos\tabela_comparacao4.png" alt="tabela" width="50%" />
</p>

Essa última etapa trouxe grande vantagem ao desempenho, melhorando as métricas. Mesmo com meses discrepantes (ex: Fevereiro), esses foram as Features escolhidas.
<p align="center">
  <img src="Anexos\mes a mes 2.png" alt="tabela" width="90%" />
</p>

 O XGBoost se destacou em todas as métricas, e foi selecionado para seguir com os próximos passos

 Escolhi o GridSearchCV para encontrar a melhor combinação de hiperparâmetros para meu modelo por meio de validação cruzada. E os hiperparâmetros escolhidos foram:

 - n_estimators: Quantidade de árvores
 - max_depth: Complexidade de cada árvore (profundidade)
 - learning_rate: Peso de cada árvore nova
 - subsample: % das amostras por árvore
 - colsample_bytree: % das features por árvore
 - random_state: Reprodutibilidade
 - n_jobs: Performance

E o resultado foi: {'max_depth': 5, 'n_estimators': 300,'colsample_bytree': 1.0, 'learning_rate': 0.1, 'subsample': 0.8}

# Cross Validate com TimeSeriesSplit

Para validar a robustez do modelo, foi aplicada validação cruzada temporal (`TimeSeriesSplit`), com 5 divisões crescentes de treino e teste, respeitando a ordem cronológica dos dados. O objetivo foi avaliar a estabilidade do desempenho do modelo ao longo do tempo, simulando diferentes períodos de previsão.

### Resultados por Fold

| Fold | MAE      | RMSE     | R²     |
|------|----------|----------|--------|
| 1    | 1.910,25 | 4.533,59 | 0.7198 |
| 2    | 2.218,77 | 4.585,20 | 0.7598 |
| 3    | 2.254,38 | 3.758,42 | 0.8463 |
| 4    | 2.620,12 | 4.309,74 | 0.8062 |
| 5    | 2.681,02 | 4.139,55 | 0.8296 |

### Estatísticas Gerais

- **MAE médio**: 2.336,91  
  O modelo erra, em média, cerca de R$ 2.337 por mês nas previsões de vendas.

- **RMSE médio**: 4.265,30  
  Sensível a valores extremos, o RMSE indica que em meses com desvios maiores o erro pode ultrapassar R$ 4.000.

- **R² médio**: 0.7923  
  Em média, o modelo explica aproximadamente 79,2% da variabilidade das vendas reais ao longo do tempo.

### Resumo

- Os resultados indicam um bom desempenho e consistência: mesmo com variações mensais, o modelo mantém valores de R² acima de 0.71 em todos os folds.
- Folds com menor erro (como Fold 3 e Fold 5) possivelmente coincidem com períodos mais regulares nas vendas.
- A variação do MAE entre os folds mostra que o modelo ainda possui espaço para melhorias em meses com comportamento atípico.
- O R² médio próximo de 0.80 confirma que o modelo é adequado para uso preditivo mensal, com bom equilíbrio entre performance e generalização.


# Interpretação do Modelo com SHAP

Para entender o funcionamento interno do modelo XGBoost e identificar as variáveis com maior influência nas previsões, utilizamos a técnica SHAP (SHapley Additive exPlanations). O gráfico abaixo mostra os impactos individuais de cada variável para cada previsão feita pelo modelo.
<p align="center">
  <img src="Anexos\shap.png" alt="tabela" width="70%" />
</p>

As variáveis mais importantes foram:

- `family_top6_Outros`: famílias de produtos fora do grupo principal tendem a reduzir as vendas previstas.
- `onpromotion`: número de itens em promoção impacta positivamente as previsões, como esperado.
- `dias_ativos_venda` e `dias_ativos_venda_lag3`: representam a frequência de vendas por mês e são diretamente proporcionais ao volume previsto.
- Variáveis específicas de loja, como `store_nbr_44` e `store_nbr_47`, também apresentaram influência significativa, o que indica comportamento local captado pelo modelo.

A análise reforça a importância das features criadas no processo de engenharia de variáveis e demonstra que o modelo é sensível a fatores sazonais, de promoção e à composição das famílias de produtos.

