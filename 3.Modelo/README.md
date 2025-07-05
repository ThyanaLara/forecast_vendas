# Estratégia de Modelagem
Durante o desenvolvimento do modelo preditivo de vendas mensais, adotou-se uma abordagem incremental, avaliando o impacto da adição de variáveis, transformação de dados e técnicas de validação. A seguir, descrevem-se os principais passos realizados e os aprendizados ao longo do processo.

### **1. Modelo Base (sem engenharia de features)**
Inicialmente, foi treinado um modelo utilizando apenas as colunas originais da base:

Variáveis numéricas: onpromotion

Variáveis categóricas: store_nbr, family_top6, ano, mes

<p align="center">
  <img src="Anexos\tabela_comparacao1.png" alt="%das familias de produto" width="90%" />
</p>

Observação: os resultados iniciais foram satisfatórios, porém ao avaliar os erros mês a mês, observou-se uma grande discrepância entre as vendas previstas e as reais em determinados períodos.

<p align="center">
  <img src="Anexos\mes a mes1.png" alt="%das familias de produto" width="90%" />
</p>

### **2. Primeiras Features Criadas (de calendários e vendas ativas)**
Com base em análises complementares, adicionaram-se variáveis externas:

qtd_feriados: número de feriados no mês

dias_ativos_venda: quantidade de dias com movimentação de vendas por loja/família

Essas variáveis enriqueceram a capacidade preditiva do modelo ao incorporar comportamento do calendário e da frequência de vendas.

<p align="center">
  <img src="Anexos\tabela_comparacao2.png" alt="%das familias de produto" width="90%" />
</p>

Observação: houve ligeira melhora no desempenho, especialmente no RMSE e R² do Random Forest.

### **3. Sazonalidade e Promoção (flags binárias)**
Na tentativa de capturar padrões sazonais e comportamentos comerciais, foram adicionadas novas variáveis binárias:

has_promo: indica se houve promoção no mês

is_fim_ano: meses de novembro e dezembro

sazonal_forte: meses com maiores erros identificados previamente (ex: maio, novembro, março)

<p align="center">
  <img src="Anexos\tabela_comparacao3.png" alt="%das familias de produto" width="90%" />
</p>

Observação: surpreendentemente, essas variáveis não melhoraram o modelo, sugerindo que os efeitos sazonais já estavam parcialmente capturados por mes, onpromotion e family_top6, ou que o impacto binário era muito simplista para representar os padrões reais.

### **4. Análise Descritiva e Transformações**
Uma análise estatística descritiva revelou:

A variável sales apresentava alta assimetria, com média muito maior que a mediana e valores máximos extremamente altos (outliers).

A variável dias_ativos_venda apresentava grande variação mensal, o que poderia induzir o modelo ao erro em meses com menos atividade.

Ações tomadas:

Aplicação de transformação logarítmica em sales para suavizar os efeitos dos outliers.

Criação da variável dias_ativos_venda_lag3: média móvel da frequência de vendas nos últimos 3 meses, fornecendo memória temporal ao modelo.

<p align="center">
  <img src="Anexos\tabela_comparacao4.png" alt="%das familias de produto" width="90%" />
</p>

Observação: essa etapa trouxe a maior melhoria no desempenho, indicando que a transformação do target e a incorporação da dinâmica de vendas foram cruciais para o ganho de performance. O XGBoost se destacou em todas as métricas, passando a ser o modelo de escolha.

