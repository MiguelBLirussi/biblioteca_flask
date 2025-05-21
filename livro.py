from datetime import datetime

class Livro:
    def __init__(self, id, titulo, autor, ano, disponivel=True):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.disponivel = disponivel
        self.historico = []

    def __str__(self):
        status = '✅' if self.disponivel else '❌'
        return f'ID:{self.id} | Título:{self.titulo} | Autor:{self.autor} | Ano:{self.ano} | Disponível:{status}'

    def exibir_historico(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT data, acao FROM historico WHERE livro_id = ? ORDER BY data", (self.id,))
        registros = cursor.fetchall()
        if not registros:
            print("Nenhum histórico disponível para este livro.")
            return
        print(f"Histórico do livro '{self.titulo}':")
        for data, acao in registros:
            print(f"{data} - {acao}")

    @staticmethod
    def criar_tabela(conn):
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

    @staticmethod
    def inserir(conn, titulo, autor, ano):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO livros (titulo, autor, ano) VALUES (?, ?, ?)", (titulo, autor, ano))
        conn.commit()

    @staticmethod
    def listar_todos(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor, ano, disponivel FROM livros")
        resultados = cursor.fetchall()
        return [Livro(id, titulo, autor, ano, bool(disponivel)) for id, titulo, autor, ano, disponivel in resultados]

    @staticmethod
    def buscar_por_id(conn, id):
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor, ano, disponivel FROM livros WHERE id = ?", (id,))
        resultado = cursor.fetchone()
        if resultado:
            return Livro(*resultado)
        return None

    @staticmethod
    def buscar_por_titulo(conn, titulo):
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor, ano, disponivel FROM livros WHERE titulo LIKE ?", ('%' + titulo + '%',))
        resultados = cursor.fetchall()
        return [Livro(id, titulo, autor, ano, bool(disponivel)) for id, titulo, autor, ano, disponivel in resultados]

    @staticmethod
    def buscar_por_autor(conn, autor):
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor, ano, disponivel FROM livros WHERE autor LIKE ?", ('%' + autor + '%',))
        resultados = cursor.fetchall()
        return [Livro(id, titulo, autor, ano, bool(disponivel)) for id, titulo, autor, ano, disponivel in resultados]

    @staticmethod
    def emprestar(conn, id):
        cursor = conn.cursor()
        cursor.execute("SELECT disponivel FROM livros WHERE id = ?", (id,))
        resultado = cursor.fetchone()
        if resultado and resultado[0]:  # Se disponível
            cursor.execute("UPDATE livros SET disponivel = 0 WHERE id = ?", (id,))
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO historico (livro_id, data, acao) VALUES (?, ?, ?)", (id, data, "Emprestado"))
            conn.commit()

    @staticmethod
    def devolver(conn, id):
        cursor = conn.cursor()
        cursor.execute("SELECT disponivel FROM livros WHERE id = ?", (id,))
        resultado = cursor.fetchone()
        if resultado and not resultado[0]:  # Se não estiver disponível
            cursor.execute("UPDATE livros SET disponivel = 1 WHERE id = ?", (id,))
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO historico (livro_id, data, acao) VALUES (?, ?, ?)", (id, data, "Devolvido"))
            conn.commit()