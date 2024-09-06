from src.transform.trasnsform_data import get_data_assess_2024, price_variation
from src.extract.extract_data import get_data_yfinance
from src.load.connect_db import load_data
import time

def main():
    # Marca o tempo de início
    start_time = time.time()

    # Lista de ativos para capturar
    assets_list = [
        'BBAS3.SA',
        'ITSA4.SA',
        'BBDC3.SA',
        'BCSA34.SA'
    ] 

    print('Capturando os dados')
    all_data = get_data_yfinance(assets_list)

    capture_time = time.time()
    print(f"Tempo de execução da captura de dados: {capture_time - start_time:.5f} segundos")

    print('Separando apenas dados de 2024')
    df_data_assess_2024 = get_data_assess_2024(all_data)
    print(df_data_assess_2024)
    
    print('Criando novo dataframe para armazenar a variação de preços')
    df_price_variate = price_variation(df_data_assess_2024)
    print(df_price_variate)
    

    transform_time = time.time()
    print(f"Tempo de execução da transformação de dados: {transform_time - capture_time:.5f} segundos")

    print('Carregando dados no banco')
    load_data(df_data_assess_2024, table_name='data_assess_2024')
    load_data(df_price_variate, table_name='price_variate')

    # Marca o tempo após o carregamento
    load_time = time.time()
    print(f"Tempo de execução do carregamento dos dados: {load_time - transform_time:.5f} segundos")

    # Tempo total de execução
    print(f"Tempo total de execução: {load_time - start_time:.5f} segundos")

if __name__ == "__main__":
    main()
