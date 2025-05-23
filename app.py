from flask import Flask, render_template, request, redirect, url_for
from db import (
    criar_conexao,
    criar_tabela,
    inserir_livro,
    listar_livros,
    buscar_livro_por_titulo,
    atualizar_livro,
    emprestar,
    devolver,
    buscar_livro_por_id,
    deletar_livro
)

app = Flask(__name__)

# Cria as tabelas no banco
criar_tabela()

# @app.route('/')
# def index():
#     livros = listar_livros()
#     return render_template('index.html', livros=livros)

@app.route('/')
def index():
    titulo_busca = request.args.get('titulo', '').lower()
    autor_busca = request.args.get('autor', '').lower()

    conn = criar_conexao()
    cursor = conn.cursor()

    if titulo_busca or autor_busca:
        query = "SELECT * FROM livros WHERE 1=1"
        params = []

        if titulo_busca:
            query += " AND LOWER(titulo) LIKE ?"
            params.append(f"%{titulo_busca}%")
        if autor_busca:
            query += " AND LOWER(autor) LIKE ?"
            params.append(f"%{autor_busca}%")

        cursor.execute(query, params)
    else:
        cursor.execute("SELECT * FROM livros")

    livros = cursor.fetchall()
    conn.close()
    return render_template('index.html', livros=livros)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        inserir_livro(titulo, autor, ano)
        return redirect(url_for('index'))
    return render_template('adicionar.html')

@app.route('/excluir/<int:id>')
def excluir(id):
    deletar_livro(id)
    return redirect(url_for('index'))

@app.route('/emprestar/<int:id>')
def emprestar_livro(id):
    emprestar(id)
    return redirect(url_for('index'))

@app.route('/devolver/<int:id>')
def devolver_livro(id):
    devolver(id)
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        atualizar_livro(id, titulo, autor, ano)
        return redirect(url_for('index'))
    else:
        livro = buscar_livro_por_id(id)
        return render_template('editar.html', livro=livro)

@app.route('/buscar', methods=['GET'])
def buscar():
    termo = request.args.get('termo', '')
    resultados = buscar_livro_por_titulo(termo)
    return render_template('index.html', livros=resultados)

@app.route('/detalhes/<int:id>')
def detalhes(id):
    livro = buscar_livro_por_id(id)  # sua função para buscar o livro no DB
    if livro is None:
        return "Livro não encontrado", 404
    return render_template('detalhes.html', livro=livro)

@app.route('/historico')
def ver_historico():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT h.id, l.titulo, h.data, h.acao
        FROM historico h
        JOIN livros l ON h.livro_id = l.id
        ORDER BY h.data DESC
    ''')
    historico = cursor.fetchall()
    conn.close()
    return render_template('historico.html', historico=historico)

if __name__ == '__main__':
    app.run(debug=True)