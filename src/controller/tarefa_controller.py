from src.model.tarefa_model import TarefaDAO

class TarefaController:
    def __init__(self, dao):
        # Quando o Controller é criado, ele cria o seu próprio acesso ao Banco de Dados
        self.dao = dao

    def criar_tarefa(self, titulo, descricao):
        # Verificação de segurança: o título não pode ser vazio ou curto demais
        if not titulo or len(titulo.strip()) <= 3:
            return "Erro: O titulo deve ter mais de 3 caracteres."

        # Pede para o DAO inserir no banco e guarda o ID que o banco gerou
        id_gerado = self.dao.create(titulo, descricao)

        if id_gerado:
            return f"Sucesso: Tarefa#{id_gerado} criada!"
        return "Erro ao gravar no banco de dados."

    def atualizar_tarefa(self, id_tarefa, novo_titulo=None, nova_desc=None, novo_status=None):
        if novo_titulo is not None and len(novo_titulo.strip()) <= 3:
            return "Erro: O titulo deve ter mais de 3 caracteres."

        # Primeiro, buscamos os dados atuais da tarefa e armazena na variável
        tarefa_atual = self.dao.get_by_id(id_tarefa)

        # Se a busca não retorna nada, o ID não existe
        if not id_tarefa:
            return "Erro: Tarefa não encontrada."

        # Lógica da Atualização Inteligente, se o usuário não enviou um dado novo (None)
        # tarefa_atual vem como uma lista/tupla: (id[0], titulo[1], descricao[2], status[3])
        # Se o usuário não digitou algum dado novo, então retornará tarefa_atual[x]
        titulo_final = novo_titulo if novo_titulo is not None else tarefa_atual[1]
        des_final = nova_desc if nova_desc is not None else tarefa_atual[2]
        status_final = novo_status if novo_status is not None else tarefa_atual[3]

        # Enviamos os dados finais (mistura dos antigos e novos) para o banco atualizar
        self.dao.update(id_tarefa, titulo_final, des_final, status_final)
        return True

    def listar_tarefas(self):
        # Pede a lista completa para o banco
        tarefas = self.dao.get_all()

        # Se não retorna nada, não existe
        if not tarefas:
            return "Nenhuma tarefa encontrada!"
        return tarefas

    def remover_tarefa(self, id_tarefa):
        # Manda o banco apagar a tarefa pelo número de identificação (ID)
        self.dao.delete(id_tarefa)
        return f"Tarefa {id_tarefa} removida."

    def buscar_por_id(self, id_tarefa):
        # Busca por uma única tarefa específica para carregar no formulário de edição
        tarefa = self.dao.get_by_id(id_tarefa)

        if not tarefa:
            return "Erro: Tarefa não encontrada"
        return tarefa