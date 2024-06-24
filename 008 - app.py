from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configuração do banco de dados MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'financeiro'
}

# Função para calcular a recomendação com base no valor do indicador
def calcular_recomendacao(indicador, valor, fechamento=None):
    if indicador in ["RSI", "RSI[1]", "Stoch.K", "Stoch.D", "Stoch.K[1]", "Stoch.D[1]"]:
        if valor > 70:
            return "Venda"
        elif valor < 30:
            return "Compra"
        else:
            return "Neutro"
    elif indicador in ["MACD.macd", "MACD.signal"]:
        if valor > 0:
            return "Compra"
        else:
            return "Venda"
    elif indicador in ["CCI20", "CCI20[1]"]:
        if valor < -100:
            return "Compra"
        elif valor > 100:
            return "Venda"
        else:
            return "Neutro"
    elif indicador in ["ADX", "ADX+DI", "ADX-DI", "ADX+DI[1]", "ADX-DI[1]", "AO", "AO[1]", "Mom", "Mom[1]"]:
        if valor > 50:
            return "Venda"
        elif valor < 50:
            return "Compra"
        else:
            return "Neutro"
    elif indicador in ["Rec.Stoch.RSI", "Stoch.RSI.K", "Rec.WR", "W.R", "Rec.BBPower", "BBPower", "Rec.UO", "UO"]:
        if valor > 0:
            return "Venda"
        elif valor < 0:
            return "Compra"
        else:
            return "Neutro"
    elif indicador in ["close"]:
        return valor

    elif indicador in ["EMA5"]:
        return valor
        
    else:
        return "Sem recomendação"

# Função para conectar ao banco de dados e obter os indicadores para uma empresa específica
def get_indicadores(empresa):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM indicadores2 WHERE empresa = %s", (empresa,))
    indicadores = cursor.fetchall()
    # Calcular a recomendação para cada indicador
    for indicador in indicadores:
        indicador['recomendacao'] = calcular_recomendacao(indicador['indicador'], indicador['valor'])
    conn.close()
    return indicadores

# Rota para exibir os indicadores em uma tabela HTML
@app.route('/empresa/<empresa>')
def mostrar_indicadores(empresa):
    indicadores = get_indicadores(empresa)
    return render_template('empresa.html', empresa=empresa, indicadores=indicadores)

if __name__ == '__main__':
    app.run(debug=True)
