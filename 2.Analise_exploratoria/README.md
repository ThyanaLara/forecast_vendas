
##  Análise Exploratória (EDA)

A análise exploratória teve como objetivo entender o comportamento das variáveis ao longo do tempo, *identificar padrões sazonais, avaliar a composição do mix de produtos e realizar o tratamento adequado de outliers*. Os principais pontos analisados foram:

**1. Média vs Total de Vendas por Tipo de Produto (Top 6)**:

  Foram comparadas duas métricas o volume total de vendas por família e a média de vendas por loja. A análise mostrou que a partir de 2016, o gráfico teve um comportamento curioso: enquanto a média de vendas por loja aumentou, o volume total de vendas caiu em 2017. Isso indicou que, embora as lojas estivessem vendendo mais, o número de lojas com atividade ou a frequência de venda por produto diminuiu.

<p align="center">
  <img src="Graficos/Media de vendas por Familia.png" alt="Média por Família" width="45%" />
  <img src="Graficos/Total de vendas por Familia.png" alt="Total por Família" width="45%" />
</p>

**2. Representatividade das Famílias de Produtos ao Longo dos Anos**:

  Também foi analisada a representatividade de cada família de produto ao longo do tempo. Observou-se que o mix de produtos mudou entre os anos.Poe exemplo a família GROCERY I, perdeu participação, enquanto PRODUCE ganhou destaque. Além disso, algumas famílias que não apareciam em determinados anos passaram a ser comercializadas posteriormente, o que pode refletir mudanças estratégicas de oferta.

<p align="center">
  <img src="Graficos/porcen. das familias de produtos.png" alt="%das familias de produto" width="70%" />
</p>

**3. Detecção e Tratamento de Outliers**:

  A detecção de outliers foi realizada em duas etapas. Inicialmente, o tratamento de outliers havia sido feito de forma geral, mas ao treinar os primeiros modelos, ficou evidente que valores extremos em meses específicos estavam impactando negativamente o desempenho. Com isso, revisei a análise, e passei a considerar a distribuição de outliers por mês, com base na mediana e no desvio interquartil (IQR) para a variável sales. 
  Essa limpeza resultou na remoção de 5,61% da base original e contribuiu para melhorar a performance do modelo, mantendo a estabilidade das séries temporais.

<p align="center">
  <img src="Graficos/Distribuição de Vendas (sales) por Ano-Mês.png" alt="Distribuição de Vendas - Outlier" width="70%" />
</p>

**4. Distribuição Mensal e por Tipo de Produto**:

  Também foi avaliada a distribuição da quantidade de vendas por mês e por tipo de produto. Observou-se que dezembro concentra o maior volume de vendas, reforçando o padrão sazonal.
  E a distribuição de vendas por família, indicou que famílias como GROCERY I, BEVERAGES e PRODUCE concentram os maiores volumes, enquanto outras como BREAD/BAKERY possuem vendas mais baixas e estáveis.

<p align="center">
  <img src="Graficos/Distribuição de Vendas por Família.png" alt="Distribuição de Vendas por produto - Outlier" width="70%" />
</p>


