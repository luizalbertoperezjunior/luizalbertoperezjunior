from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Configuração do banco de dados MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'financeiro'
}

# Função para conectar ao banco de dados e consultar os indicadores
def get_indicadores():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM indicadores")
    indicadores = cursor.fetchall()
    conn.close()
    return indicadores

# Rota para obter os indicadores
@app.route('/indicadores')
def indicadores():
    indicadores = get_indicadores()
    return jsonify(indicadores)

if __name__ == '__main__':
    app.run(debug=True)
