import numpy as np
import pandas as pd

#pasta = 
holidays_events = pd.read_csv(r'c:\Users\Thyana De Lara\Documents\TCC\modelo_vendas_forecasting\Bases\holidays_events.csv')
train = pd.read_csv(r'c:\Users\Thyana De Lara\Documents\TCC\modelo_vendas_forecasting\Bases\train.csv')
stores = pd.read_csv(r'C:\Users\Thyana De Lara\Documents\TCC\modelo_vendas_forecasting\Bases\stores.csv')

train['date'] = pd.to_datetime(train['date'])
holidays_events['date'] = pd.to_datetime(holidays_events['date'])

#Criação do campo de frequência
# Filtrar a base para considerar apenas linhas com venda real
df_com_venda = train[train['sales'] > 0]

# Contar quantos produtos foram vendidos por data/loja/family
df_volume = (df_com_venda.groupby(['date', 'store_nbr', 'family']).size().reset_index(name='volume'))

# Extrair ano e mês da data (se ainda não estiver)
df_volume['ano'] = pd.to_datetime(df_volume['date']).dt.year
df_volume['mes'] = pd.to_datetime(df_volume['date']).dt.month

# Agregar volume por loja/family/mês
df_volume_mensal = df_volume.groupby(['store_nbr', 'family', 'ano', 'mes'])['volume'].sum().reset_index()

# Criar uma coluna com nome e tipo dos feriados agrupados por mês
feriados_por_mes_detalhado = holidays_events.groupby(holidays_events['date'].dt.to_period('M')).agg({
    'description': lambda x: ', '.join(x.unique())}).reset_index()

print(feriados_por_mes_detalhado)

# Primeiro, criamos uma cópia da tabela de feriados
holidays = holidays_events.copy()

# Expandir o dataset de feriados para cada loja, dependendo da regra de localidade
def map_holiday_to_stores(holiday_row, stores_df):
    if holiday_row['locale'] == 'National':
        # Se for feriado nacional, todas as lojas participam
        return stores_df['store_nbr'].tolist()
    elif holiday_row['locale'] == 'Regional':
        # Se for regional, só lojas daquele estado
        return stores_df.loc[stores_df['state'] == holiday_row['locale_name'], 'store_nbr'].tolist()
    elif holiday_row['locale'] == 'Local':
        # Se for local, só lojas daquela cidade
        return stores_df.loc[stores_df['city'] == holiday_row['locale_name'], 'store_nbr'].tolist()
    else:
        # Caso tenha algum tipo não esperado, retorna vazio
        return []

# Criar uma lista de linhas expandidas (cada linha por loja afetada)
expanded_rows = []

for idx, row in holidays.iterrows():
    affected_stores = map_holiday_to_stores(row, stores)
    for store in affected_stores:
        expanded_rows.append({'date': row['date'],'store_nbr': store,'description': row['description'],'type': row['type'],'locale': row['locale'],
                              'locale_name': row['locale_name']})

# Criar um novo DataFrame com os feriados já mapeados por loja
holidays_per_store = pd.DataFrame(expanded_rows)

# Criar uma coluna de ano e mês
holidays_per_store['mes_ano'] = holidays_per_store['date'].dt.to_period('M')

# Agora, contar quantos feriados por loja em cada mês
qtd_feriados_por_loja_mes = holidays_per_store.groupby(['store_nbr', 'mes_ano']).size().reset_index(name='qtd_feriados')
print(qtd_feriados_por_loja_mes.head())

# Agrupar o train mensalmente por loja e família
df = train.groupby([ train['date'].dt.to_period('M'),'store_nbr', 'family',]).agg({'sales': 'sum','onpromotion': 'sum'}).reset_index()

# Criar coluna de ano e mês
df['ano'] = df['date'].dt.year
df['mes'] = df['date'].dt.month

# Juntar com o DataFrame mensal
df = df.merge(qtd_feriados_por_loja_mes,
    left_on=['store_nbr', 'date'], 
    right_on=['store_nbr', 'mes_ano'],
    how='left')

# Preencher os meses sem feriado com zero
df['qtd_feriados'] = df['qtd_feriados'].fillna(0)

# Unir na base final
df = df.merge(df_volume_mensal, on=['store_nbr', 'family', 'ano', 'mes'], how='left')

# Preencher com zero onde não teve volume
df['dias_ativos_venda'] = df['volume'].fillna(0)

print("\nInformações do DataFrame:")
print(df.info())

df['sales'] = np.maximum(df['sales'], 0)  # zera valores negativos
df['sales'] = df['sales'].replace(0, 0.01)

colunas = ['date', 'store_nbr', 'family', 'sales', 'onpromotion', 'ano', 'mes', 'qtd_feriados', 'dias_ativos_venda']
df = df[colunas]

print("\nContagem de valores nulos por coluna:")
print(df.isnull().sum())
df.to_csv('1.dados_tratado.csv', index=False)