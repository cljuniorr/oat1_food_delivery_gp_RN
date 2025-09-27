# Sistema de Gerenciamento de Pedidos

# Listas principais
pedidos_ativos = []
pedidos_finalizados = []
todos_os_pedidos = []
itens = []

# Contadores para códigos únicos
proximo_codigo_item = 1
proximo_codigo_pedido = 1

# Filas por status
pedido_aguardando_aprovacao = []
pedido_aceito = []
pedido_fazendo = []
pedido_feito = []
pedido_esperando_entregador = []
pedido_saiu_entrega = []
pedido_entregue = []
pedido_rejeitado = []
pedido_cancelado = []

def cadastrar_item():
    """Cadastra um novo item no sistema."""
    nome = input("Nome do item: ").strip()
    if not nome:
        print("Nome do item não pode estar vazio!")
        return None
    
    descricao = input("Descrição do item: ").strip()
    
    # Validação do preço
    while True:
        try:
            preco = float(input("Preço do item: R$ "))
            if preco < 0:
                print("O preço não pode ser negativo!")
                continue
            break
        except ValueError:
            print("Por favor, insira um valor numérico válido!")
    
    # Validação da quantidade
    while True:
        try:
            quantidade_estoque = int(input("Quantidade em estoque: "))
            if quantidade_estoque < 0:
                print("A quantidade não pode ser negativa!")
                continue
            break
        except ValueError:
            print("Por favor, insira um número inteiro válido!")

    global proximo_codigo_item
    
    # Estrutura: [nome, codigo, preco, descricao, quantidade_estoque]
    produto = [nome, proximo_codigo_item, preco, descricao, quantidade_estoque]
    
    itens.append(produto)
    proximo_codigo_item += 1
    
    print(f"\nItem '{produto[0]}' cadastrado com sucesso!")
    print(f"Código atribuído: {produto[1]}")
    return produto

def modificar_itens():
    """Permite modificar itens já cadastrados."""
    if not itens:
        print("Nenhum item cadastrado no sistema.")
        return
    
    print("\n--- Itens Cadastrados ---")
    for item in itens:
        print(f"[{item[1]}] {item[0]} - R$ {item[2]:.2f} | Estoque: {item[4]} | {item[3]}")
    
    try:
        codigo = int(input("\nDigite o código do item que deseja modificar: "))
    except ValueError:
        print("Código inválido!")
        return
    
    item_encontrado = None
    for item in itens:
        if item[1] == codigo:
            item_encontrado = item
            break
    
    if not item_encontrado:
        print("Item não encontrado!")
        return
    
    print(f"\nModificando: {item_encontrado[0]}")
    
    # Modificar nome
    novo_nome = input(f"Novo nome (atual: '{item_encontrado[0]}'): ").strip()
    if novo_nome:
        item_encontrado[0] = novo_nome
    
    # Modificar preço
    novo_preco = input(f"Novo preço (atual: R$ {item_encontrado[2]:.2f}): ").strip()
    if novo_preco:
        try:
            preco_float = float(novo_preco)
            if preco_float >= 0:
                item_encontrado[2] = preco_float
            else:
                print("Preço não pode ser negativo. Valor mantido.")
        except ValueError:
            print("Preço inválido. Valor mantido.")
    
    # Modificar descrição
    nova_descricao = input(f"Nova descrição (atual: '{item_encontrado[3]}'): ").strip()
    if nova_descricao:
        item_encontrado[3] = nova_descricao
    
    # Modificar quantidade
    nova_quantidade = input(f"Nova quantidade (atual: {item_encontrado[4]}): ").strip()
    if nova_quantidade:
        try:
            quantidade_int = int(nova_quantidade)
            if quantidade_int >= 0:
                item_encontrado[4] = quantidade_int
            else:
                print("Quantidade não pode ser negativa. Valor mantido.")
        except ValueError:
            print("Quantidade inválida. Valor mantido.")

    print(f"\nItem atualizado com sucesso!")

def consultar_itens():
    """Mostra todos os itens cadastrados."""
    if not itens:
        print("Nenhum item cadastrado no sistema.")
        return
    
    print("\n--- Catálogo de Itens ---")
    for item in itens:
        estoque_info = f"Estoque: {item[4]}" if item[4] > 0 else "SEM ESTOQUE"
        print(f"[{item[1]}] {item[0]} - R$ {item[2]:.2f}")
        print(f"    Descrição: {item[3]}")
        print(f"    {estoque_info}")
        print("-" * 40)

def criar_pedido():
    """Cria um novo pedido."""
    if not itens:
        print("Não há itens cadastrados. Cadastre itens antes de criar pedidos.")
        return

    global proximo_codigo_pedido
    
    pedido_itens = []
    valor_total = 0.0
    
    print("\n--- Criar Novo Pedido ---")
    print("Itens disponíveis:")
    
    # Mostrar apenas itens com estoque
    itens_disponiveis = [item for item in itens if item[4] > 0]
    if not itens_disponiveis:
        print("Nenhum item disponível em estoque!")
        return
    
    for item in itens_disponiveis:
        print(f"[{item[1]}] {item[0]} - R$ {item[2]:.2f} (Estoque: {item[4]})")

    # Loop para adicionar itens ao pedido
    while True:
        entrada = input("\nDigite o código do item (ou 'fim' para finalizar): ").strip()
        
        if entrada.lower() == 'fim':
            break
            
        try:
            codigo = int(entrada)
        except ValueError:
            print("Código inválido!")
            continue
        
        # Buscar item pelo código
        item_escolhido = None
        for item in itens:
            if item[1] == codigo:
                item_escolhido = item
                break
        
        if not item_escolhido:
            print("Item não encontrado!")
            continue
            
        if item_escolhido[4] <= 0:
            print(f"Item '{item_escolhido[0]}' está sem estoque!")
            continue
        
        # Pedir quantidade
        while True:
            try:
                quantidade = int(input(f"Quantidade de '{item_escolhido[0]}' (máx: {item_escolhido[4]}): "))
                if quantidade <= 0:
                    print("Quantidade deve ser maior que zero!")
                    continue
                elif quantidade > item_escolhido[4]:
                    print(f"Estoque insuficiente! Máximo disponível: {item_escolhido[4]}")
                    continue
                break
            except ValueError:
                print("Quantidade inválida!")
        
        # Calcular subtotal e adicionar ao pedido
        subtotal = item_escolhido[2] * quantidade
        valor_total += subtotal
        
        # Estrutura do item no pedido: [codigo, nome, quantidade, subtotal]
        item_pedido = [codigo, item_escolhido[0], quantidade, subtotal]
        pedido_itens.append(item_pedido)
        
        # Reduzir estoque
        item_escolhido[4] -= quantidade
        
        print(f"Adicionado: {quantidade}x {item_escolhido[0]} = R$ {subtotal:.2f}")

    if not pedido_itens:
        print("Pedido cancelado - nenhum item foi adicionado.")
        return

    # Aplicar cupom de desconto
    valor_com_desconto = valor_total
    cupom_aplicado = ""
    
    cupom = input("\nCupom de desconto (DESCONTO10, DESCONTO20 ou deixe vazio): ").strip().upper()
    
    if cupom == "DESCONTO10":
        valor_com_desconto = valor_total * 0.9
        cupom_aplicado = cupom
        print("Cupom DESCONTO10 aplicado - 10% de desconto!")
    elif cupom == "DESCONTO20":
        valor_com_desconto = valor_total * 0.8
        cupom_aplicado = cupom
        print("Cupom DESCONTO20 aplicado - 20% de desconto!")
    elif cupom and cupom not in ["DESCONTO10", "DESCONTO20"]:
        print("Cupom inválido - pedido criado sem desconto.")

    # Criar estrutura do pedido: [codigo, itens, valor_final, cupom, status]
    pedido = [
        proximo_codigo_pedido,
        pedido_itens,
        valor_com_desconto,
        cupom_aplicado,
        "AGUARDANDO APROVACAO"
    ]
    
    pedidos_ativos.append(pedido)
    todos_os_pedidos.append(pedido)
    proximo_codigo_pedido += 1
    
    print(f"Pedido #{pedido[0]} criado com sucesso!")
    print(f"Status: {pedido[4]}")
    if valor_total != valor_com_desconto:
        print(f"Valor original: R$ {valor_total:.2f}")
        print(f"Valor com desconto: R$ {valor_com_desconto:.2f}")
    else:
        print(f"Valor total: R$ {valor_com_desconto:.2f}")

def imprimir_pedido(pedido):
    """Imprime os detalhes de um pedido de forma organizada."""
    print(f"\n{'='*50}")
    print(f"PEDIDO #{pedido[0]:03d}")
    print(f"Status: {pedido[4]}")
    print(f"{'='*50}")
    
    print("ITENS:")
    for item in pedido[1]:
        codigo, nome, quantidade, subtotal = item
        print(f"  • {quantidade}x {nome} (Cód: {codigo}) - R$ {subtotal:.2f}")
    
    if pedido[3]:  # Se há cupom aplicado
        print(f"\nCupom aplicado: {pedido[3]}")
    
    print(f"\nVALOR TOTAL: R$ {pedido[2]:.2f}")
    print(f"{'='*50}")

def consultar_pedido():
    """Consulta pedidos com opções de filtro por status."""
    if not todos_os_pedidos:
        print("Nenhum pedido registrado no sistema.")
        return

    while True:
        print("\n--- Consultar Pedidos ---")
        print("(1) Ver todos os pedidos")
        print("(2) Filtrar por status")
        print("(0) Voltar ao menu principal")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "0":
            break
        elif opcao == "1":
            print("\n--- TODOS OS PEDIDOS ---")
            for pedido in todos_os_pedidos:
                imprimir_pedido(pedido)
        elif opcao == "2":
            filtrar_pedidos_por_status()
        else:
            print("Opção inválida!")

def filtrar_pedidos_por_status():
    """Filtra e mostra pedidos por status específico."""
    status_opcoes = {
        "1": "AGUARDANDO APROVACAO",
        "2": "ACEITO", 
        "3": "FAZENDO",
        "4": "FEITO",
        "5": "ESPERANDO ENTREGADOR",
        "6": "SAIU PARA ENTREGA",
        "7": "ENTREGUE",
        "8": "CANCELADO",
        "9": "REJEITADO"
    }
    
    print("\nFiltrar por status:")
    for num, status in status_opcoes.items():
        print(f"({num}) {status}")
    print("(0) Voltar")
    
    escolha = input("Escolha o status: ").strip()
    
    if escolha == "0":
        return
    
    if escolha not in status_opcoes:
        print("Opção inválida!")
        return
    
    status_escolhido = status_opcoes[escolha]
    pedidos_filtrados = [p for p in todos_os_pedidos if p[4] == status_escolhido]
    
    if not pedidos_filtrados:
        print(f"\nNenhum pedido encontrado com status '{status_escolhido}'.")
    else:
        print(f"\n--- PEDIDOS: {status_escolhido} ---")
        for pedido in pedidos_filtrados:
            imprimir_pedido(pedido)

def buscar_proximo_pedido(status):
    """Busca o próximo pedido com o status especificado."""
    for pedido in pedidos_ativos:
        if pedido[4] == status:
            return pedido
    return None

def gerenciar_status_pedido():
    """Interface para gerenciar o fluxo de status dos pedidos."""
    while True:
        print("\n--- Processar Pedidos ---")
        print("O sistema processará sempre o pedido mais antigo de cada etapa.")
        print()
        
        # Mostrar quantos pedidos há em cada status
        status_count = {}
        for pedido in pedidos_ativos:
            status = pedido[4]
            status_count[status] = status_count.get(status, 0) + 1
        
        print("Status atual dos pedidos ativos:")
        for status, count in status_count.items():
            print(f"  • {status}: {count} pedido(s)")
        print()
        
        print("(1) Aprovar/Rejeitar pedidos")
        print("(2) Iniciar preparo")
        print("(3) Finalizar preparo") 
        print("(4) Aguardar entregador")
        print("(5) Enviar para entrega")
        print("(6) Confirmar entrega")
        print("(7) Cancelar pedido")
        print("(0) Voltar ao menu")
        
        opcao = input("Escolha uma ação: ").strip()
        
        if opcao == "0":
            break
        elif opcao == "1":
            processar_aprovacao()
        elif opcao == "2":
            processar_inicio_preparo()
        elif opcao == "3":
            processar_fim_preparo()
        elif opcao == "4":
            processar_aguardar_entregador()
        elif opcao == "5":
            processar_envio_entrega()
        elif opcao == "6":
            processar_confirmacao_entrega()
        elif opcao == "7":
            cancelar_pedido()
        else:
            print("Opção inválida!")

def processar_aprovacao():
    """Processa aprovação ou rejeição de pedidos."""
    pedido = buscar_proximo_pedido("AGUARDANDO APROVACAO")
    if not pedido:
        print("Nenhum pedido aguardando aprovação.")
        return
    
    imprimir_pedido(pedido)
    
    while True:
        decisao = input("Aprovar (A) ou Rejeitar (R)? ").strip().upper()
        if decisao == "A":
            pedido[4] = "ACEITO"
            pedido_aceito.append(pedido)
            print(f"Pedido #{pedido[0]} aprovado!")
            break
        elif decisao == "R":
            pedido[4] = "REJEITADO"
            pedido_rejeitado.append(pedido)
            pedidos_ativos.remove(pedido)
            pedidos_finalizados.append(pedido)
            print(f"Pedido #{pedido[0]} rejeitado!")
            break
        else:
            print("Digite A para aprovar ou R para rejeitar.")

def processar_inicio_preparo():
    """Inicia o preparo de um pedido aceito."""
    pedido = buscar_proximo_pedido("ACEITO")
    if not pedido:
        print("Nenhum pedido aceito para iniciar preparo.")
        return
    
    imprimir_pedido(pedido)
    
    confirmacao = input("Iniciar preparo deste pedido? (S/N): ").strip().upper()
    if confirmacao == "S":
        pedido[4] = "FAZENDO"
        if pedido in pedido_aceito:
            pedido_aceito.remove(pedido)
        pedido_fazendo.append(pedido)
        print(f"Preparo do pedido #{pedido[0]} iniciado!")

def processar_fim_preparo():
    """Finaliza o preparo de um pedido."""
    pedido = buscar_proximo_pedido("FAZENDO")
    if not pedido:
        print("Nenhum pedido em preparo.")
        return
    
    imprimir_pedido(pedido)
    
    confirmacao = input("Finalizar preparo deste pedido? (S/N): ").strip().upper()
    if confirmacao == "S":
        pedido[4] = "FEITO"
        if pedido in pedido_fazendo:
            pedido_fazendo.remove(pedido)
        pedido_feito.append(pedido)
        print(f"Pedido #{pedido[0]} está pronto!")

def processar_aguardar_entregador():
    """Move pedido pronto para aguardar entregador."""
    pedido = buscar_proximo_pedido("FEITO")
    if not pedido:
        print("Nenhum pedido pronto aguardando entregador.")
        return
    
    imprimir_pedido(pedido)
    
    confirmacao = input("Mover para aguardar entregador? (S/N): ").strip().upper()
    if confirmacao == "S":
        pedido[4] = "ESPERANDO ENTREGADOR"
        if pedido in pedido_feito:
            pedido_feito.remove(pedido)
        pedido_esperando_entregador.append(pedido)
        print(f"Pedido #{pedido[0]} aguardando entregador!")

def processar_envio_entrega():
    """Envia pedido para entrega."""
    pedido = buscar_proximo_pedido("ESPERANDO ENTREGADOR")
    if not pedido:
        print("Nenhum pedido aguardando entregador.")
        return
    
    imprimir_pedido(pedido)
    
    confirmacao = input("Enviar para entrega? (S/N): ").strip().upper()
    if confirmacao == "S":
        pedido[4] = "SAIU PARA ENTREGA"
        if pedido in pedido_esperando_entregador:
            pedido_esperando_entregador.remove(pedido)
        pedido_saiu_entrega.append(pedido)
        print(f"Pedido #{pedido[0]} saiu para entrega!")

def processar_confirmacao_entrega():
    """Confirma a entrega de um pedido."""
    pedido = buscar_proximo_pedido("SAIU PARA ENTREGA")
    if not pedido:
        print("Nenhum pedido em rota de entrega.")
        return
    
    imprimir_pedido(pedido)
    
    confirmacao = input("Confirmar entrega? (S/N): ").strip().upper()
    if confirmacao == "S":
        pedido[4] = "ENTREGUE"
        if pedido in pedido_saiu_entrega:
            pedido_saiu_entrega.remove(pedido)
        pedido_entregue.append(pedido)
        pedidos_ativos.remove(pedido)
        pedidos_finalizados.append(pedido)
        print(f"Pedido #{pedido[0]} entregue com sucesso!")

def cancelar_pedido():
    """Cancela um pedido específico."""
    if not pedidos_ativos:
        print("Nenhum pedido ativo para cancelar.")
        return
    
    print("Pedidos ativos:")
    for pedido in pedidos_ativos:
        print(f"  #{pedido[0]} - {pedido[4]} - R$ {pedido[2]:.2f}")
    
    try:
        codigo = int(input("Digite o código do pedido para cancelar: "))
    except ValueError:
        print("Código inválido!")
        return
    
    pedido_encontrado = None
    for pedido in pedidos_ativos:
        if pedido[0] == codigo:
            pedido_encontrado = pedido
            break
    
    if not pedido_encontrado:
        print("Pedido não encontrado!")
        return
    
    # Só permite cancelar pedidos que ainda não saíram para entrega
    if pedido_encontrado[4] in ["SAIU PARA ENTREGA", "ENTREGUE"]:
        print("Este pedido não pode mais ser cancelado.")
        return
    
    # Devolver itens ao estoque
    for item_pedido in pedido_encontrado[1]:
        codigo_item, nome_item, quantidade, _ = item_pedido
        for item in itens:
            if item[1] == codigo_item:
                item[4] += quantidade  # Devolver ao estoque
                break
    
    # Remove das filas específicas
    status_atual = pedido_encontrado[4]
    if status_atual == "AGUARDANDO APROVACAO" and pedido_encontrado in pedido_aguardando_aprovacao:
        pedido_aguardando_aprovacao.remove(pedido_encontrado)
    elif status_atual == "ACEITO" and pedido_encontrado in pedido_aceito:
        pedido_aceito.remove(pedido_encontrado)
    elif status_atual == "FAZENDO" and pedido_encontrado in pedido_fazendo:
        pedido_fazendo.remove(pedido_encontrado)
    elif status_atual == "FEITO" and pedido_encontrado in pedido_feito:
        pedido_feito.remove(pedido_encontrado)
    elif status_atual == "ESPERANDO ENTREGADOR" and pedido_encontrado in pedido_esperando_entregador:
        pedido_esperando_entregador.remove(pedido_encontrado)
    
    pedido_encontrado[4] = "CANCELADO"
    pedido_cancelado.append(pedido_encontrado)
    pedidos_ativos.remove(pedido_encontrado)
    pedidos_finalizados.append(pedido_encontrado)
    
    print(f"Pedido #{pedido_encontrado[0]} cancelado! Itens devolvidos ao estoque.")

def menu_principal():
    """Exibe o menu principal e processa as opções."""
    while True:
        print("\n" + "="*50)
        print("           SISTEMA DE PEDIDOS")
        print("="*50)
        print("(1) Cadastrar Item")
        print("(2) Modificar Item")
        print("(3) Consultar Itens")
        print("(4) Criar Pedido")
        print("(5) Processar Pedidos")
        print("(6) Consultar Pedidos")
        print("(0) Sair")
        print("="*50)
        
        opcao = input("Escolha uma opção: ").strip()
        
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
            print("Obrigado por usar o sistema!")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Iniciar o programa
if __name__ == "__main__":
    menu_principal()