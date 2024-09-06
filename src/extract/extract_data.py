import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
from datetime import date, datetime



def get_data_yfinance(assets_list):

    # Configuração do ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # DataFrame para armazenar todos os dados
    all_data = []

    for assets in assets_list:
        print(f'Abrindo página para {assets}')
        url = f'https://br.financas.yahoo.com/quote/{assets}/history/'
        driver.get(url)

        print('Aguardando carregamento')
        driver.implicitly_wait(5)

        print('Scrollando até o fim da página')
        for _ in range(5):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            sleep(2)

        # Capturando o html da página
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        print(f'Capturando os dados da tabela de preços do ativo {assets}')

        source_table = soup.find('table', class_='W(100%) M(0)')
        if not source_table:
            print(f'Tabela não encontrada para o ativo {assets}')
            continue

        headers = []
        data = []

        for header in source_table.find_all("th"):
            headers.append(header.text.strip())

        for row in source_table.find_all("tr"):
            columns = row.find_all("td")
            if columns:
                row_data = [column.text.strip() for column in columns]
                data.append(row_data)

        # Criando o dataframe do ativo
        df = pd.DataFrame(data, columns=headers)

        # Retirando linha de texto se houver
        if not df.empty:
            df = df.iloc[:-1]

        # Adicionando a coluna para identificação do ativo e ajustando nome da coluna
        df['Ativo'] = assets
        df.rename(columns={
            'Fechamento*': 'Fechamento',
            'Fechamento ajustado**': 'Fechamento ajustado'
        }, inplace=True)

        # Adicionando os dados do ativo ao DataFrame final
        all_data.append(df)

    # Fechar o driver após a captura dos dados
    driver.quit()
    
    return all_data






# # %%
# df.to_csv(f'Análise feita em {date.today()}.csv')
# variação_df.to_csv(f'Variação de preço em 2024.csv')
