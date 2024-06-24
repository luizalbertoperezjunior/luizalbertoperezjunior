import pandas as pd
from tradingview_ta import TA_Handler, Interval
import datetime
import mysql.connector

# Obter a data atual
data_atual = datetime.datetime.now().strftime("%Y-%m-%d")

# Definir símbolo das ações
empresas = ["PETR3", "PETR4", "WEGE3", "ITUB4", "VALE3", "BBDC4", "ITUB3", "BBAS3", "B3SA3", 
            "MGLU3", "ABEV3", "SUZB3", "BRAP4", "SANB11", "NTCO3", "GGBR4", "CSAN3", 
             "CYRE3", "LREN3", "BRFS3", "MDIA3", "CAML3"]


# Definindo os osciladores desejados
oscillators_desejados = ["RECOMMENDATION","BUY","SELL","NEUTRAL","COMPUTE"]

# Definindo os indicadores desejados
indicadores_desejados = [
    "Recommend.Other", "Recommend.All", "Recommend.MA", "RSI", "RSI[1]",
    
    "Stoch.K", "Stoch.D", "Stoch.K[1]", "Stoch.D[1]", "CCI20", "CCI20[1]",
    "ADX", "ADX+DI", "ADX-DI", "ADX+DI[1]", "ADX-DI[1]", "AO", "AO[1]", "Mom",
    "Mom[1]", "MACD.macd", "MACD.signal", "Rec.Stoch.RSI", "Stoch.RSI.K", 
    "Rec.WR", "W.R", "Rec.BBPower", "BBPower", "Rec.UO", "UO", "close", 
    "EMA5", "SMA5", "EMA10", "SMA10", "EMA20", "SMA20", "EMA30", "SMA30", 
    "EMA50", "SMA50", "EMA100", "SMA100", "EMA200", "SMA200", "Rec.Ichimoku",
    "Ichimoku.BLine", "Rec.VWMA", "VWMA", "Rec.HullMA9", "HullMA9", 
    "Pivot.M.Classic.S3", "Pivot.M.Classic.S2", "Pivot.M.Classic.S1", 
    "Pivot.M.Classic.Middle", "Pivot.M.Classic.R1", "Pivot.M.Classic.R2", 
    "Pivot.M.Classic.R3", "Pivot.M.Fibonacci.S3", "Pivot.M.Fibonacci.S2", 
    "Pivot.M.Fibonacci.S1", "Pivot.M.Fibonacci.Middle", "Pivot.M.Fibonacci.R1", 
    "Pivot.M.Fibonacci.R2", "Pivot.M.Fibonacci.R3", "Pivot.M.Camarilla.S3", 
    "Pivot.M.Camarilla.S2", "Pivot.M.Camarilla.S1", "Pivot.M.Camarilla.Middle", 
    "Pivot.M.Camarilla.R1", "Pivot.M.Camarilla.R2", "Pivot.M.Camarilla.R3", 
    "Pivot.M.Woodie.S3", "Pivot.M.Woodie.S2", "Pivot.M.Woodie.S1", 
    "Pivot.M.Woodie.Middle", "Pivot.M.Woodie.R1", "Pivot.M.Woodie.R2", 
    "Pivot.M.Woodie.R3", "Pivot.M.Demark.S1", "Pivot.M.Demark.Middle", 
    "Pivot.M.Demark.R1", "open", "P.SAR", "BB.lower", "BB.upper", "AO[2]", 
    "volume", "change", "low", "high"
]

# Dicionário para armazenar os indicadores das empresas
indicadores_empresas = {}

# Loop para obter os indicadores de cada empresa
for empresa in empresas:
    # Inicializando o TA_Handler
    tesla = TA_Handler(
        symbol=empresa,
        screener="brazil",
        exchange="BMFBOVESPA",
        interval=Interval.INTERVAL_1_DAY
    )
    
    # Obtendo os indicadores
    indicators = tesla.get_indicators()
    indicadores_empresas[empresa] = indicators

# Conectar-se ao banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="financeiro"
)

# Criar uma tabela para armazenar os indicadores, se ela ainda não existir
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS indicadores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    data DATE,
                    empresa VARCHAR(255),
                    indicador VARCHAR(255),
                    valor FLOAT
                    
                )''')

# Iterar sobre os indicadores e salvar no banco de dados
for empresa, indicadores in indicadores_empresas.items():
    for indicador, valor in indicadores.items():
        # Inserir os valores na tabela
        cursor.execute("INSERT INTO indicadores (data, empresa, indicador, valor) VALUES (%s, %s, %s, %s)", (data_atual, empresa, indicador, valor))

# Confirmar as alterações e fechar a conexão
conn.commit()
conn.close()   
