# 📚 Sistema de Biblioteca - Versão Flask

Este projeto é um sistema de gerenciamento de biblioteca simples que permite adicionar, listar, buscar e editar livros. Diferente da versão anterior, agora os dados são armazenados em um banco de dados **SQLite**, garantindo maior persistência e estruturação dos dados, além disso agora o foco do projeto muda para integração com o framework **Flask**, para criação de uma interface, onde o usuário vai realizar a interação.

---

## 🚀 Funcionalidades

- ✅ Cadastro de livros  
- 📖 Listagem de todos os livros  
- 🔍 Busca por título ou autor  
- 🔁 Empréstimo e devolução de livros  
- 💾 Histórico de alterações e empréstimos
- 🔒 Persistência de dados com SQLite 

---

## 🧠 Conceitos Aplicados

- Programação Orientada a Objetos (POO)  
- Modularização do código  
- Manipualação de dados com SQLite 
- Interface gráfica com Flask
- Tratamento de exceções  
- Menu interativo no terminal  
- Boas práticas com PEP8  

---

## 🗂 Estrutura do Projeto

# biblioteca_flask/
# └── README.md 
# ├── app.py - Menu principal e interação com o usuário, arquivo que roda o Flask
# ├── livro.py - Classe Livro e suas funcionalidades  
# ├── db.py - Funções para manipulação do banco de dados SQLite
# ├── biblioteca.db - Arquivo do banco de dados (criado automaticamente)
# ├── templates/
#     └── index.html - Página inicial (listar livros, formulário, etc.)
# ├── static/
#     └── style.css - CSS para estilizar as páginas

---

## ▶️ Como Executar

#1. Clone o repositório:

```bash
git clone https://github.com/MiguelBLirussi/sistema-biblioteca-terminal.git
cd biblioteca_flask
```

#2. Execute o sistema:
python app.py

---

## 💡 Próximas melhorias

Testes automatizados com unittest

---

## 🧑‍💻 Autor
Desenvolvido por MiguelBLirussi ✨

