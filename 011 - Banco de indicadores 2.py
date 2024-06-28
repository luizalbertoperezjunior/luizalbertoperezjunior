import pandas as pd
from tradingview_ta import TA_Handler, Interval
import datetime
import mysql.connector

# Obter a data atual
# data_atual = datetime.datetime.now().strftime("%Y-%m-%d")

# Obter a data atual
data_atual = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


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
        # interval=Interval.INTERVAL_1_HOUR
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

    cursor.execute('''drop table indicadores2''')

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
                # Lógica para comparar EMA5 e close
                if valor_close > valor_EMA5:
                    recomendacao = "Compra - Curto Prazo"
                elif valor_close < valor_EMA5:
                    recomendacao = "Venda - Curto Prazo"

            elif indicador == "EMA10":
                valor_EMA10 = valor
                # Lógica para comparar EMA10 e close
                if valor_close > valor_EMA10:
                    recomendacao = "Compra - Curto Prazo"
                elif valor_close < valor_EMA10:
                    recomendacao = "Venda - Curto Prazo"
            
            elif indicador == "EMA20":
                valor_EMA20 = valor
                # Lógica para comparar EMA20 e close
                if valor_close > valor_EMA20:
                    recomendacao = "Compra - Médio Prazo"
                elif valor_close < valor_EMA20:
                    recomendacao = "Venda - Médio Prazo"

            elif indicador == "EMA30":
                valor_EMA30 = valor
                # Lógica para comparar EMA30 e close
                if valor_close is not None and valor_EMA30 is not None:
                    if valor_close > valor_EMA30:
                        recomendacao = "Compra - Médio Prazo"
                    elif valor_close < valor_EMA30:
                        recomendacao = "Venda - Médio Prazo"

            elif indicador == "EMA50":
                valor_EMA50 = valor
                # Lógica para comparar EMA50 e close
                if valor_close is not None and valor_EMA50 is not None:
                    if valor_close > valor_EMA50:
                        recomendacao = "Compra - Longo Prazo"
                    elif valor_close < valor_EMA50:
                        recomendacao = "Venda - Longo Prazo"

            elif indicador == "EMA100":
                valor_EMA100 = valor
                # Lógica para comparar EMA100 e close
                if valor_close is not None and valor_EMA100 is not None:
                    if valor_close > valor_EMA100:
                        recomendacao = "Compra - Longo Prazo"
                    elif valor_close < valor_EMA100:
                        recomendacao = "Venda - Longo Prazo"

            elif indicador == "EMA200":
                valor_EMA200 = valor
                # Lógica para comparar EMA200 e close
                if valor_close is not None and valor_EMA200 is not None:
                    if valor_close > valor_EMA200:
                        recomendacao = "Compra - Longo Prazo"
                    elif valor_close < valor_EMA200:
                        recomendacao = "Venda - Longo Prazo"
            
            
                # else:
                #     recomendacao = "Neutro"

                # SMA comparações
            elif indicador == "SMA5":
                valor_SMA5 = valor
                if valor_close is not None:
                    if valor_close > valor_SMA5:
                        recomendacao = "Compra - Curto Prazo"
                    elif valor_close < valor_SMA5:
                        recomendacao = "Venda - Curto Prazo"
            
            elif indicador == "SMA10":
                valor_SMA10 = valor
                if valor_close is not None:
                    if valor_close > valor_SMA10:
                        recomendacao = "Compra - Curto Prazo"
                    elif valor_close < valor_SMA10:
                        recomendacao = "Venda - Curto Prazo"
            
            elif indicador == "SMA20":
                valor_SMA20 = valor
                if valor_close is not None:
                    if valor_close > valor_SMA20:
                        recomendacao = "Compra - Médio Prazo"
                    elif valor_close < valor_SMA20:
                        recomendacao = "Venda - Médio Prazo"
            
            elif indicador == "SMA30":
                valor_SMA30 = valor
                if valor_close is not None:
                    if valor_close > valor_SMA30:
                        recomendacao = "Compra - Médio Prazo"
                    elif valor_close < valor_SMA30:
                        recomendacao = "Venda - Médio Prazo"
            
            elif indicador == "SMA50":
                valor_SMA50 = valor
                if valor_close is not None:
                    if valor_close > valor_SMA50:
                        recomendacao = "Compra - Longo Prazo"
                    elif valor_close < valor_SMA50:
                        recomendacao = "Venda - Longo Prazo"
            
            elif indicador == "SMA100":
                valor_SMA100 = valor
                if valor_close is not None:
                    if valor_close > valor_SMA100:
                        recomendacao = "Compra - Longo Prazo"
                    elif valor_close < valor_SMA100:
                        recomendacao = "Venda - Longo Prazo"
            
            elif indicador == "SMA200":
                valor_SMA200 = valor
                if valor_close is not None:
                    if valor_close > valor_SMA200:
                        recomendacao = "Compra - Longo Prazo"
                    elif valor_close < valor_SMA200:
                        recomendacao = "Venda - Longo Prazo"

            # Ichimoku Baseline comparação
            elif indicador == "Ichimoku.BLine":
                valor_IchimokuBLine = valor
                if valor_close is not None:
                    if valor_close > valor_IchimokuBLine:
                        recomendacao = "Compra"
                    elif valor_close < valor_IchimokuBLine:
                        recomendacao = "Venda"

            # Ichimoku Baseline comparação
            elif indicador == "Ichimoku.BLine":
                valor_IchimokuBLine = valor
                if valor_close is not None:
                    if valor_close > valor_IchimokuBLine:
                        recomendacao = "Compra"
                    elif valor_close < valor_IchimokuBLine:
                        recomendacao = "Venda"

            # O indicador VWMA (Volume Weighted Moving Average) é uma média móvel ponderada pelo volume, 
            # o que significa que ele dá mais peso aos preços de negociação com maior volume. 
            elif indicador == "VWMA":
                valor_IchimokuBLine = valor
                if valor_close is not None:
                    if valor_close > valor_IchimokuBLine:
                        recomendacao = "Compra"
                    elif valor_close < valor_IchimokuBLine:
                        recomendacao = "Venda"

            # HullMA9 comparação
            elif indicador == "HullMA9":
                valor_HullMA9 = valor
                if valor_close is not None:
                    if valor_close > valor_HullMA9:
                        recomendacao = "Compra"
                    elif valor_close < valor_HullMA9:
                        recomendacao = "Venda"
            
            # Compra: Quando o preço atual está abaixo do S3, pode ser visto como uma oportunidade de compra, esperando uma reversão de alta.
            # Venda: Quando o preço atual está acima do S3, pode ser visto como uma oportunidade de venda, esperando que o preço desça para testar o suporte. 
            elif indicador == "Pivot.M.Classic.S3":
                valor_Pivot_S3 = valor
                if valor_close is not None:
                    if valor_close < valor_Pivot_S3:
                        recomendacao = "Compra"
                    elif valor_close > valor_Pivot_S3:
                        recomendacao = "Venda"
            
            elif indicador == "Pivot.M.Classic.S2":
                valor_Pivot_S2 = valor
                if valor_close is not None:
                    if valor_close < valor_Pivot_S2:
                        recomendacao = "Compra"
                    elif valor_close > valor_Pivot_S2:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Classic.S1":
                valor_Pivot_S1 = valor
                if valor_close is not None:
                    if valor_close < valor_Pivot_S1:
                        recomendacao = "Compra"
                    elif valor_close > valor_Pivot_S1:
                        recomendacao = "Venda"

            # Compra: Quando o preço atual está acima do ponto de pivô médio, pode ser visto como uma oportunidade de compra, esperando que o preço continue subindo.
            # Venda: Quando o preço atual está abaixo do ponto de pivô médio, pode ser visto como uma oportunidade de venda, esperando que o preço continue descendo.
            elif indicador == "Pivot.M.Classic.Middle":
                valor_Pivot_M = valor
                if valor_close is not None:
                    if valor_close > valor_Pivot_M:
                        recomendacao = "Compra"
                    elif valor_close < valor_Pivot_M:
                        recomendacao = "Venda"

            # Compra: Quando o preço atual está acima do R1, pode ser visto como uma oportunidade de compra, esperando que o preço continue subindo.
            # Venda: Quando o preço atual está abaixo do R1, pode ser visto como uma oportunidade de venda, esperando uma reversão de baixa.
            elif indicador == "Pivot.M.Classic.R3":
                valor_Pivot_R3 = valor
                if valor_close is not None:
                    if valor_close > valor_Pivot_R3:
                        recomendacao = "Compra"
                    elif valor_close < valor_Pivot_R3:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Classic.R2":
                valor_Pivot_R2 = valor
                if valor_close is not None:
                    if valor_close > valor_Pivot_R2:
                        recomendacao = "Compra"
                    elif valor_close < valor_Pivot_R2:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Classic.R1":
                valor_Pivot_R1 = valor
                if valor_close is not None:
                    if valor_close > valor_Pivot_R1:
                        recomendacao = "Compra"
                    elif valor_close < valor_Pivot_R1:
                        recomendacao = "Venda"

            # Compra: Quando o preço atual está abaixo do ponto de pivô Fibonacci S3, pode ser visto como uma oportunidade de compra, esperando que o preço reverta para cima.
            # Venda: Quando o preço atual está acima do ponto de pivô Fibonacci S3, pode ser visto como uma oportunidade de venda, esperando que o preço reverta para baixo.
            elif indicador == "Pivot.M.Fibonacci.S3":
                valor_Fibonacci_S3 = valor
                if valor_close is not None:
                    if valor_close < valor_Fibonacci_S3:
                        recomendacao = "Compra"
                    elif valor_close > valor_Fibonacci_S3:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Fibonacci.S2":
                valor_Fibonacci_S2 = valor
                if valor_close is not None:
                    if valor_close < valor_Fibonacci_S2:
                        recomendacao = "Compra"
                    elif valor_close > valor_Fibonacci_S2:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Fibonacci.S1":
                valor_Fibonacci_S1 = valor
                if valor_close is not None:
                    if valor_close < valor_Fibonacci_S1:
                        recomendacao = "Compra"
                    elif valor_close > valor_Fibonacci_S1:
                        recomendacao = "Venda"

            # Compra: Quando o preço atual está abaixo do ponto de pivô Fibonacci Middle, pode ser visto como uma oportunidade de compra, esperando que o preço reverta para cima.
            # Venda: Quando o preço atual está acima do ponto de pivô Fibonacci Middle, pode ser visto como uma oportunidade de venda, esperando que o preço reverta para baixo.           
            elif indicador == "Pivot.M.Fibonacci.Middle":
                valor_Fibonacci_Middle = valor
                if valor_close is not None:
                    if valor_close < valor_Fibonacci_Middle:
                        recomendacao = "Compra"
                    elif valor_close > valor_Fibonacci_Middle:
                        recomendacao = "Venda"

            # Compra: Quando o preço atual está acima do ponto de pivô Fibonacci R1, isso pode indicar uma resistência quebrada e um possível movimento ascendente adicional.
            # Venda: Quando o preço atual está abaixo do ponto de pivô Fibonacci R1, isso pode indicar uma resistência válida e um possível movimento descendente.
            elif indicador == "Pivot.M.Fibonacci.R1":
                valor_Fibonacci_R1 = valor
                if valor_close is not None:
                    if valor_close < valor_Fibonacci_R1:
                        recomendacao = "Compra"
                    elif valor_close > valor_Fibonacci_R1:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Fibonacci.R2":
                valor_Fibonacci_R2 = valor
                if valor_close is not None:
                    if valor_close < valor_Fibonacci_R2:
                        recomendacao = "Compra"
                    elif valor_close > valor_Fibonacci_R2:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Fibonacci.R3":
                valor_Fibonacci_R3 = valor
                if valor_close is not None:
                    if valor_close < valor_Fibonacci_R3:
                        recomendacao = "Compra"
                    elif valor_close > valor_Fibonacci_R3:
                        recomendacao = "Venda"

            # Compra:Quando o preço atual está acima do ponto de pivô Camarilla S3, isso pode indicar uma resistência quebrada e um possível movimento ascendente adicional.
            # Venda:Quando o preço atual está abaixo do ponto de pivô Camarilla S3, isso pode indicar um suporte válido e um possível movimento descendente.
            elif indicador == "Pivot.M.Camarilla.S3":
                valor_Camarilla_S3 = valor
                if valor_close is not None:
                    if valor_close > valor_Camarilla_S3:
                        recomendacao = "Compra"
                    elif valor_close < valor_Camarilla_S3:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Camarilla.S2":
                valor_Camarilla_S2 = valor
                if valor_close is not None:
                    if valor_close > valor_Camarilla_S2:
                        recomendacao = "Compra"
                    elif valor_close < valor_Camarilla_S2:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Camarilla.S1":
                valor_Camarilla_S1 = valor
                if valor_close is not None:
                    if valor_close > valor_Camarilla_S1:
                        recomendacao = "Compra"
                    elif valor_close < valor_Camarilla_S1:
                        recomendacao = "Venda"

            # Compra: Quando o preço atual está acima do ponto de pivô Camarilla Middle, isso pode indicar uma resistência quebrada e um possível movimento ascendente adicional.
            # Venda: Quando o preço atual está abaixo do ponto de pivô Camarilla Middle, isso pode indicar um suporte válido e um possível movimento descendente.
            elif indicador == "Pivot.M.Camarilla.Middle":
                valor_Camarilla_Middle = valor
                if valor_close is not None:
                    if valor_close > valor_Camarilla_Middle:
                        recomendacao = "Compra"
                    elif valor_close < valor_Camarilla_Middle:
                        recomendacao = "Venda"

            # Compra: Quando o preço atual está acima do ponto de pivô Camarilla R1, 
            # isso pode indicar uma quebra de resistência e um possível movimento ascendente adicional.

            # Venda: Quando o preço atual está abaixo do ponto de pivô Camarilla R1, 
            # isso pode indicar que o preço pode ter dificuldade em ultrapassar esse nível de resistência, sugerindo um possível movimento descendente.
            elif indicador == "Pivot.M.Camarilla.R1":
                valor_Camarilla_R1 = valor
                if valor_close is not None:
                    if valor_close > valor_Camarilla_R1:
                        recomendacao = "Compra"
                    elif valor_close < valor_Camarilla_R1:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Camarilla.R2":
                valor_Camarilla_R2 = valor
                if valor_close is not None:
                    if valor_close > valor_Camarilla_R2:
                        recomendacao = "Compra"
                    elif valor_close < valor_Camarilla_R2:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Camarilla.R3":
                valor_Camarilla_R3 = valor
                if valor_close is not None:
                    if valor_close > valor_Camarilla_R3:
                        recomendacao = "Compra"
                    elif valor_close < valor_Camarilla_R3:
                        recomendacao = "Venda"

            # Compra: Quando o preço atual está acima do ponto de pivô Woodie S3, 
            # isso pode indicar que o preço encontrou suporte e pode se recuperar para cima.

            # Venda: Quando o preço atual está abaixo do ponto de pivô Woodie S3, 
            # isso pode indicar que o preço pode ter dificuldade em ultrapassar esse nível de suporte, sugerindo um possível movimento descendente.
            elif indicador == "Pivot.M.Woodie.S3":
                valor_Woodie_S3 = valor
                if valor_close is not None:
                    if valor_close > valor_Woodie_S3:
                        recomendacao = "Compra"
                    elif valor_close < valor_Woodie_S3:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Woodie.S2":
                valor_Woodie_S2 = valor
                if valor_close is not None:
                    if valor_close > valor_Woodie_S2:
                        recomendacao = "Compra"
                    elif valor_close < valor_Woodie_S2:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Woodie.S1":
                valor_Woodie_S1 = valor
                if valor_close is not None:
                    if valor_close > valor_Woodie_S1:
                        recomendacao = "Compra"
                    elif valor_close < valor_Woodie_S1:
                        recomendacao = "Venda"
            
            # Compra: Quando o preço atual está acima do ponto de pivô Woodie Middle, 
            # isso pode indicar que o preço encontrou suporte e pode se recuperar para cima.
            
            # Venda: Quando o preço atual está abaixo do ponto de pivô Woodie Middle, 
            # isso pode indicar que o preço pode ter dificuldade em ultrapassar esse nível de suporte, sugerindo um possível movimento descendente.

            elif indicador == "Pivot.M.Woodie.Middle":
                valor_Woodie_Middle = valor
                if valor_close is not None:
                    if valor_close > valor_Woodie_Middle:
                        recomendacao = "Compra"
                    elif valor_close < valor_Woodie_Middle:
                        recomendacao = "Venda"

            # Compra: Quando o preço atual está acima do ponto de pivô Woodie R1, 
            # isso pode indicar que o preço encontrou suporte e pode continuar a subir.

            # Venda: Quando o preço atual está abaixo do ponto de pivô Woodie R1, 
            # isso pode indicar que o preço pode ter dificuldade em ultrapassar esse nível de resistência, sugerindo um possível movimento descendente.

            elif indicador == "Pivot.M.Woodie.R1":
                valor_Woodie_R1 = valor
                if valor_close is not None:
                    if valor_close > valor_Woodie_R1:
                        recomendacao = "Compra"
                    elif valor_close < valor_Woodie_R1:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Woodie.R2":
                valor_Woodie_R2 = valor
                if valor_close is not None:
                    if valor_close > valor_Woodie_R2:
                        recomendacao = "Compra"
                    elif valor_close < valor_Woodie_R2:
                        recomendacao = "Venda"
            
            elif indicador == "Pivot.M.Woodie.R3":
                valor_Woodie_R3 = valor
                if valor_close is not None:
                    if valor_close > valor_Woodie_R3:
                        recomendacao = "Compra"
                    elif valor_close < valor_Woodie_R3:
                        recomendacao = "Venda"

            # Compra: Quando o preço atual está acima do ponto de pivô Demark S1, 
            # isso pode indicar que o preço encontrou suporte e pode continuar a subir.

            # Venda: Quando o preço atual está abaixo do ponto de pivô Demark S1, 
            # isso pode indicar que o preço pode ter dificuldade em ultrapassar esse nível de resistência, sugerindo um possível movimento descendente.
            elif indicador == "Pivot.M.Demark.S1":
                valor_Demark_S1 = valor
                if valor_close is not None:
                    if valor_close > valor_Demark_S1:
                        recomendacao = "Compra"
                    elif valor_close < valor_Demark_S1:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Demark.Middle":
                valor_Demark_Middle = valor
                if valor_close is not None:
                    if valor_close > valor_Demark_Middle:
                        recomendacao = "Compra"
                    elif valor_close < valor_Demark_Middle:
                        recomendacao = "Venda"

            elif indicador == "Pivot.M.Demark.R1":
                valor_Demark_R1 = valor
                if valor_close is not None:
                    if valor_close > valor_Demark_R1:
                        recomendacao = "Compra"
                    elif valor_close < valor_Demark_R1:
                        recomendacao = "Venda"

            elif indicador == "P.SAR":
                valor_P_SAR = valor
                if valor_close is not None:
                    if valor_close > valor_P_SAR:
                        recomendacao = "Compra"
                    elif valor_close < valor_P_SAR:
                        recomendacao = "Venda"

            elif indicador == "BB.lower":
                valor_BB_lower = valor
                if valor_close is not None:
                    if valor_close <= valor_BB_lower:
                        recomendacao = "Compra"
                    elif valor_close >= valor_BB_lower:
                        recomendacao = "Venda"


            elif indicador == "BB.upper":
                valor_BB_upper = valor
                if valor_close is not None:
                    if valor_close <= valor_BB_upper:
                        recomendacao = "Compra"
                    elif valor_close >= valor_BB_upper:
                        recomendacao = "Venda"


                        # "P.SAR", "BB.lower", "BB.upper", "AO[2]"


            else:
                recomendacao = "Sem recomendação"

            # Comando SQL para atualizar dados na tabela
            update_query = "UPDATE indicadores2 SET recomendacao = %s WHERE empresa = %s AND indicador = %s"
            cursor.execute(update_query, (recomendacao, empresa, indicador))

    # Confirmar as alterações no banco de dados
    conn.commit()
    print("Dados atualizados com sucesso!")

except mysql.connector.Error as e:
    print(f"Erro ao acessar o MySQL: {e}")

finally:
    # Fechar a conexão com o banco de dados
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexão ao MySQL encerrada.")