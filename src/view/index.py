from http.server import BaseHTTPRequestHandler
from src.controller.tarefa_controller import TarefaController
from urllib.parse import parse_qs

# Classe é o manual de instruições do nosso servidor
class ServidorWeb(BaseHTTPRequestHandler):
    # Conectamos o Controller (núcleo) da aplicação que sabe mexer nos dados
    controller = TarefaController()

    # O método do_GET é chamado toda vez que você digita um endereço ou clica num link
    def do_GET(self):
        # Rota Principal: Página Inicial
        # self.path -> é uma comparação exata, so funciona se o endereço for exatamente o home (barra)
        if self.path == "/":
            # Avisa para o navegador que deu tudo certo (Código 200)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            # Abre os arquivos de desenho do site (esqueletos HTML)
            with open("src/view/templates/base.html", "r", encoding="utf-8") as f:
                layout = f.read()

            with open("src/view/templates/listar.html", "r", encoding="utf-8") as f:
                conteudo = f.read()

            # Pede ao Controller a lista de todas as tarefas que está no banco
            tarefas = self.controller.listar_tarefas()

            # Transforma a lista de tarefas em linhas de uma tabela HTML
            # Criando linha por linha
            linhas_tabela = ""
            if isinstance(tarefas, list):
                for t in tarefas:
                    # Decide se o botão vai dizer "Check" ou "Desfazer" baseado no status
                    texto_check = "Desfazer" if t[3] == "concluida" else "Check"
                    novo_status_rapido = "pendente" if t[3] == "concluida" else "concluida"
                    cor_badge = "success" if t[3] == "concluida" else "warning"

                    # Monta linha a linha com o ID, Título, Descrição e os botões de ação
                    linhas_tabela += f"""
                    <tr>
                        <td>{t[0]}</td>
                        <td><strong>{t[1]}</strong></td>
                        <td>{t[2]}</td>
                        <td><span class="badge bg-{cor_badge}">{t[3]}</span></td>
                        <td>
                            <a href='/alternar?id={t[0]}&status={novo_status_rapido}' class='btn btn-sm btn-outline-secondary'>{texto_check}</a>
                            <a href='/editar?id={t[0]}' class='btn btn-sm btn-primary'>Editar</a>
                            <a href='/remover?id={t[0]}' class='btn btn-danger btn-sm'>Excluir</a>
                        </td>
                    </tr>
                    """
            else:
                # Se não tiver nada, avisa que a lista está vazia
                linhas_tabela = "<tr><td colspan='5'>Nenhuma tarefa encontrada</td></tr>"

            # Injeta os dados nos HTMLs
            # Troca as etiquetas "{{ }}" dos arquivos HTML pelos dados reais e pela tabela
            pagina_final = layout.replace("{{ conteudo }}", conteudo)
            pagina_final = pagina_final.replace("{{ tabela_tarefas }}", linhas_tabela)

            # Entrega a página pronta para o navegador mostrar para o usuário
            # self.wfile = Write File -> arquivo de escrita, é o canal de saída do servidor para o seu navegador
            # .write -> ato de empurrar o conteúdo por esse canal
            # .encode() -> não envia letras pela e sim bytes(zeros e uns)
            # transforma seu texto num formato que a rede mundial de computadores consegue carregar
            self.wfile.write(pagina_final.encode())

        # Remover Tarefa
        # self.path.startswith -> significa "começa com", necessário, pois endereços de edição ou como exclusão
        # são acompanhados de informações extras como (ex: /editar?id=5)
        elif self.path.startswith("/remove"):
            # Pega o ID que veio no link (ex: /remove?id=5)
            id_remover = self.path.split("=")[1]
            self.controller.remover_tarefa(id_remover)

            # Manda o navegador voltar para a página inicial (Código 303)
            self.send_response(303) # Muda de direção (Código 303)
            self.send_header("Location", "/") # Vá para o endereço '/' (Página Inicial)
            self.end_headers() # Pode ir agora

        # Formulário de Nova Tarefa
        elif self.path == "/novo":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; utf-8")
            self.end_headers()

            with open("src/view/templates/base.html", "r", encoding="utf-8") as f:
                layout = f.read()
            with open("src/view/templates/form.html", "r", encoding="utf-8") as f:
                form = f.read()

            # Prepara o formulário vazio para uma nova tarefa
            form = form.replace("{{ titulo_pagina }}", "Nova Tarefa")
            form = form.replace("{{ id_tarefa }}", "")
            form = form.replace("{{ valor_titulo }}", "")
            form = form.replace("{{ valor_descricao }}", "")
            form = form.replace("{{ select_pendente }}", "selected")
            form = form.replace("{{ select_concluida }}", "")

            pagina_final = layout.replace("{{ conteudo }}", form)

            self.wfile.write(pagina_final.encode())

        # Formulário de Edição
        elif self.path.startswith("/editar"):
            # Descobre qual tarefa queremos editar e busca os dados dela
            id_editar = self.path.split("=")[1]
            tarefa = self.controller.buscar_por_id(id_editar)

            self.send_response(200)
            self.send_header("Content-Type", "text/html; utf-8")
            self.end_headers()

            with open("src/view/templates/base.html", "r", encoding="utf-8") as f:
                layout = f.read()
            with open("src/view/templates/form.html", "r", encoding="utf-8") as f:
                form = f.read()

            # Preenche o formulário com os dados que já existem no banco
            form = form.replace("{{ titulo_pagina }}", "Editar Tarefa")
            form = form.replace("{{ id_tarefa }}", str(tarefa[0]))
            form = form.replace("{{ valor_titulo }}", tarefa[1])
            form = form.replace("{{ valor_descricao }}", tarefa[2])
            form = form.replace("{{ select_pendente }}", "selected" if tarefa[3] == "pendente" else "")
            form = form.replace("{{ select_concluida }}", "selected" if tarefa[3] == "concluida" else "")

            pagina_final = layout.replace("{{ conteudo }}", form)
            self.wfile.write(pagina_final.encode())

        # Botão Rápido de Alternar Status
        elif self.path.startswith("/alternar"):
            # Pega o ID e o novo Status da URL (ex: /alternar?id=1&status=concluida)
            # .split('?')[1] -> corta o endereço no ponto de interrogação
            # a parte [0] é o alternar e a parte [1] é tudo que vem depois (ex: id=1&status=concluida)
            # parse_qs -> pega essa tripa de texto e transforma num dicionário organizado {'id': ['10'], 'status': ['concluida']}
            params = parse_qs(self.path.split('?')[1])

            # params.get('id')[0] -> vai na gaveta 'id' e pega o primeiro valor que encontrar
            id_tarefa = params.get('id')[0]
            novo_status = params.get('status')[0]

            # Chama o atualizar passando apenas o ID e o novo Status
            self.controller.atualizar_tarefa(id_tarefa=id_tarefa, novo_status=novo_status)

            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()



    # O método do_POST é chamado quando você envia um formulário (clica em Salvar)
    def do_POST(self):
        # Verifica qual rota o formulário está chamando
        if self.path == "/salvar":
            # Lê o tamanho da encomenda (dados) que o usuário enviou
            content_length = int(self.headers['Content-Length'])

            # Lê os bytes do corpo da requisição
            # self.rfile -> Read File (Arquivo de leitura), canal por onde os dados que o usuário enviou estão chegando
            # .read(content_length) -> aqui faz a pergunta "Qual o tamanho desse pacote?", se o formulário tiver 100
            # caracteres, ele lê exatamente os 100 para não perder nada nem ler lixo
            # .decode('utf-8') -> na internet os dados são transportados por bytes, o decode faz a tradução de volta
            # para o texto humano, para que você possa ler
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Converte os dados visualizados na requisição em um dicionário
            dados = parse_qs(post_data)

            # Organiza os dados recebidos (usa um valor vazio "" se não vier nada)
            id_tarefa = dados.get('id', [""])[0]
            titulo = dados.get('titulo', [""])[0]
            descricao = dados.get('descricao', [""])[0]
            status = dados.get('status', ["pendente"])[0]

            # Se o ID estiver vazio, o sistema entende que é uma tarefa nova
            if id_tarefa == "":
                # Se não tem ID, cria
                self.controller.criar_tarefa(titulo, descricao)
            else:
                # Se já tiver ID, o sistema atualiza a tarefa que já existe
                self.controller.atualizar_tarefa(
                    id_tarefa=id_tarefa,
                    novo_titulo=titulo,
                    nova_desc=descricao,
                    novo_status=status
                )

            # Redireciona o usuário de volta para a lista atualizada
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
