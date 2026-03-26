import os
from dotenv import load_dotenv # Biblioteca que carrega dados salvos em um arquivo
import psycopg2 # Tradutor que permite o Python falar com o banco de dados

# Carrega as variáveis dentro de .env
load_dotenv()

# Definição da Tarefa como será estruturada na aplicação
class TarefaModel:
    def __init__(self, titulo, descricao, status, id=None, criado_em=None):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.criado_em = criado_em

# DAO ou Data Access Object (Motor de Acesso aos Dados)
# Classe responsável por tudo que envolve o nosso Banco de Dados
class TarefaDAO:
    # Puxamos as configurações que load_dotenv() carregou
    def __init__(self):
        self.config = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT")
        }

    # Teste simples de conexão com o banco de dados
    def conectar(self):
        try:
            # Tenta abrir a porta do banco
            conn = psycopg2.connect(**self.config)
            print("Conexão com o banco de dados estabelecida com sucesso!")

            # Cursor é como se fosse o ponteiro do mouse no banco
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            versao = cursor.fetchone()
            print(f"Versão do PostgreSQL: {versao[0]}")

            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            print(f"Falha ao conectar ao banco de dados: {e}")

    # Conecta ao banco de dados
    # Abre a conexão, executa o comando SQL e fecha a conexão automaticamente
    def _executar(self, query, params=None, fetch=None):
        try:
            # 'conn' será a variável principal que será conectada ao banco de dados
            conn = psycopg2.connect(**self.config)

            # O cursor é como um ponteiro, ele é quem leva o comando SQL até o banco e traz o resultado
            cursor = conn.cursor()

            # Executa o comando SQL desejado substituindo os %s pelos dados reais (params)
            cursor.execute(query, params)

            # Se for um comando de leitura, o cursor coleta os dados encontrados
            # ele traz ou se não, apenas salva
            resultado = cursor.fetchall() if fetch else None

            # Confirma as alterações no banco
            conn.commit()

            # Fechamos o cursor primeiro depois a conexão ao banco de dados
            cursor.close()
            conn.close()
            return resultado
        except psycopg2.Error as e:
            print(f"Erro: {e}")
            return None

    # Operações do Banco
    def create(self, titulo, descricao):
        query = "INSERT INTO tarefas (titulo, descricao) VALUES (%s, %s) RETURNING id;"
        return self._executar(query, (titulo, descricao), fetch=True)

    def get_by_id(self, id):
        query = "SELECT id, titulo, descricao, status FROM tarefas WHERE id = %s;"
        resultado = self._executar(query, (id,), fetch=True)
        # 'resultado[0] retornará o ID da tarefa, se não nada retornará
        return resultado[0] if resultado else None

    def get_all(self):
        query = "SELECT id, titulo, descricao, status, criado_em FROM tarefas ORDER BY criado_em DESC;"
        return self._executar(query, fetch=True)

    def update(self, id, titulo, descricao, status="pendente"):
        query = "UPDATE tarefas SET titulo = %s, descricao = %s, status = %s WHERE id = %s;"
        return self._executar(query, (titulo, descricao, status, id))

    def delete(self, id):
        query = "DELETE FROM tarefas WHERE id = %s;"
        return self._executar(query, (id,))
