import pandas as pd
from tradingview_ta import TA_Handler, Interval

# Definir símbolo das ações
empresas = ["PETR3", "PETR4", "WEGE3", "ITUB4"]

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

# Definindo os osciladores desejados
oscillators_desejados = ["RECOMMENDATION","BUY","SELL","NEUTRAL","COMPUTE"]

# Dicionários para armazenar os indicadores e osciladores de cada empresa
indicadores_empresas = {}
oscillators_empresas = {}

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

    # Obtendo os osciladores
    oscillators = tesla.get_analysis().oscillators 
    oscillators_empresas[empresa] = oscillators

    # Extraindo e exibindo valores dos osciladores desejados
    valores_oscillators = {}
    for oscilador in oscillators_desejados:
        valores_oscillators[oscilador] = oscillators.get(oscilador, None)
        print(oscilador, ":", valores_oscillators[oscilador])

    # Convertendo os osciladores em DataFrame
    table_oscillators = pd.DataFrame.from_dict(oscillators, orient='index', columns=[tesla.symbol])
    
    # Obtendo e convertendo as médias móveis
    moving_averages = tesla.get_analysis().moving_averages  
    table_moving_averages = pd.DataFrame.from_dict(moving_averages, orient='index', columns=[tesla.symbol])

    # Criando um dicionário para armazenar os valores dos indicadores desejados
    valores_indicadores = {}
    for indicador in indicadores_desejados:
        valores_indicadores[indicador] = indicators.get(indicador, None)
        print(indicador, ":", valores_indicadores[indicador])

    # Obtendo outros indicadores
    momentum = tesla.get_analysis().indicators["Mom"]
    momentum_macd = tesla.get_analysis().indicators["MACD.macd"]

    # Salvando os valores dos indicadores em um arquivo Excel
    with pd.ExcelWriter(f'C:/Users/luizperez/Documents/Apostila/Python/Finan/{empresa}.xlsx') as writer:
        pd.DataFrame.from_dict(valores_indicadores, orient='index', columns=[tesla.symbol]).to_excel(writer, sheet_name='Indicadores')
        table_oscillators.to_excel(writer, sheet_name='Oscillators')
        table_moving_averages.to_excel(writer, sheet_name='Moving Averages')
        pd.DataFrame({'Momentum': [momentum]}).to_excel(writer, sheet_name='Momentum', index=False)
        pd.DataFrame({'Momentum MACD': [momentum_macd]}).to_excel(writer, sheet_name='Momentum MACD', index=False)

# Exibindo os indicadores e osciladores das empresas
print("Indicadores:", indicadores_empresas)
print("Osciladores:", oscillators_empresas)
