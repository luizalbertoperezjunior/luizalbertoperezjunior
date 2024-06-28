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

# Função para obter os indicadores com paginação
def obter_indicadores_paginados(empresa_selecionada=None, pagina=1, itens_por_pagina=20):
    # Conecta ao banco de dados MySQL
    connection = mysql.connector.connect(**db_config)

    # Prepara a query SQL para contar o total de registros
    query_total = "SELECT COUNT(*) AS total FROM indicadores"
    cursor_total = connection.cursor()
    cursor_total.execute(query_total)
    total_registros = cursor_total.fetchone()[0]
    cursor_total.close()

    # Calcula o total de páginas
    total_paginas = total_registros // itens_por_pagina
    if total_registros % itens_por_pagina != 0:
        total_paginas += 1

    # Calcula o índice inicial para a página atual
    indice_inicio = (pagina - 1) * itens_por_pagina

    # Prepara a query SQL para selecionar os indicadores com paginação
    if empresa_selecionada:
        query_indicadores = "SELECT * FROM indicadores WHERE empresa = %s LIMIT %s, %s"
        parametros = (empresa_selecionada, indice_inicio, itens_por_pagina)
    else:
        query_indicadores = "SELECT * FROM indicadores LIMIT %s, %s"
        parametros = (indice_inicio, itens_por_pagina)

    cursor_indicadores = connection.cursor(dictionary=True)
    cursor_indicadores.execute(query_indicadores, parametros)
    indicadores = cursor_indicadores.fetchall()
    cursor_indicadores.close()

    # Fecha a conexão com o banco de dados
    connection.close()

    return indicadores, total_paginas

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

        # Chama a função para obter os indicadores com paginação
        indicadores, total_paginas = obter_indicadores_paginados(empresa_selecionada=empresa_selecionada)

        # Fecha o cursor e a conexão com o banco de dados
        cursor_empresas.close()
        connection.close()

        # Renderiza o template HTML e passa os dados dos indicadores, empresas e paginação
        return render_template('index2.html', indicadores=indicadores, empresas=empresas,
                               paginacao=True, pagina=1, total_paginas=total_paginas)

    else:
        # Se o método for GET (primeiro acesso), exibe a primeira página de indicadores
        indicadores, total_paginas = obter_indicadores_paginados()

        # Fecha o cursor e a conexão com o banco de dados
        cursor_empresas.close()
        connection.close()

        # Renderiza o template HTML e passa os dados dos indicadores, empresas e paginação
        return render_template('index2.html', indicadores=indicadores, empresas=empresas,
                               paginacao=True, pagina=1, total_paginas=total_paginas)

if __name__ == '__main__':
    app.run(debug=True)
