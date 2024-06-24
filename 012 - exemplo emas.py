import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Gerar dados fictícios para simular preços de ações
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='B')
prices = pd.Series(np.random.normal(100, 1, len(dates)), index=dates).cumsum()

# Calcular EMAs para diferentes períodos
emas = {
    'EMA5': prices.ewm(span=5, adjust=False).mean(),
    'EMA10': prices.ewm(span=10, adjust=False).mean(),
    'EMA20': prices.ewm(span=20, adjust=False).mean(),
    'EMA30': prices.ewm(span=30, adjust=False).mean(),
    'EMA50': prices.ewm(span=50, adjust=False).mean(),
    'EMA100': prices.ewm(span=100, adjust=False).mean(),
    'EMA200': prices.ewm(span=200, adjust=False).mean(),
}

# Plotar os preços e EMAs
plt.figure(figsize=(14, 7))
plt.plot(prices, label='Preço de Fechamento')
for ema_name, ema_values in emas.items():
    plt.plot(ema_values, label=ema_name)
plt.legend()
plt.title('Preço de Fechamento e Médias Móveis Exponenciais (EMAs)')
plt.xlabel('Data')
plt.ylabel('Preço')
plt.grid(True)
plt.show()
