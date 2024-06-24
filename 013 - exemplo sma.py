import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Gerar dados fictícios para simular preços de ações
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='B')
prices = pd.Series(np.random.normal(100, 1, len(dates)), index=dates).cumsum()

# Calcular a SMA5
sma5 = prices.rolling(window=5).mean()

# Gerar sinais de compra e venda
signals = pd.DataFrame(index=prices.index)
signals['price'] = prices
signals['SMA5'] = sma5
signals['signal'] = 0  # Inicializando a coluna de sinais
signals['signal'][5:] = np.where(signals['price'][5:] > signals['SMA5'][5:], 1, 0)  # 1 para compra
signals['position'] = signals['signal'].diff()  # Calculando as mudanças de posição

# Plotar os preços e a SMA5
plt.figure(figsize=(14, 7))
plt.plot(prices, label='Preço de Fechamento')
plt.plot(sma5, label='SMA5', color='orange')
plt.plot(signals.loc[signals['position'] == 1.0].index, signals['SMA5'][signals['position'] == 1.0], '^', markersize=10, color='g', label='Compra')
plt.plot(signals.loc[signals['position'] == -1.0].index, signals['SMA5'][signals['position'] == -1.0], 'v', markersize=10, color='r', label='Venda')
plt.legend()
plt.title('Preço de Fechamento e SMA5 com Sinais de Compra e Venda')
plt.xlabel('Data')
plt.ylabel('Preço')
plt.grid(True)
plt.show()
