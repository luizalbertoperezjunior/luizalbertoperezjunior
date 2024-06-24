from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Configuração do banco de dados MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'financeiro'
}

# Rota para exibir os indicadores financeiros
@app.route('/')
def index():
    # Conecta ao banco de dados MySQL
    connection = mysql.connector.connect(**db_config)

    # Prepara a query SQL para selecionar os indicadores
    query = "SELECT * FROM indicadores2"

    # Executa a query
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)

    # Obtém todos os resultados da query
    indicadores = cursor.fetchall()

    # Fecha o cursor e a conexão com o banco de dados
    cursor.close()
    connection.close()

    # Renderiza o template HTML e passa os dados dos indicadores
    return render_template('index.html', indicadores=indicadores)

if __name__ == '__main__':
    app.run(debug=True)
