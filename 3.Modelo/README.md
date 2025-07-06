# Estratégia de Modelagem
Durante o desenvolvimento do modelo preditivo de vendas mensais, adotou-se uma abordagem incremental, avaliando o impacto da adição de variáveis, transformação de dados e técnicas de validação. A seguir, descrevem-se os principais passos realizados e os aprendizados ao longo do processo.

###     **1. Modelo Base (sem engenharia de features)**
Inicialmente, foi treinado um modelo utilizando apenas as colunas originais da base:

Variáveis numéricas: onpromotion

Variáveis categóricas: store_nbr, family_top6, ano, mes

<p align="center">
  <img src="Anexos\tabela_comparacao1.png" alt="tabela" width="50%" />
</p>

Observação: os resultados iniciais foram satisfatórios, porém ao avaliar os erros mês a mês, observou-se uma grande discrepância entre as vendas previstas e as reais em determinados períodos.

<p align="center">
  <img src="Anexos\mes a mes1.png" alt="tabela" width="90%" />
</p>

###     **2. Primeiras Features Criadas (de calendários e vendas ativas)**
Com base em análises complementares, adicionaram-se variáveis externas:

qtd_feriados: número de feriados no mês

dias_ativos_venda: quantidade de dias com movimentação de vendas por loja/família

Essas variáveis enriqueceram a capacidade preditiva do modelo ao incorporar comportamento do calendário e da frequência de vendas.

<p align="center">
  <img src="Anexos\tabela_comparacao2.png" alt="tabela" width="50%" />
</p>

Observação: houve ligeira melhora no desempenho, especialmente no RMSE e R² do Random Forest.

###     **3. Sazonalidade e Promoção (flags binárias)**
Na tentativa de capturar padrões sazonais e comportamentos comerciais, foram adicionadas novas variáveis binárias:

has_promo: indica se houve promoção no mês

is_fim_ano: meses de novembro e dezembro

sazonal_forte: meses com maiores erros identificados previamente (ex: maio, novembro, março)

<p align="center">
  <img src="Anexos\tabela_comparacao3.png" alt="tabela" width="50%" />
</p>

Observação: surpreendentemente, essas variáveis não melhoraram o modelo, sugerindo que os efeitos sazonais já estavam parcialmente capturados por mes, onpromotion e family_top6, ou que o impacto binário era muito simplista para representar os padrões reais.

###     **4. Análise Descritiva e Transformações**
Uma análise estatística descritiva revelou:

A variável sales apresentava alta assimetria, com média muito maior que a mediana e valores máximos extremamente altos (outliers).

A variável dias_ativos_venda apresentava grande variação mensal, o que poderia induzir o modelo ao erro em meses com menos atividade.

Ações tomadas:

Aplicação de transformação logarítmica em sales para suavizar os efeitos dos outliers.

Criação da variável dias_ativos_venda_lag3: média móvel da frequência de vendas nos últimos 3 meses, fornecendo memória temporal ao modelo.

<p align="center">
  <img src="Anexos\tabela_comparacao4.png" alt="tabela" width="50%" />
</p>

Observação: essa etapa trouxe a maior melhoria no desempenho, indicando que a transformação do target e a incorporação da dinâmica de vendas foram cruciais para o ganho de performance. O XGBoost se destacou em todas as métricas, passando a ser o modelo de escolha.
<p align="center">
  <img src="Anexos\mes a mes 2.png" alt="tabela" width="90%" />
</p>

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

### Interpretação

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

