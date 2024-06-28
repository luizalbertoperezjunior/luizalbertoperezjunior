import pandas as pd
from tradingview_ta import TA_Handler, Interval
import datetime
import mysql.connector

# Obter a data atual
data_atual = datetime.datetime.now().strftime("%Y-%m-%d")

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
    cursor.execute("DROP TABLE IF EXISTS indicadores2")

    cursor.execute('''CREATE TABLE IF NOT EXISTS indicadores2 (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        data DATE,
                        empresa VARCHAR(255),
                        indicador VARCHAR(255),
                        valor FLOAT,
                        recomendacao VARCHAR(255)
                    )''')

    # Iterar sobre os indicadores e salvar no banco de dados
    for empresa, indicadores in indicadores_empresas.items():
        for indicador, valor in indicadores.items():
            # Inserir os valores na tabela
            insert_query = "INSERT INTO indicadores2 (data, empresa, indicador, valor) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (data_atual, empresa, indicador, valor))

            # Lógica para atualizar a recomendação com base no indicador e valor
            if indicador in ["RSI", "RSI[1]", "Stoch.K", "Stoch.D", "Stoch.K[1]", "Stoch.D[1]"]:
                if valor > 70:
                    recomendacao = "Venda"
                elif valor < 30:
                    recomendacao = "Compra"
                else:
                    recomendacao = "Neutro"
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
                else:
                    recomendacao = "Neutro"
            elif indicador in ["ADX", "ADX+DI", "ADX-DI", "ADX+DI[1]", "ADX-DI[1]", "AO", "AO[1]", "Mom", "Mom[1]"]:
                if valor > 50:
                    recomendacao = "Venda"
                elif valor < 50:
                    recomendacao = "Compra"
                else:
                    recomendacao = "Neutro"
            elif indicador in ["Rec.Stoch.RSI", "Stoch.RSI.K", "Rec.WR", "W.R", "Rec.BBPower", "BBPower", "Rec.UO", "UO", "Rec.VWMA", "Rec.HullMA9", "AO[2]"]:
                if valor > 0:
                    recomendacao = "Venda"
                elif valor < 0:
                    recomendacao = "Compra"
                else:
                    recomendacao = "Neutro"
            elif indicador == "close":
                valor_close = valor
            elif indicador == "EMA5":
                valor_EMA5 = valor
                if valor_close > valor_EMA5:
                    recomendacao = "Compra - Curto Prazo"
                elif valor_close < valor_EMA5:
                    recomendacao = "Venda - Curto Prazo"
            elif indicador == "EMA10":
                valor_EMA10 = valor
                if valor_close > valor_EMA10:
                    recomendacao = "Compra - Curto Prazo"
                elif valor_close < valor_EMA10:
                    recomendacao = "Venda - Curto Prazo"
            elif indicador == "EMA20":
                valor_EMA20 = valor
                if valor_close > valor_EMA20:
                    recomendacao = "Compra - Médio Prazo"
                elif valor_close < valor_EMA20:
                    recomendacao = "Venda - Médio Prazo"
            elif indicador == "EMA30":
                valor_EMA30 = valor
                if valor_close > valor_EMA30:
                    recomendacao = "Compra - Médio Prazo"
                elif valor_close < valor_EMA30:
                    recomendacao = "Venda - Médio Prazo"
            elif indicador == "EMA50":
                valor_EMA50 = valor
                if valor_close > valor_EMA50:
                    recomendacao = "Compra - Longo Prazo"
                elif valor_close < valor_EMA50:
                    recomendacao = "Venda - Longo Prazo"
            elif indicador == "EMA100":
                valor_EMA100 = valor
                if valor_close > valor_EMA100:
                    recomendacao = "Compra - Longo Prazo"
                elif valor_close < valor_EMA100:
                    recomendacao = "Venda - Longo Prazo"
            elif indicador == "EMA200":
                valor_EMA200 = valor
                if valor_close > valor_EMA200:
                    recomendacao = "Compra - Longo Prazo"
                elif valor_close < valor_EMA200:
                    recomendacao = "Venda - Longo Prazo"
            elif indicador == "SMA5":
                valor_SMA5 = valor
                if valor_close > valor_SMA5:
                    recomendacao = "Compra - Curto Prazo"
                elif valor_close < valor_SMA5:
                    recomendacao = "Venda - Curto Prazo"
            elif indicador == "SMA10":
                valor_SMA10 = valor
                if valor_close > valor_SMA10:
                    recomendacao = "Compra - Curto Prazo"
                elif valor_close < valor_SMA10:
                    recomendacao = "Venda - Curto Prazo"
            elif indicador == "SMA20":
                valor_SMA20 = valor
                if valor_close > valor_SMA20:
                    recomendacao = "Compra - Médio Prazo"
                elif valor_close < valor_SMA20:
                    recomendacao = "Venda - Médio Prazo"
            elif indicador == "SMA30":
                valor_SMA30 = valor
                if valor_close > valor_SMA30:
                    recomendacao = "Compra - Médio Prazo"
                elif valor_close < valor_SMA30:
                    recomendacao = "Venda - Médio Prazo"
            elif indicador == "SMA50":
                valor_SMA50 = valor
                if valor_close > valor_SMA50:
                    recomendacao = "Compra - Longo Prazo"
                elif valor_close < valor_SMA50:
                    recomendacao = "Venda - Longo Prazo"
            elif indicador == "SMA100":
                valor_SMA100 = valor
                if valor_close > valor_SMA100:
                    recomendacao = "Compra - Longo Prazo"
                elif valor_close < valor_SMA100:
                    recomendacao = "Venda - Longo Prazo"
            elif indicador == "SMA200":
                valor_SMA200 = valor
                if valor_close > valor_SMA200:
                    recomendacao = "Compra - Longo Prazo"
                elif valor_close < valor_SMA200:
                    recomendacao = "Venda - Longo Prazo"
            elif indicador == "Ichimoku.BLine":
                valor_IchimokuBLine = valor
                if valor_close > valor_IchimokuBLine:
                    recomendacao = "Compra"
                elif valor_close < valor_IchimokuBLine:
                    recomendacao = "Venda"
            elif indicador == "VWMA":
                valor_VWMA = valor
                if valor_close > valor_VWMA:
                    recomendacao = "Compra"
                elif valor_close < valor_VWMA:
                    recomendacao = "Venda"
            elif indicador == "HullMA9":
                valor_HullMA9 = valor
                if valor_close > valor_HullMA9:
                    recomendacao = "Compra"
                elif valor_close < valor_HullMA9:
                    recomendacao = "Venda"
            elif indicador == "Pivot.M.Classic.S3":
                valor_Pivot_S3 = valor
                if valor_close < valor_Pivot_S3:
                    recomendacao = "Compra"
                elif valor_close > valor_Pivot_S3:
                    recomendacao = "Venda"
            elif indicador == "Pivot.M.Classic.S2":
                valor_Pivot_S2 = valor
                if valor_close < valor_Pivot_S2:
                    recomendacao = "Compra"
                elif valor_close > valor_Pivot_S2:
                    recomendacao = "Venda"
            elif indicador == "Pivot.M.Classic.S1":
                valor_Pivot_S1 = valor
                if valor_close < valor_Pivot_S1:
                    recomendacao = "Compra"
                elif valor_close > valor_Pivot_S1:
                    recomendacao = "Venda"
            elif indicador == "Pivot.M.Classic.Middle":
                valor_Pivot_Middle = valor
                if valor_close < valor_Pivot_Middle:
                    recomendacao = "Compra"
                elif valor_close > valor_Pivot_Middle:
                    recomendacao = "Venda"
            elif indicador == "Pivot.M.Classic.R1":
                valor_Pivot_R1 = valor
                if valor_close > valor_Pivot_R1:
                    recomendacao = "Venda"
                elif valor_close < valor_Pivot_R1:
                    recomendacao = "Compra"
            elif indicador == "Pivot.M.Classic.R2":
                valor_Pivot_R2 = valor
                if valor_close > valor_Pivot_R2:
                    recomendacao = "Venda"
                elif valor_close < valor_Pivot_R2:
                    recomendacao = "Compra"
            elif indicador == "Pivot.M.Classic.R3":
                valor_Pivot_R3 = valor
                if valor_close > valor_Pivot_R3:
                    recomendacao = "Venda"
                elif valor_close < valor_Pivot_R3:
                    recomendacao = "Compra"
            else:
                recomendacao = "Neutro"

            # Atualizar a recomendação na tabela
            update_query = "UPDATE indicadores2 SET recomendacao = %s WHERE data = %s AND empresa = %s AND indicador = %s"
            cursor.execute(update_query, (recomendacao, data_atual, empresa, indicador))

    conn.commit()
finally:
    # Fechar a conexão com o banco de dados
    conn.close()
