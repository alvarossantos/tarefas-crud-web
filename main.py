from http.server import HTTPServer
from src.view.index import ServidorWeb

from src.model.tarefa_model import TarefaDAO
from src.controller.tarefa_controller import TarefaController

def rodar_servidor():
    # Configurações Básicas
    # Define onde o site vai ser liga no meu computador
    endereco = '' # Aceita conexões de qualquer lugar da sua rede
    porta = 8080 # A porta que o site vai usar

    # Instanciando a camada de dados (Model)
    dao_banco = TarefaDAO()
    # Instaciando o Controller passando o DAO para ele (Injetando)
    meu_controller = TarefaController(dao=dao_banco)

    # Passamos (Injetamos) o Controller pronto para a nossa View (ServidorWeb)
    ServidorWeb.controller = meu_controller

    # Cria o servidor usando as regras definidas no arquivo index.py
    servidor = HTTPServer((endereco, porta), ServidorWeb)

    print(f"Servidor iniciado em http://localhost:{porta}")
    print("Pressione Ctrl+C para desligar o servidor.")

    try:
        # Mantém o servidor rodando para sempre
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nDesligando o servidor...")
        servidor.server_close()

# Se este arquivo foi executado ele liga o servidor
if __name__ == "__main__":
    rodar_servidor()