import pandas as pd
import numpy as np
from dateutil import parser

def get_data_assess_2024(all_data):
    '''Função para Capturar apenas dados do ano de 2024'''
    
    # Concatenar todos os DataFrames
    df = pd.concat(all_data, ignore_index=True)

    # Filtrando as linhas que não contêm a palavra "Dividendo e Desdobramento de ações" em qualquer coluna
    df = df[~df.apply(lambda row: row.astype(str).str.contains('Dividendo').any(), axis=1)]
    df = df[~df.apply(lambda row: row.astype(str).str.contains('Desdobramento de ações').any(), axis=1)]

    # Ajustando colunas de preço e convertendo as colunas numéricas para float
    cols_to_convert = ['Abertura', 'Alto', 'Baixo', 'Fechamento', 'Fechamento ajustado']
    df[cols_to_convert] = df[cols_to_convert].replace(',', '.', regex=True).astype(float)

    # Substituir '-' por NaN
    df['Volume'] = df['Volume'].replace('-', np.nan)
    df['Volume'] = df['Volume'].str.replace('.', '', regex=False).astype(float)

    # Ajustando a coluna das datas de negociação
    months_map = {
        'de jan. de': '01',
        'de fev. de': '02',
        'de mar. de': '03',
        'de abr. de': '04',
        'de mai. de': '05',
        'de jun. de': '06',
        'de jul. de': '07',
        'de ago. de': '08',
        'de set. de': '09',
        'de out. de': '10',
        'de nov. de': '11',
        'de dez. de': '12'
    }

    # Função para substituir os meses e converter a data
    def convert_date(date_str):
        for month, num in months_map.items():
            if month in date_str:
                date_str = date_str.replace(month, num)
                break
        return parser.parse(date_str).strftime('%d/%m/%Y')

    # Aplicando a função de conversão à coluna 'Data'
    df['Data'] = df['Data'].apply(convert_date)
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')

    # Separando apenas negociações de 2024
    df_2024 = df[df['Data'].dt.year == 2024]
    
    return df_2024

def price_variation(df_data_assess_2024):
    '''Função para verificar o maior e menor valor histórico'''
    df = df_data_assess_2024
    print(df)
    
    # Extraindo ano e mês para facilitar o agrupamento
    df['Ano-Mês'] = df['Data'].dt.to_period('M')

    # Calculando o maior valor histórico (máxima) e a maior baixa (mínima) por mês
    monthly_max = df.groupby('Ano-Mês')['Alto'].max().reset_index(name='Máxima do Mês')
    monthly_min = df.groupby('Ano-Mês')['Baixo'].min().reset_index(name='Mínima do Mês')

    # Mesclando essas informações de volta ao DataFrame original
    df = df.merge(monthly_max, on='Ano-Mês')
    df = df.merge(monthly_min, on='Ano-Mês')

    # Criando colunas adicionais
    df['Diferença Máx-Mín'] = df['Máxima do Mês'] - df['Mínima do Mês']
    df['Volume Médio'] = df.groupby('Ano-Mês')['Volume'].transform('mean')
    df['Variância de Fechamento'] = df.groupby('Ano-Mês')['Fechamento'].transform('var')

    # Verificando a variação de preço anual
    # Extrair o ano da data
    df['Ano'] = df['Data'].dt.year

    # Obter o fechamento do início e do final do ano para cada ativo
    fechamento_inicio = df[df['Data'].dt.month == 1].groupby('Ativo')['Fechamento'].first().reset_index(name='Fechamento_Inicio')
    fechamento_fim = df[df['Data'].dt.month == 12].groupby('Ativo')['Fechamento'].last().reset_index(name='Fechamento_Fim')

    # Unir os DataFrames de fechamento inicial e final
    variação_df = pd.merge(fechamento_inicio, fechamento_fim, on='Ativo')

    # Calcular a variação absoluta e percentual
    variação_df['Variação_Absoluta'] = variação_df['Fechamento_Fim'] - variação_df['Fechamento_Inicio']
    variação_df['Variação_Perc'] = (variação_df['Variação_Absoluta'] / variação_df['Fechamento_Inicio']) * 100


    return variação_df

