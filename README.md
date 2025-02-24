# 📝 Postify – Teste Técnico
**Descrição do projeto:** Aplicação API Flask de rede social para postagens de texto.  

---

## Sumário
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Arquitetura do projeto](#arquitetura-do-projeto)
- [Endpoints da API](#endpoints-da-api)
- [Como rodar](#como-rodar)
- [Testes Postman](#testes-postman)
- [Créditos](#créditos)

---

## Tecnologias utilizadas
- **Flask** – Framework web para a API
- **SQLAlchemy** – ORM para banco de dados
- **PostgreSQL** – Banco de dados relacional
- **Flask-Login** – Autenticação de usuários
- **Flask-RestX** – Organização de rotas e integração com Swagger
- **Swagger** – Documentação automática da API

---
## Arquitetura do projeto
```bash
📂 postify-app/
    L 📂 controllers/                               # definição de rotas e funções
        L 📄 auth_controllers.py
        L 📄 post_controllers.py
        L 📄 user_controllers.py
    L 📄 __init__.py
    L 📄 app_config.py                              # configuração das extensões e rotas da API            
    L 📄 app.py                                     # inicialização da aplicação Flask e execução do server
    L 📄 db_config.py                               # configuração do banco de dados PostgreSQL
    L 📄 models.py                                  # modelos das entidades (usuários e postagens)
📂 postman-tests/
    L 📄 Postify-Testes.postman_collection.json     # arquivo de testes para o Postman
📄 .gitignore
📄 README.md
📄 requirements.txt                                 # requisitos para rodar o projeto
```

---

## Endpoints da API
URL BASE: http://127.0.0.1:5000/api

- **Autenticação:**
    - **/login (POST)** - Faz o login
    - **/logout (POST)** - Faz o logout do usuário logado (login obrigatório)
    - **/status (GET)** - Mostra qual o usuário logado (login obrigatório)
- **Usuário:**
    - **/users/ (POST)** - Criação de usuário novo
    - **/users/ (GET)** - Busca e listagem de todos os usuários (login obrigatório)
    - **/users/{user_id} (GET)** - Busca de usuário por ID (login obrigatório)
    - **/users/{username} (PUT)** - Edição de usuário por username (login obrigatório)
    - **/users/{username} (DELETE)** - Deletar usuário por username (login obrigatório)
- **Postagem:**
    - **/posts/new-post: (POST)** - Criação de postagem nova (login obrigatório)
    - **/posts/all-posts: (GET)** - Busca e listagem de todas as postagens (login obrigatório)
    - **/posts/user/{username}: (GET)** - Busca de listagem de todas as postagens de um usuário específico (login obrigatório)
    - **/posts/my-posts: (GET)** - Listagem de todas as postagens do usuário logado (login obrigatório)
    - **/posts/post/(post_id): (GET)** - Busca de postagem por ID (login obrigatório)
    - **/posts/post/(post_id): (PUT)** - Edição de postagem (login obrigatório)
    - **/posts/post/(post_id): (DELETE)** - Deletar postagem (login obrigatório)

---

## Como rodar

#### Pré-requisitos:
Antes de rodar o projeto, tenha certeza de ter instalados:
- Python
- PostgreSQL
- Postman
- PgAdmin, DBeaver, ou algum outro SGDB compatível com PostgreSQL para melhor checagem do banco de dados (opcional)
</br>

**1. Clone o repositório:**
   ```bash
   git clone https://github.com/beaalmeidas/Postify-TesteTecnico.git
   ```
</br>

**2. Ao abrir a pasta em um editor de texto e abrir um novo terminal, use o seguinte comando para criar um ambiente virtual:**
   ```bash
   python -m venv venv
   venv/Scripts/activate
    # Para Mac/Linux:
    # python3 -m venv venv
    # source venv/bin/activate
   ```
</br>

**3. Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
</br>

**4. Configure o banco de dados:**
   ```bash
    # Usuário: admin
    # Senha: 1234
    # Banco de dados: postify_db

   # Crie o banco
    CREATE DATABASE postify_db;

    # Conecte-se com o banco
    \c postify_db;

    # Crie a tabela de usuário
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        user_email VARCHAR(120) UNIQUE NOT NULL,
        user_password VARCHAR(255) NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,
        is_admin BOOLEAN DEFAULT FALSE
    );

    # Crie a tabela de postagens:
    CREATE TABLE posts (
        post_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        post_content TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    );

    # Rode as migrações:
    cd postify-app
    flask db upgrade
   ```

</br>

**5. Rode a aplicação:**
```bash
    cd postify-app
    flask run
```

**A API estará rodando na porta http://127.0.0.1:5000/, onde o Swagger estará disponível.**

---

## Testes Postman
**Utilize a [coleção de testes Postman](./postman-tests/Postify-Testes.postman_collection.json) incluída no projeto para testar os endpoints.**


Para utilizar os testes no Postman:

1. **Abra o Postman**.
2. **Importe a coleção**:
   - Clique em "Import" no canto superior esquerdo.
   - Selecione o arquivo `Postify-Testes.postman_collection.json` localizado na pasta `postman-tests/`.
3. **Execute os testes**:
   - Após a importação, você pode selecionar os testes desejados e executá-los para validar os endpoints da API.

---

## Créditos
Beatriz Almeida de Souza Silva </br>
Fevereiro de 2025.