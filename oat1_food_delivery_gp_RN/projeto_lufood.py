pedidos_ativos = []
pedidos_finalizados = []
todos_os_pedidos = []
itens = []
# gerador de códigos (incrementar)
sequencia_cod = 1
sequencia_cod_pedido = 1

def cadastrar_item():
    nome = input("Nome do item: ")
    descricao = input("Descrição do item: ")
    preco = None
    quantidade_estoque = None

    # Tratar preco e quantidade para ser float e int
    while type(preco) != float:
        try:
            preco = float(input("Preço do item: "))
        except:
            print('\n-----Insira um número válido!-----\n')
    
    while type(quantidade_estoque) != int:
        try:
            quantidade_estoque = int(input("Quantidade em estoque: "))
        except:
            print('\n-----Insira um número válido!-----\n')

    global sequencia_cod

    produto = [nome, sequencia_cod, preco, descricao, quantidade_estoque]

    itens.append(produto) # adiciona o produto na lista de itens (final)
    sequencia_cod += 1 # incrementa +1 na variável global 'sequencia_cod'
    print(f"Novo item: {produto[0]}. Cadastrado com sucesso!")
    return produto

def modificar_itens():
    # novamente verifica se há itens cadastrados, se não houver, retorna essa mensagem mensagem e sai da função
    if len(itens) == 0:
        print("Sem dados de cadastro no item.")
        return
    # mostra todos os itens cadastrados e que podem sofrer modificção
    print("Itens cadastrados:") # for (para) cada item na lista de itens (in itens) buscar as informações abaixo
    for item in itens:
        print(f"Código: {item[1]}, Nome: {item[0]}, Preço: {item[2]}, Descrição: {item[3]}, Quantidade em estoque: {item[4]}")
    # pede para o usuário digitar o código do item que deseja modificar e logo depois percorre a lista de itens buscando o código digitado; SE ENCONTRAR, entra no bloco if
    codigo = input("Digite o código do item que deseja modificar: ")
    for item in itens:
        if str(item[1]) == codigo:
            print(f"Modificando item: {item[0]}")
            novo_nome = input(f"Novo nome (Nome atual: '{item[0]}'): ")
            novo_preco = input(f"Novo preço (Valor atual: '{item[2]}'): ")
            nova_descricao = input(f"Nova descrição (Descrição atual: '{item[3]}'): ")
            nova_quantidade = input(f"Nova quantidade em estoque (Atual: '{item[4]}'): ")
            # se o usuário não digitar nada, mantém o valor atual.. se digitar altera no dicionário (dados primeiro são convertidos para o tipo correto e depois atribuídos)
            if novo_nome:
                item[0] = novo_nome
            if novo_preco:
                item[2] = float(novo_preco)
            if nova_descricao:
                item[3] = nova_descricao
                # para a quantidade em estoque, tenta converter o valor para inteiro, se não conseguir (ValueError) mostra uma mensagem de erro e mantém o valor atual
            if nova_quantidade:
                try:
                    item[4] = int(nova_quantidade)
                except ValueError:
                    print("Quantidade inválida. Valor não alterado.")

            print(f"Item {item[1]} atualizado com sucesso!")
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
        print(f"Código: {item[1]}, Nome: {item[0]}, Preço: {item[2]}, Descrição: {item[3]}, Quantidade em estoque: {item[4]}")

def criar_pedido():
    # verifica a existência de itens cadastrados; pedidos não podem ser feitos sem itens
    if len(itens) == 0:
        print("Itens não cadastrados.")
        return

    cupom = ''
    status = 'AGUARDANDO APROVACAO'
    pedido_itens = []
    valor_total = 0.0 # Começa em 0 para somar
    
    global sequencia_cod_pedido
    pedido = [sequencia_cod_pedido]
    
    print("\nItens disponíveis:")
    for item in itens:
        print(f"Código: {item[1]}, Nome: {item[0]}, Preço: R$ {item[2]}")

    # loop para adicionar itens ao pedido
    while True:
        comprar = []
        quantidade = None
        codigo = input("Digite o código do item desejado. Para finalizar, digite 'fim'. ")
        if codigo.lower() == "fim":
            break

        encontrado = False
        for item in itens:
            if str(item[1]) == codigo:
                while type(quantidade) != int:
                    try:
                        quantidade = int(input("Quantidade: "))
                    except:
                        print('\n-----Insira um número válido!-----\n')

                if quantidade > 0 and quantidade <= item[4]:
                    # --- INÍCIO DAS CORREÇÕES ---
                    
                    subtotal_item = item[2] * quantidade.
                    valor_total += subtotal_item           
                    
                    comprar.append(codigo)
                    comprar.append(item[0])
                    comprar.append(quantidade)
                    comprar.append(subtotal_item)         
                    
                    # --- FIM DAS CORREÇÕES ---
                    
                    pedido_itens.append(comprar)
                    item[4] -= quantidade  # reduz o estoque
                    print(f"{quantidade} unidades de {item[0]} adicionado(s) ao pedido.")
                elif quantidade <= 0:
                    print("A quantidade deve ser maior que zero.")
                else:
                    print(f"Estoque insuficiente para '{item[0]}'. Apenas {item[4]} disponível(is).")
                
                encontrado = True
                break
        
        if not encontrado:
            print("Código não encontrado. Tente novamente.")

    # pedido não pode ser vazio
    if len(pedido_itens) == 0:
        print("Pedido cancelado pois nenhum item foi adicionado.")
        return

    # Colocar as compras do cliente no pedido
    pedido.append(pedido_itens)

    # Tratamento do cupom;
    valor_com_desconto = valor_total # Inicia com o valor total
    while True:
        cupom = input("CUPOM (se não tiver, deixe em branco): ")
        if cupom == "DESCONTO10":
            valor_com_desconto = valor_total * 0.9  # aplica 10% de desconto
            print("Cupom aplicado: 10% de desconto.")
            break
        elif cupom == "DESCONTO20":
            valor_com_desconto = valor_total * 0.8  # aplica 20% de desconto
            print("Cupom aplicado: 20% de desconto.")
            break
        elif cupom == '':
            break
        else:
            print("Cupom inválido ou não inserido.")

    # Valor Total
    pedido.append(valor_com_desconto)

    # Cupom
    pedido.append(cupom)

    # status
    pedido.append(status)

    pedidos_ativos.append(pedido)
    todos_os_pedidos.append(pedido)
    sequencia_cod_pedido += 1
    print(f"\nPedido #{pedido[0]:02d} criado com sucesso!")
    print(f"Status: {pedido[4]}")
    print(f"Valor total: R$ {pedido[2]:.2f}")

def imprimir_detalhes_pedido(pedido):
    """Função auxiliar para imprimir um único pedido de forma formatada."""
    print("\n-----------------------------------------")
    print(f"Pedido Código: #{pedido[0]:02d}")
    print(f"Status: {pedido[4]}")
    print("Itens:")
    
    # Itera sobre a lista de itens dentro do pedido
    for item_comprado in pedido[1]:
        # item_comprado = ['código', 'nome', quantidade, subtotal]
        codigo_prod = item_comprado[0]
        nome_prod = item_comprado[1]
        quantidade = item_comprado[2]
        subtotal = item_comprado[3]
        print(f"  - {quantidade}x {nome_prod} (Cód: {codigo_prod}) - Subtotal: R$ {subtotal:.2f}")

    if pedido[3]: # Se houver um cupom
        print(f"Cupom Aplicado: {pedido[3]}")
        
    print(f"Valor Total: R$ {pedido[2]:.2f}")
    print("-----------------------------------------")

def consultar_pedido():
    if not todos_os_pedidos:
        print("\n--- Não há pedidos registrados. ---")
        return

    # Passo 1: Imprimir todos os pedidos de forma formatada
    print("\n======== Histórico de Todos os Pedidos ========")
    for pedido in todos_os_pedidos:
        imprimir_detalhes_pedido(pedido)


    # Passo 2: Oferecer opções para filtrar por status
    while True:
        print("\nFiltrar pedidos por Status:\n"
              "(1) AGUARDANDO APROVACAO\n"
              "(2) ACEITO\n"
              "(3) FAZENDO\n"
              "(4) FEITO\n"
              "(5) ESPERANDO ENTREGADOR\n"
              "(6) SAIU PARA ENTREGA\n"
              "(7) ENTREGUE\n"
              "(8) CANCELADO\n"
              "(9) REJEITADO\n"
              "(0) VOLTAR AO MENU PRINCIPAL")

        sub_opcao = input("Escolha uma opção de filtro: ")
        status_desejado = None

        if sub_opcao == "0":
            print("Voltando ao menu principal...")
            return
        elif sub_opcao == "1":
            status_desejado = "AGUARDANDO APROVACAO"
        elif sub_opcao == "2":
            status_desejado = "ACEITO"
        elif sub_opcao == "3":
            status_desejado = "FAZENDO"
        elif sub_opcao == "4":
            status_desejado = "FEITO"
        elif sub_opcao == "5":
            status_desejado = "ESPERANDO ENTREGADOR"
        elif sub_opcao == "6":
            status_desejado = "SAIU PARA ENTREGA"
        elif sub_opcao == "7":
            status_desejado = "ENTREGUE"
        elif sub_opcao == "8":
            status_desejado = "CANCELADO"
        elif sub_opcao == "9":
            status_desejado = "REJEITADO"
        else:
            print("Opção de status inválida.")
            continue

        if status_desejado:
            print(f"\n--- Pedidos com status: {status_desejado} ---")
            encontrou_pedido = False
            for pedido in todos_os_pedidos:
                if pedido[4] == status_desejado:
                    imprimir_detalhes_pedido(pedido)
                    encontrou_pedido = True
            
            if not encontrou_pedido:
                print(f"\nNenhum pedido encontrado com o status '{status_desejado}'.")

def mostrar_pedidos_por_status(status_desejado, flag=0):
    encontrou_lista = False

    for pedido in pedidos_ativos:
        if pedido[4] == status_desejado:
            print(f"  - ID: {pedido[0]}, Valor: R$ {pedido[2]}")
            encontrou_lista = True
            
        
    if not encontrou_lista and flag != 0:
        print("\n---- Nenhum pedido encontrado com este status ----\n")
    
    return encontrou_lista

def gerenciar_status_pedido():
    while True:
        print("\n--- Gerenciador de Status de Pedidos ---")
        print("(1) Processar Novo Pedido (Aceitar/Rejeitar)")
        print("(2) Iniciar Preparo do Pedido")
        print("(3) Finalizar Preparo do Pedido")
        print("(4) Informar que Aguarda Entregador")
        print("(5) Informar Saída para Entrega")
        print("(6) Finalizar Pedido como ENTREGUE")
        print("(7) Cancelar Pedido")
        print("(0) Voltar ao Menu Principal")
        
        sub_opcao = input("Escolha uma opção: ")

        if sub_opcao == "0":
            print("Voltando ao menu principal")
            return

        # Para cada opção, mostramos a lista de pedidos relevantes primeiro
        if sub_opcao == "1":
            pedidos_existem = mostrar_pedidos_por_status('AGUARDANDO APROVACAO')
            if not pedidos_existem:
                print("\n---- Nenhum pedido aguardando aprovação. ----")
                continue
        elif sub_opcao == "2":
            pedidos_existem = mostrar_pedidos_por_status("ACEITO")
            if not pedidos_existem:
                print("\n---- Nenhum pedido aceito para iniciar o preparo. ----")
                continue
        elif sub_opcao == "3":
            pedidos_existem = mostrar_pedidos_por_status("FAZENDO")
            if not pedidos_existem:
                print("\n---- Nenhum pedido em preparação. ----")
                continue
        elif sub_opcao == "4":
            pedidos_existem = mostrar_pedidos_por_status("FEITO")
            if not pedidos_existem:
                print("\n---- Nenhum pedido feito aguardando entregador. ----")
                continue
        elif sub_opcao == "5":
            pedidos_existem = mostrar_pedidos_por_status("ESPERANDO ENTREGADOR")
            if not pedidos_existem:
                print("\n---- Nenhum pedido esperando entregador. ----")
                continue
        elif sub_opcao == "6":
            pedidos_existem = mostrar_pedidos_por_status("SAIU PARA ENTREGA")
            if not pedidos_existem:
                print("\n---- Nenhum pedido saiu para entrega. ----")
                continue
        elif sub_opcao == "7":
            print("\nPedidos que podem ser cancelados:")
            pedidos_pendentes = mostrar_pedidos_por_status("AGUARDANDO APROVACAO")
            pedidos_aceitos = mostrar_pedidos_por_status("ACEITO")
            if not pedidos_pendentes and not pedidos_aceitos:
                print("---- Nenhum pedido disponível para cancelamento. ----")
                continue
        else:
            print("Opção inválida. Tente novamente.")
            continue

        codigo_pedido = input('Insira o id do pedido para alterar (0 para voltar): ')

        if codigo_pedido == '0':
            continue

        pedido_marcado = None
        
        for pedido in pedidos_ativos:
            if str(pedido[0]) == codigo_pedido:
                pedido_marcado = pedido
                break # Encontrou o pedido, para de procurar

        if not pedido_marcado:
            print(f"\nErro: Pedido com ID {codigo_pedido} não encontrado ou não corresponde ao status selecionado.")
            continue # Volta para o menu do gerenciador

        # O código abaixo só é executado se o pedido_marcado foi encontrado com sucesso.
        if sub_opcao == '1':
            if pedido_marcado[4] == 'AGUARDANDO APROVACAO':
                decisao = input("Aceitar (A) ou Rejeitar (R) o pedido? ").upper()
                if decisao == "A":
                    pedido_marcado[4] = "ACEITO"
                    print(f"Pedido #{codigo_pedido} ACEITO. Status atualizado.")
                elif decisao == "R":
                    pedido_marcado[4] = "REJEITADO"
                    pedidos_ativos.remove(pedido_marcado)
                    pedidos_finalizados.append(pedido_marcado)
                    print(f"Pedido #{codigo_pedido} REJEITADO e movido para finalizados.")
                else:
                    print("Opção inválida.")
            else:
                print(f"Erro: O pedido #{codigo_pedido} não está aguardando aprovação.")

        elif sub_opcao == "2":
            if pedido_marcado[4] == "ACEITO":
                pedido_marcado[4] = "FAZENDO"
                print(f"Pedido #{codigo_pedido} agora está sendo FEITO.")
            else:
                print(f"Erro: O pedido #{codigo_pedido} não foi aceito. Status atual: {pedido_marcado[4]}")

        elif sub_opcao == "3":
            if pedido_marcado[4] == "FAZENDO":
                pedido_marcado[4] = "FEITO"
                print(f"Pedido #{codigo_pedido} foi FEITO e está pronto.")
            else:
                print(f"Erro: O pedido #{codigo_pedido} não está em preparação. Status atual: {pedido_marcado[4]}")

        elif sub_opcao == "4":
            if pedido_marcado[4] == "FEITO":
                pedido_marcado[4] = "ESPERANDO ENTREGADOR"
                print(f"Pedido #{codigo_pedido} agora está ESPERANDO ENTREGADOR.")
            else:
                print(f"Erro: O pedido #{codigo_pedido} ainda não foi feito. Status atual: {pedido_marcado[4]}")

        elif sub_opcao == "5":
            if pedido_marcado[4] == "ESPERANDO ENTREGADOR":
                pedido_marcado[4] = "SAIU PARA ENTREGA"
                print(f"Pedido #{codigo_pedido} SAIU PARA ENTREGA.")
            else:
                print(f"Erro: O pedido #{codigo_pedido} não estava aguardando entregador. Status atual: {pedido_marcado[4]}")

        elif sub_opcao == "6":
            if pedido_marcado[4] == "SAIU PARA ENTREGA":
                pedido_marcado[4] = "ENTREGUE"
                pedidos_ativos.remove(pedido_marcado)
                pedidos_finalizados.append(pedido_marcado)
                print(f"Pedido #{codigo_pedido} finalizado como ENTREGUE.")
            else:
                print(f"Erro: O pedido #{codigo_pedido} não havia saído para entrega. Status atual: {pedido_marcado[4]}")
        
        elif sub_opcao == "7":
            if pedido_marcado[4] in ["AGUARDANDO APROVACAO", "ACEITO"]:
                pedido_marcado[4] = "CANCELADO"
                pedidos_ativos.remove(pedido_marcado)
                pedidos_finalizados.append(pedido_marcado)
                print(f"Pedido #{codigo_pedido} CANCELADO.")
            else:
                print(f"Erro: Pedido não pode mais ser cancelado. Status atual: {pedido_marcado[4]}")
while True:

    print("Menu Principal\n"
      "(1) Cadastrar Produtos\n"
      "(2) Atualizar Produtos\n"
      "(3) Consultar Produtos\n"
      "(4) Criar Pedido\n"
      "(5) Processar Pedidos\n"
      "(6) Consultar Pedidos\n"
      "(0) SAIR")


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
        gerenciar_status_pedido()
    elif opcao == "6":
        consultar_pedido()
    elif opcao == "0":
        print("Saindo do programa")
        exit()
    else:  
        print("Opção inválida. Tente novamente.")
