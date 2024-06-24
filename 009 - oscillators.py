import mysql.connector
from tradingview_ta import TA_Handler, Interval
import datetime

# Definir símbolo das ações
empresas = ["PETR3", "PETR4", "WEGE3", "ITUB4", "VALE3", "BBDC4", "ITUB3", "BBAS3", "B3SA3", 
            "MGLU3", "ABEV3", "SUZB3", "BRAP4", "SANB11", "NTCO3", "GGBR4", "CSAN3", 
            "CYRE3", "LREN3", "BRFS3", "MDIA3", "CAML3"]

# Conectar-se ao banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="financeiro"
)

# Criar uma tabela para armazenar os osciladores, se ela ainda não existir
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS osciladores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    data DATE,
                    empresa VARCHAR(255),
                    indicador VARCHAR(255),
                    valor FLOAT
                )''')

# Obter a data atual
data_atual = datetime.datetime.now().strftime("%Y-%m-%d")

# Dicionário para armazenar os osciladores de cada empresa
oscillators_empresas = {}

# Iterar sobre as empresas e obter os indicadores
for empresa in empresas:
    # Inicializando o TA_Handler
    handler = TA_Handler(
        symbol=empresa,
        screener="brazil",
        exchange="BMFBOVESPA",
        interval=Interval.INTERVAL_1_DAY
    )
    
    # Obtendo os indicadores
    indicators = handler.get_indicators()
    oscillators_empresas[empresa] = indicators

# Iterar sobre os indicadores e salvar no banco de dados
for empresa, indicators in oscillators_empresas.items():
    for indicator, value in indicators.items():
        # Inserir os valores na tabela
        cursor.execute("INSERT INTO osciladores (data, empresa, indicador, valor) VALUES (%s, %s, %s, %s)", (data_atual, empresa, indicator, value))

# Confirmar as alterações e fechar a conexão
conn.commit()
conn.close()

print("Dados inseridos com sucesso no banco de dados.")
