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

# Rota para exibir os indicadores financeiros
@app.route('/', methods=['GET', 'POST'])
def index():
    # Conecta ao banco de dados MySQL
    connection = mysql.connector.connect(**db_config)

    # Prepara a query SQL para selecionar as empresas distintas
    query_empresas = "SELECT DISTINCT empresa FROM indicadores"
    cursor_empresas = connection.cursor()
    cursor_empresas.execute(query_empresas)
    empresas = [empresa[0] for empresa in cursor_empresas.fetchall()]

    # Verifica se o formulário foi submetido
    if request.method == 'POST':
        # Obtém o valor selecionado no campo de seleção de empresa
        empresa_selecionada = request.form['empresa']

        # Prepara a query SQL para selecionar os indicadores filtrados
        if empresa_selecionada:
            query_indicadores = "SELECT * FROM indicadores WHERE empresa = %s"
            cursor_indicadores = connection.cursor(dictionary=True)
            cursor_indicadores.execute(query_indicadores, (empresa_selecionada,))
            indicadores = cursor_indicadores.fetchall()
            cursor_indicadores.close()
        else:
            # Se nenhuma empresa selecionada, exibe todos os indicadores
            query_indicadores = "SELECT * FROM indicadores"
            cursor_indicadores = connection.cursor(dictionary=True)
            cursor_indicadores.execute(query_indicadores)
            indicadores = cursor_indicadores.fetchall()
            cursor_indicadores.close()
    else:
        # Se o método for GET (primeiro acesso), exibe todos os indicadores
        query_indicadores = "SELECT * FROM indicadores"
        cursor_indicadores = connection.cursor(dictionary=True)
        cursor_indicadores.execute(query_indicadores)
        indicadores = cursor_indicadores.fetchall()
        cursor_indicadores.close()

    # Fecha o cursor e a conexão com o banco de dados
    cursor_empresas.close()
    connection.close()

    # Renderiza o template HTML e passa os dados dos indicadores e das empresas
    return render_template('index4.html', indicadores=indicadores, empresas=empresas)



if __name__ == '__main__':
    app.run(debug=True)