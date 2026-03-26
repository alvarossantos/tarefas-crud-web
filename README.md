# Gerenciador de Tarefas CRUD - Web

Este é um projeto de um simples aplicativo web para gerenciamento de tarefas (CRUD - Create, Read, Update, Delete), construído com Python puro, sem o uso de frameworks web como Flask ou Django. O objetivo é demonstrar os conceitos fundamentais de desenvolvimento web, arquitetura de software (MVC) e interação com banco de dados.

## ✨ Funcionalidades

*   **Criar:** Adicionar novas tarefas com título e descrição.
*   **Listar:** Visualizar todas as tarefas em uma tabela, com status (pendente/concluída).
*   **Atualizar:** Editar o título, descrição e status de uma tarefa existente.
*   **Remover:** Excluir uma tarefa.
*   **Alternar Status:** Mudar rapidamente o status de uma tarefa de "pendente" para "concluída" e vice-versa.

## 🏛️ Arquitetura

A aplicação segue o padrão de arquitetura **Model-View-Controller (MVC)** para organizar o código de forma clara e manutenível.

*   **Model (`src/model/tarefa_model.py`):**
    *   Responsável pela lógica de dados e interação com o banco de dados.
    *   A classe `TarefaDAO` (Data Access Object) encapsula todas as operações SQL (INSERT, SELECT, UPDATE, DELETE) para o banco de dados PostgreSQL.
    *   Utiliza a biblioteca `psycopg2` para se comunicar com o banco.

*   **View (`src/view/`):**
    *   Responsável pela camada de apresentação.
    *   `index.py`: Contém a classe `ServidorWeb` que herda de `BaseHTTPRequestHandler`. Ela atua como um roteador simples, tratando as requisições HTTP (GET e POST) e renderizando as páginas.
    *   `templates/`: Contém os arquivos HTML (`base.html`, `listar.html`, `form.html`) que servem como moldes para as páginas. Os dados dinâmicos são injetados nesses moldes antes de serem enviados ao navegador.

*   **Controller (`src/controller/tarefa_controller.py`):**
    *   Atua como o intermediário entre o Model e a View.
    *   Recebe as requisições da View, processa a lógica de negócio (como validações) e chama os métodos apropriados do Model para manipular os dados.
    *   Retorna os dados processados para a View exibir.

## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python 3
*   **Servidor Web:** Módulo `http.server` da biblioteca padrão do Python.
*   **Banco de Dados:** PostgreSQL
*   **Bibliotecas Python:**
    *   `psycopg2-binary`: Driver para conectar o Python ao PostgreSQL.
    *   `python-dotenv`: Para gerenciar variáveis de ambiente (credenciais do banco).

## 🚀 Como Iniciar a Aplicação

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### 1. Pré-requisitos

*   Python 3.8+
*   PostgreSQL instalado e rodando.

### 2. Configuração do Banco de Dados

1.  Acesse seu terminal PostgreSQL (ex: `psql`) e crie o banco de dados:

    ```sql
    CREATE DATABASE tarefas;
    ```

2.  Conecte-se ao banco recém-criado (`\c tarefas`) e execute o script contido no arquivo `database_tarefas.txt` para criar a tabela `tarefas` e a trigger de atualização.

### 3. Configuração do Projeto

1.  Clone o repositório:
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd tarefas-crud-web
    ```

2.  Crie e ative um ambiente virtual (recomendado):
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux / macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Instale as dependências do projeto a partir do arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  Na raiz do projeto, crie um arquivo chamado `.env`. Ele guardará as credenciais de acesso ao seu banco de dados. Preencha com suas informações, como no exemplo abaixo:

    ```env
    DB_NAME=tarefas
    DB_USER=seu_usuario_postgres
    DB_PASSWORD=sua_senha_postgres
    DB_HOST=localhost
    DB_PORT=5432
    ```

### 4. Executando a Aplicação

Com o ambiente virtual ativado e o arquivo `.env` configurado, inicie o servidor executando o `main.py`:

```bash
python main.py
```

O servidor será iniciado e você verá a seguinte mensagem no terminal:

```
Servidor iniciado em http://localhost:8080
Pressione Ctrl+C para desligar o servidor.
```

Agora, você pode acessar a aplicação em seu navegador através do endereço http://localhost:8080.

## 📂 Estrutura do Projeto

```
projeto/
│
├── src/
│   ├── model/
│   │   └── tarefa_model.py       # Lógica de dados e acesso ao BD
│   ├── view/
│   │   ├── templates/            # Arquivos HTML
│   │   └── index.py              # Servidor HTTP e renderização
│   └── controller/
│       └── tarefa_controller.py  # Lógica de negócio da aplicação
│
├── .env                          # (Criar manualmente) Credenciais do BD
├── database_tarefas.txt          # Script SQL para o banco
├── main.py                       # Ponto de entrada da aplicação
├── requirements.txt              # Dependências Python
└── README.md                     # Este arquivo
```