import json
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
import logging

# Configurar logging para depuração
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def connect_db():
    '''Função para criar conexão com o banco de dados'''
    
    # Carregar as credenciais do arquivo JSON
    with open('./src/config/secrets.json', 'r') as f:
        secrets = json.load(f)

    # Criar o engine do SQLAlchemy
    connection_url = (
        f"mssql+pyodbc://{secrets['username']}:{secrets['password']}@"
        f"{secrets['host']}:{secrets['port']}/{secrets['database']}?"
        f"driver={secrets['driver'].replace(' ', '+')}"
    )
    engine = create_engine(connection_url, connect_args={"timeout": 60})
    
    return engine


def load_data(df, table_name):
    '''Função para carregar os dados no banco SQL Server'''
    tables_created = []
    engine          = connect_db()
    
    try:
        # Salvar DataFrame na tabela especificada
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Tabela '{table_name}' criada e dados inseridos com sucesso!")
        
        # Adiciona o nome da tabela à lista se a criação for bem-sucedida
        tables_created.append(table_name)
    
    except Exception as e:
        print(f"Erro ao carregar os dados para a tabela '{table_name}': {e}")
    
