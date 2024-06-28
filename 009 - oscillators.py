import pandas as pd
from tradingview_ta import TA_Handler, Interval
import datetime
import mysql.connector

# Obter a data atual
data_atual = datetime.datetime.now().strftime("%Y-%m-%d")
data_hoje = datetime.datetime.now().strftime("%d_%m_%Y")

# Definir símbolo das ações
empresas = ["SAPR4","CPLE6","CMIG4","TAEE4","BBDC3","PETR3", "PETR4", "WEGE3", "ITUB4", "VALE3", "BBDC4", "ITUB3", "BBAS3", "B3SA3", 
            "MGLU3", "ABEV3", "SUZB3", "BRAP4", "SANB11", "NTCO3", "GGBR4", "CSAN3", 
            "CYRE3", "LREN3", "BRFS3", "MDIA3", "CAML3"]

# Dicionário para armazenar os indicadores das empresas
indicadores_empresas = {}

# Loop para obter os indicadores de cada empresa
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
    indicadores_empresas[empresa] = indicators

# Conectar-se ao banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="financeiro"
)

try:
    # Criar uma tabela para armazenar os indicadores, se ela ainda não existir
    cursor = conn.cursor()

    # Drop da tabela antiga se existir
    cursor.execute("DROP TABLE IF EXISTS indicadores")

    cursor.execute('''CREATE TABLE IF NOT EXISTS indicadores (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        data DATE,
                        empresa VARCHAR(255),
                        indicador VARCHAR(255),
                        valor FLOAT,
                        recomendacao VARCHAR(255)
                    )''')

    # Iterar sobre os indicadores e salvar no banco de dados
    for empresa, indicadores in indicadores_empresas.items():
        valor_close = None
        recomendacao = "Neutro"  # Recomendação inicial

        for indicador, valor in indicadores.items():
            # Inserir os valores na tabela
            insert_query = "INSERT INTO indicadores (data, empresa, indicador, valor) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (data_atual, empresa, indicador, valor))

            # Lógica para atualizar a recomendação com base no indicador e valor
            if indicador in ["RSI", "RSI[1]", "Stoch.K", "Stoch.D", "Stoch.K[1]", "Stoch.D[1]"]:
                if valor > 70:
                    recomendacao = "Venda"
                elif valor < 30:
                    recomendacao = "Compra"
            elif indicador in ["MACD.macd", "MACD.signal"]:
                if valor > 0:
                    recomendacao = "Compra"
                else:
                    recomendacao = "Venda"
            elif indicador in ["CCI20", "CCI20[1]"]:
                if valor < -100:
                    recomendacao = "Compra"
                elif valor > 100:
                    recomendacao = "Venda"
            elif indicador in ["ADX", "ADX+DI", "ADX-DI", "ADX+DI[1]", "ADX-DI[1]", "AO", "AO[1]", "Mom", "Mom[1]"]:
                if valor > 50:
                    recomendacao = "Venda"
                elif valor < 50:
                    recomendacao = "Compra"
            elif indicador in ["Rec.Stoch.RSI", "Stoch.RSI.K", "Rec.WR", "W.R", "Rec.BBPower", "BBPower", "Rec.UO", "UO", "Rec.VWMA", "Rec.HullMA9", "AO[2]"]:
                if valor > 0:
                    recomendacao = "Venda"
                elif valor < 0:
                    recomendacao = "Compra"
            elif indicador == "close":
                valor_close = valor

            elif indicador.startswith("EMA"):
                periodo = int(indicador[3:])
                if valor_close is not None:
                    if valor_close > valor:
                        recomendacao = f"Compra - {periodo} Prazo"
                    elif valor_close < valor:
                        recomendacao = f"Venda - {periodo} Prazo"

            elif indicador.startswith("SMA"):
                periodo = int(indicador[3:])
                if valor_close is not None:
                    if valor_close > valor:
                        recomendacao = f"Compra - {periodo} Prazo"
                    elif valor_close < valor:
                        recomendacao = f"Venda - {periodo} Prazo"

                        
            elif indicador == "Rec.Ichimoku":
                if valor_close is not None:
                    if valor_close > valor:
                        recomendacao = "Compra"
                    elif valor_close < valor:
                        recomendacao = "Venda"


            elif indicador == "Ichimoku.BLine":
                if valor_close is not None:
                    if valor_close > valor:
                        recomendacao = "Compra"
                    elif valor_close < valor:
                        recomendacao = "Venda"

            elif indicador == "VWMA":
                if valor_close is not None:
                    if valor_close > valor:
                        recomendacao = "Compra"
                    elif valor_close < valor:
                        recomendacao = "Venda"

            elif indicador == "HullMA9":
                if valor_close is not None:
                    if valor_close > valor:
                        recomendacao = "Compra"
                    elif valor_close < valor:
                        recomendacao = "Venda"

            elif indicador.startswith("Pivot.M.Classic"):
                if valor_close is not None:
                    if "S" in indicador and valor_close < valor:
                        recomendacao = "Compra"
                    elif "R" in indicador and valor_close > valor:
                        recomendacao = "Venda"

            elif indicador.startswith("Pivot.M.Fibonacci"):
                if valor_close is not None:
                    if "S" in indicador and valor_close < valor:
                        recomendacao = "Compra"
                    elif "R" in indicador and valor_close > valor:
                        recomendacao = "Venda"

            elif indicador.startswith("Pivot.M.Camarilla"):
                if valor_close is not None:
                    if "S" in indicador and valor_close < valor:
                        recomendacao = "Compra"
                    elif "R" in indicador and valor_close > valor:
                        recomendacao = "Venda"

            elif indicador.startswith("Pivot.M.Woodie"):
                if valor_close is not None:
                    if "S" in indicador and valor_close < valor:
                        recomendacao = "Compra"
                    elif "R" in indicador and valor_close > valor:
                        recomendacao = "Venda"

            elif indicador.startswith("Pivot.M.Demark"):
                if valor_close is not None:
                    if "S" in indicador and valor_close < valor:
                        recomendacao = "Compra"
                    elif "R" in indicador and valor_close > valor:
                        recomendacao = "Venda"

            # Atualizar a recomendação no banco de dados
            update_query = "UPDATE indicadores SET recomendacao = %s WHERE data = %s AND empresa = %s AND indicador = %s"
            cursor.execute(update_query, (recomendacao, data_atual, empresa, indicador))

    # Commit para salvar as alterações
    conn.commit()

finally:
    # Fechar a conexão com o banco de dados
    cursor.close()
    conn.close()
