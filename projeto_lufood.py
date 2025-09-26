# Base do projeto
"""
menu de itens
cadastro -> atualização -> consulta
detalhes do itens

"""
# Lista para guardar todos os itens que forem cadastrados.
pedidos_pendentes = []
pedidos_aceitos = []
pedidos_prontos = []
todos_pedidos = []
itens = []
# gerador de códigos
sequencia_cod = 1 # código começando em 1

# CADASTRO DE ITENS
def cadastrar_item():
    # entrada de dados pelo usuário
    nome = input("Nome do item: ")
    preco = float(input("Preço do item: "))
    descricao = input("Descrição do item: ")
    quantidade_estoque = int(input("Quantidade em estoque: "))
    # define 'sequencia_cod' como uma variável global para que possa ser modificada dentro da função
    global sequencia_cod
    # dicionário de dados do produto
    produto = {
        "nome" : nome,
        "codigo" : f"{sequencia_cod:03d}", # define a formatação do código que será inicializado e formata o código com 3 dígitos, preenchendo com zeros à esquerda se necessário (o "3" pode ser mudado para outros valores para comportar maiores quantidades de código; ex: 04d para 4 digitos e etc)
        "preco" : preco,
        "quantidade_estoque" : quantidade_estoque,
        "descricao" : descricao
    }

    itens.append(produto) # adiciona o produto na lista de itens (final)
    sequencia_cod += 1 # incrementa +1 na variável global 'sequencia_cod'
    print(f"Novo item: {produto['nome']}. Cadastrado com sucesso!")
    return produto

def modificar_itens():
    # novamente verifica se há itens cadastrados, se não houver, retorna essa mensagem mensagem e sai da função
    if len(itens) == 0:
        print("Sem dados de cadastro no item.")
        return
    # mostra todos os itens cadastrados e que podem sofrer modificção
    print("Itens cadastrados:") # for (para) cada item na lista de itens (in itens) buscar as informações abaixo
    for item in itens:
        print(f"Código: {item['codigo']}, Nome: {item['nome']}, Preço: {item['preco']}, Descrição: {item['descricao']}, Quantidade em estoque: {item.get('quantidade_estoque', 'N/A')}")
    # pede para o usuário digitar o código do item que deseja modificar e logo depois percorre a lista de itens buscando o código digitado; SE ENCONTRAR, entra no bloco if
    codigo = input("Digite o código do item que deseja modificar: ")
    for item in itens:
        if item['codigo'] == codigo:
            print(f"Modificando item: {item['nome']}")
            novo_nome = input(f"Novo nome (Nome atual: '{item['nome']}'): ")
            novo_preco = input(f"Novo preço (Valor atual: '{item['preco']}'): ")
            nova_descricao = input(f"Nova descrição (Descrição atual: '{item['descricao']}'): ")
            nova_quantidade = input(f"Nova quantidade em estoque (Atual: '{item.get('quantidade_estoque', 'N/A')}'): ")
            # se o usuário não digitar nada, mantém o valor atual.. se digitar altera no dicionário (dados primeiro são convertidos para o tipo correto e depois atribuídos)
            if novo_nome:
                item['nome'] = novo_nome
            if novo_preco:
                item['preco'] = float(novo_preco)
            if nova_descricao:
                item['descricao'] = nova_descricao
                # para a quantidade em estoque, tenta converter o valor para inteiro, se não conseguir (ValueError) mostra uma mensagem de erro e mantém o valor atual
            if nova_quantidade:
                try:
                    item['quantidade_estoque'] = int(nova_quantidade)
                except ValueError:
                    print("Quantidade inválida. Valor não alterado.")

            print(f"Item {item['codigo']} atualizado com sucesso!")
            return

    print("Código não encontrado.")

def consultar_itens():
    # mais uma vez verifica se há ou não itens cadastrados
    if len(itens) == 0:
        print("Sem dados de cadastro no item.")
        return
    # mostra todos os itens cadastrados em caso de retorno positivo
    print("Itens cadastrados:")
    for item in itens:
        print(f"Código: {item['codigo']}, Nome: {item['nome']}, Preço: {item['preco']}, Descrição: {item['descricao']}, Quantidade em estoque: {item.get('quantidade_estoque', 'N/A')}")

def criar_pedido():
    # verifica a existência de itens cadastrados; pedidos não podem ser feitos sem itens
    if len(itens) == 0:
        print("Itens não cadastrados.")
        return

    pedido_itens = []
    valor_total = 0.0

    print("\nItens disponíveis:")
    for item in itens:
        print(f"Código: {item['codigo']}, Nome: {item['nome']}, Preço: R$ {item['preco']}")

    # loop para adicionar itens ao pedido, enquanto não digitar 'fim' ele continua solicitando código.
    while True:
        codigo = input("Digite os códigos dos itens desejados. Para finalizar, digite 'fim'. ")
        if codigo.lower() == "fim":
            break

        encontrado = False
        # percorre a lista buscando o código digitado, e adiciona ao pedido apenas aquilo que existe de fato no estoque.
        for item in itens:
            if item['codigo'] == codigo:
                if item.get('quantidade_estoque', 0) > 0:
                    pedido_itens.append(item)
                    valor_total += item['preco']
                    item['quantidade_estoque'] -= 1  # reduz o estoque
                    print(f"Item '{item['nome']}' adicionado ao pedido.")
                else:
                    print(f"Item '{item['nome']}' acabou. Insira outro código ou finalize.")
                encontrado = True
                break

        if not encontrado:
            print("Código não encontrado. Tente novamente.")

    # pedido não pode ser vazio
    if len(pedido_itens) == 0:
        print("Pedido precisa ter pelo menos um item.")
        return

    # tratamento do cupom; nesse caso temos 2 possibilidades ofertadas fora isso é inválido
    cupom = input("CUPOM (se não tiver, deixe em branco): ")
    if cupom == "DESCONTO10":
        valor_total *= 0.9  # aplica 10% de desconto
        print("Cupom aplicado: 10% de desconto.")
    elif cupom == "DESCONTO20":
        valor_total *= 0.8  # aplica 20% de desconto
        print("Cupom aplicado: 20% de desconto.")
    else:
        print("Cupom inválido ou não inserido.")

    # dicionário de pedido coletado que será adicionado a fila de pendentes
    pedido = {
        "id": len(pedidos_pendentes) + 1,
        "itens": pedido_itens,
        "valor_total": round(valor_total, 2),
        "cupom": cupom,
        "status": "AGUARDANDO APROVACAO"
    }

    pedidos_pendentes.append(pedido)
    print(f"\nPedido #0{pedido['id']} criado com sucesso!")
    print(f"Status: {pedido['status']}")
    print(f"Valor total: R$ {pedido['valor_total']}")

def processar_pedidos():
    # verifica se tem pedidos pendentes para processamento de fila
    if not pedidos_pendentes:
        print("Sem pendências.")
        return
    
    # pega o primeiro pedido da fila - o 0 é o primeiro - (first in, first out) e pergunta se aceita ou rejeita.
    pedido = pedidos_pendentes.pop(0)
    print(f"Processando Pedido #{pedido['id']} - Valor: R$ {pedido['valor_total']}")
    decisao = input("Aceitar pedido (A) ou Rejeitar pedido (R)? ").upper() #deixa resposta em maíusculo
    
    if decisao == "A":
        pedido["status"] = "FAZENDO"
        pedidos_aceitos.append(pedido)
        # o .append adiciona o pedido no final da lista de aceitos
        print("Pedido aceito e movido para preparo.")
    elif decisao == "R":
        pedido["status"] = "REJEITADO"
        print("Pedido rejeitado.")
    else:
        print("Opção inválida. Pedido mantido como pendente.")
        # se a opção for inválida, o pedido volta para o início da fila de pendentes
        pedidos_pendentes.insert(0, pedido)

def finalizar_preparo():
    if not pedidos_aceitos:
        print("Nenhum pedido em preparo.")
        return

    # pega o primeiro pedido da fila de aceitos e finaliza o preparo
    pedido = pedidos_aceitos.pop(0)
    pedido["status"] = "Aguardando retirada do entregador."
    pedidos_prontos.append(pedido)
    print(f"Pedido #{pedido['id']} finalizado e aguardando entregador.")

def atualizar_status():
    id_busca = input("Digite o ID do pedido: ")
    for lista in [pedidos_pendentes, pedidos_aceitos, pedidos_prontos]:
        for pedido in lista:
            if str(pedido["id"]) == id_busca:
                print(f"Status atual: {pedido['status']}")
                novo_status = input("Novo status: ").upper()
                pedido["status"] = novo_status
                print("Status atualizado.")
                return
    print("Pedido não existe.")

def cancelar_pedido():
    id_busca = input("Digite o ID do pedido para cancelar: ")
    for fila in [pedidos_pendentes, pedidos_aceitos]:
        for pedido in fila:
            if str(pedido["id"]) == id_busca:
                if pedido["status"] in ["AGUARDANDO APROVACAO", "FAZENDO"]:
                    pedido["status"] = "CANCELADO"
                    fila.remove(pedido)
                    print("Pedido cancelado!")
                    return
    print("Pedido não pode ser cancelado ou não foi encontrado.")


 # MENU DE ITENS
while True: # loop infinito para o menu de itens

    print("Menu Principal")
    print(f"{'(1) Cadastrar Produtos':<10}")
    print(f"{'(2) Atualizar Produtos':<10}")
    print(f"{'(3) Consultar Produtos':<10}")
    print(f"{'(4) Criar Pedido':<10}")
    print(f"{'(5) Processar Pedidos':<10}")
    print(f"{'(6) Cancelar Pedido':<10}")
    print(f"{'(7) Finalizar Preparação do Pedido':<10}")
    print(f"{'(8) Atualizar Status do Pedido':<10}")
    print(f"{'(0) SAIR':<10}")

    opcao = input("Escolha a opção desejada: ")
    if opcao == "1":
        cadastrar_item()
    elif opcao == "2":
        modificar_itens()
    elif opcao == "3":
        consultar_itens()
    elif opcao == "4":
        criar_pedido()
    elif opcao == "5":
        processar_pedidos()
    elif opcao == "6":
        cancelar_pedido()
    elif opcao == "7":
        finalizar_preparo()
    elif opcao == "8":
        atualizar_status()
    elif opcao == "0":
        print("Saindo do programa...")
        exit() # encerra o programa e o loop do "while"
    else:  
        print("Opção inválida. Tente novamente.")




