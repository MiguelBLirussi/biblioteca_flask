import sqlite3

DB_NAME = "biblioteca.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabela():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                ano TEXT NOT NULL,
                disponivel INTEGER NOT NULL
            )
        ''')
        conn.commit()