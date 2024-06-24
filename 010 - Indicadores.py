from flask import Flask, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuração do banco de dados MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'financeiro'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

@app.route('/api/indicadores', methods=['GET'])
def get_indicadores():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    cursor = connection.cursor(dictionary=True)
    query = "SELECT data, empresa, indicador, valor FROM indicadores"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(rows)

@app.route('/indicadores', methods=['GET'])
def mostrar_indicadores():
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados", 500

    cursor = connection.cursor(dictionary=True)
    query = "SELECT data, empresa, indicador, valor FROM indicadores"
    cursor.execute(query)
    indicadores = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('empresa.html', indicadores=indicadores)

if __name__ == '__main__':
    app.run(debug=True)
