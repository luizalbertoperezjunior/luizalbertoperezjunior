import pandas_datareader.data as web

symbol = 'PETR4.SA'
start_date = '2024-02-01'
end_date = '2024-02-22'

df = web.DataReader(symbol, 'yahoo', start_date, end_date)
print(df)
