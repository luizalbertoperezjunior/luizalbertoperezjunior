import pandas as pd
import yfinance as yf

# Definir símbolo das ações
empresas = ["PETR3.SA", "PETR4.SA", "WEGE3.SA","ITUB4.SA"]

for empresa in empresas:
    # Obter dados dos últimos 10 dias
    hoje = pd.to_datetime("today")
    data_inicio = hoje - pd.Timedelta(days=30)
    dados_acoes = yf.download(empresa, start=data_inicio, end=hoje)
    
    # Salvar dados em Excel
    print(empresa)
    nome_arquivo = f"C:/Users/luizperez/Documents/Apostila/Python/Finan/{empresa}.xlsx"
    dados_acoes.to_excel(nome_arquivo)

    print(f"Dados salvos em {nome_arquivo}")

    # Exibir dados
    print(dados_acoes)




