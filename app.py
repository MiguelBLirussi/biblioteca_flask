import sys
import os
from livro import Livro
import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect("biblioteca.db")
cursor = conn.cursor()

def main():
    os.system("cls" if os.name == "nt" else "clear")
    Livro.criar_tabela(conn)
    while True:
        exibir_menu()
        comando = tarefa_desejada()
        chamar_tarefa(comando)

def voltar_menu():
    print("\nTarefa finalizada!\nVoltando ao Menu Principal...")
    input("Aperte 'Enter' para voltar ao Menu Principal")
    os.system("cls" if os.name == "nt" else "clear")

def exibir_menu():
    print('Gerenciamento de Biblioteca')
    print('1. Adicionar livro')
    print('2. Listar todos os livros')
    print('3. Buscar livro por título ou autor')
    print('4. Emprestar ou devolver um livro')
    print('5. Exibir histórico de empréstimos de um livro')
    print('6. Sair')

def tarefa_desejada():
    while True:
        comando = input('Digite o número da opção desejada: ')
        try:
            comando = int(comando)
            if 1 <= comando <= 6:
                return comando
        except:
            pass
        print("Por favor digite um comando válido...")

def adicionar_livro():
    os.system("cls" if os.name == "nt" else "clear")
    print("Vamos adicionar um novo livro")
    titulo = input("Qual o nome do livro?\n")
    autor = input("Perfeito, qual o autor do livro?\n")
    ano = input("De qual ano é o livro?\n")
    Livro.inserir(conn, titulo, autor, ano)
    voltar_menu()

def listar_livros():
    os.system("cls" if os.name == "nt" else "clear")
    livros = Livro.listar_todos(conn)
    if not livros:
        print("Não há livros na biblioteca.")
    else:
        print("Listando Livros:")
        for livro in livros:
            print(livro)
    voltar_menu()

def buscar_livro():
    os.system("cls" if os.name == "nt" else "clear")
    while True:
        print("Buscando Livro...")
        comando = input("Deseja procurar pelo título ou autor?\n 1. Título | 2. Autor | 3. Menu\n")
        try:
            comando = int(comando)
            if comando == 1:
                termo = input("Digite o título:\n").strip()
                resultados = Livro.buscar_por_titulo(conn, termo)
            elif comando == 2:
                termo = input("Digite o autor:\n").strip()
                resultados = Livro.buscar_por_autor(conn, termo)
            elif comando == 3:
                voltar_menu()
                return
            else:
                raise ValueError

            if resultados:
                for livro in resultados:
                    print(livro)
            else:
                print("Nenhum livro encontrado.")
            break
        except ValueError:
            print("Opção inválida.")
    voltar_menu()

def editar_livro():
    os.system("cls" if os.name == "nt" else "clear")
    id_livro = input("Digite o ID do livro que deseja emprestar ou devolver: ")
    livro = Livro.buscar_por_id(conn, id_livro)
    if not livro:
        print(f"Nenhum livro com ID {id_livro} foi encontrado.")
    else:
        if livro.disponivel:
            Livro.emprestar(conn, id_livro)
            print(f"O livro '{livro.titulo}' foi emprestado.")
        else:
            Livro.devolver(conn, id_livro)
            print(f"O livro '{livro.titulo}' foi devolvido.")
    voltar_menu()

def exibir_historico():
    os.system("cls" if os.name == "nt" else "clear")
    id_livro = input("Digite o ID do livro para ver o histórico: ")
    livro = Livro.buscar_por_id(conn, id_livro)
    if not livro:
        print(f"Nenhum livro com ID {id_livro} foi encontrado.")
    else:
        livro.exibir_historico(conn)
    voltar_menu()

def fechar_programa():
    print("Fechando o sistema...")
    conn.close()
    sys.exit()

def chamar_tarefa(comando):
    if comando == 1:
        adicionar_livro()
    elif comando == 2:
        listar_livros()
    elif comando == 3:
        buscar_livro()
    elif comando == 4:
        editar_livro()
    elif comando == 5:
        exibir_historico()
    elif comando == 6:
        fechar_programa()

if __name__ == "__main__":
    main()