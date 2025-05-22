import sqlite3
from datetime import datetime

def criar_conexao():
    return sqlite3.connect('biblioteca.db')

def criar_tabela():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano TEXT NOT NULL,
            disponivel INTEGER NOT NULL DEFAULT 1
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            acao TEXT NOT NULL,
            FOREIGN KEY(livro_id) REFERENCES livros(id)
        )
    ''')
    conn.commit()
    conn.close()

def inserir_livro(titulo, autor, ano):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livros (titulo, autor, ano, disponivel) VALUES (?, ?, ?, 1)', (titulo, autor, ano))
    conn.commit()
    conn.close()

def listar_livros():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    conn.close()
    return livros

def buscar_livro_por_id(id):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros WHERE id = ?', (id,))
    livro = cursor.fetchone()
    conn.close()
    return livro

def buscar_livro_por_titulo(titulo):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livros WHERE titulo LIKE ?', ('%' + titulo + '%',))
    livros = cursor.fetchall()
    conn.close()
    return livros

def atualizar_livro(id, titulo, autor, ano):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('UPDATE livros SET titulo = ?, autor = ?, ano = ? WHERE id = ?', (titulo, autor, ano, id))
    conn.commit()
    conn.close()

def deletar_livro(id):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livros WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def emprestar(id):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT disponivel FROM livros WHERE id = ?', (id,))
    resultado = cursor.fetchone()
    if resultado and resultado[0]:  # Se disponível
        cursor.execute('UPDATE livros SET disponivel = 0 WHERE id = ?', (id,))
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO historico (livro_id, data, acao) VALUES (?, ?, ?)', (id, data, 'Emprestado'))
        conn.commit()
    conn.close()

def devolver(id):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT disponivel FROM livros WHERE id = ?', (id,))
    resultado = cursor.fetchone()
    if resultado and not resultado[0]:  # Se não estiver disponível
        cursor.execute('UPDATE livros SET disponivel = 1 WHERE id = ?', (id,))
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO historico (livro_id, data, acao) VALUES (?, ?, ?)', (id, data, 'Devolvido'))
        conn.commit()
    conn.close()