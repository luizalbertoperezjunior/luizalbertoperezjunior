import pandas as pd
from tradingview_ta import TA_Handler, Interval, Exchange
from tabulate import tabulate

# Definir símbolo das ações
empresas = ["PETR3", "PETR4", "WEGE3", "ITUB4"]

for empresa in empresas:
    
    tesla = TA_Handler(
        symbol=empresa,
        screener="brazil",
        exchange="BMFBOVESPA",
        interval=Interval.INTERVAL_1_DAY,
        # proxies={'http': 'http://
        # example.com:8080'} # Uncomment to enable proxy (replace the URL).
    )
    
    indicators = tesla.get_indicators()
    print(indicators)
    table = pd.DataFrame.from_dict(indicators, orient='index', columns=[tesla.symbol])
    print(table)
    
    oscillators = tesla.get_analysis().oscillators 
    table_oscillators = pd.DataFrame.from_dict(oscillators, orient='index', columns=[tesla.symbol])
    print(oscillators)
    moving_averages = tesla.get_analysis().moving_averages  
    table_moving_averages = pd.DataFrame.from_dict(moving_averages, orient='index', columns=[tesla.symbol])
    
    momentum = tesla.get_analysis().indicators["Mom"]
    momentum_macd = tesla.get_analysis().indicators["MACD.macd"]
    
    with pd.ExcelWriter(f'C:/Users/luizperez/Documents/Apostila/Python/Finan/{empresa}.xlsx') as writer:
        table.to_excel(writer, sheet_name='Indicators')
        table_oscillators.to_excel(writer, sheet_name='Oscillators')
        table_moving_averages.to_excel(writer, sheet_name='Moving Averages')
        pd.DataFrame({'Momentum': [momentum]}).to_excel(writer, sheet_name='Momentum', index=False)
        pd.DataFrame({'Momentum MACD': [momentum_macd]}).to_excel(writer, sheet_name='Momentum MACD', index=False)
