# ETL Yahoo Finance

Este projeto realiza um processo de **ETL (Extract, Transform, Load)** para coletar dados de ações diretamente do site **Yahoo Finance (YFinance)** utilizando **web scraping** e armazená-los em um banco de dados **SQL Server**.

O projeto é implementado em **Python** e faz uso de diversas bibliotecas para manipulação de dados, scraping e integração com o banco de dados.

## Estrutura do Projeto
```
ETL_YFinance/
├── logs
├── main.py                         # Arquivo principal que executa o processo de ETL
├── README.md                       # Documentação do projeto
├── requirements.txt                # Lista de dependências do projeto
└── src
    ├── config
    │   └── secrets_model.json      # Arquivo contendo informações sensíveis (ex: senhas)
    ├── extract
    │   └── extract_data.py         # Função de web scraping dos dados da YFinance
    ├── load
    │   └── connect_db.py           # Função para carregar os dados no SQL Server
    └── transform
        └── trasnsform_data.py      # Funções para transformar os dados coletados
```

## Pré-requisitos

Antes de rodar o projeto, você precisará instalar o Python 3.x e alguns pacotes adicionais. Para isso:

1. **Instale o Python 3.x**: [Baixe aqui](https://www.python.org/downloads/).
2. **Instale o SQL Server** (caso ainda não tenha um servidor configurado) ou use uma conexão já existente.

### Configurações do Banco de Dados

Este projeto armazena os dados extraídos no **SQL Server**. As configurações de conexão, como host, usuário, senha e nome do banco de dados, estão no arquivo `src/config/secrets.json`. É necessário atualizar esse arquivo com as informações corretas antes de rodar o projeto.

Se não houver um banco de dados criado, faça a criação préviamente utilizando seu SGBD ou o sqlcmd com o código
```bash
sqlcmd -S SeuServidor -U SeuUsuário -P SuaSenha -Q "CREATE DATABASE YFINANCE"
```


## Passo a Passo para Executar o Projeto

### 1. Clonar o repositório

Primeiro, clone o repositório para a sua máquina local.

```bash
git clone https://github.com/seu-usuario/ETL_YFinance.git
cd ETL_YFinance
```

### 2. Instalar Dependências
Instale as bibliotecas necessárias utilizando o `pip`. O arquivo `requirements.txt` contém todas as dependências do projeto.

```bash
pip install -r requirements.txt
```
### 3. Configurar Variáveis Sensíveis

No ditetório `src/config/secrets_model.json` você encontrará um modelo para inserir as informações senssíveis de acesso ao banco de dados.
Insira suas configurações e salve-as como o nome `secrets.json` no mesmo diretório para que o acesso seja realizado corretamente.

### 4. Executar o Projeto
Após configurar o ambiente, execute o script principal main.py para iniciar o processo de ETL.

```bash
python3 main.py
```
O script irá:

1. **Extrair** os dados de ações do site Yahoo Finance usando web scraping.
2. **Transformar** os dados, aplicando as regras de negócio necessárias.
3. **Carregar** os dados no SQL Server.

## Principais Bibliotecas Utilizadas

- **pandas**: Manipulação de dados.
- **numpy**: Suporte matemático e operações de arrays.
- **selenium**: Automatização do web scraping.
- **beautifulsoup4**: Extração de dados do HTML.
- **sqlalchemy**: Integração e manipulação de dados no SQL Server.
- **pyodbc**: Conexão com o SQL Server.


