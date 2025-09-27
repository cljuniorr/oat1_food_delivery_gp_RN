# 🍔 Sistema de Gerenciamento de Pedidos

## 👥 Equipe
* Breno Matos Bastos
* Bruno Sampaio Silva
* Claudio dos Santos Junior
* Gabriel Gomes Cruz Uzeda
* Herick Marcio Matos Brito
* Levi Falcão de Queiroz

## 📖 Descrição
Este projeto é um sistema completo de gerenciamento de pedidos desenvolvido em **Python**. O sistema simula o funcionamento de um restaurante, permitindo o controle total do menu de itens, criação e processamento de pedidos, e gerenciamento do fluxo operacional através de filas organizadas por status.

O sistema oferece uma interface **interativa em linha de comando** com menu principal intuitivo, proporcionando controle completo sobre todas as operações do estabelecimento.

## ⚙️ Estrutura e Funcionalidades

### 🔹 Gerenciamento de Menu
#### **Cadastrar Item**
* Adiciona novos produtos ao catálogo
* Validação automática de dados (preços positivos, quantidades válidas)
* Geração automática de códigos únicos
* Controle de estoque integrado

#### **Modificar Item**
* Atualização de informações existentes (nome, descrição, preço, estoque)
* Validação de entrada para evitar valores inválidos
* Preservação de dados não alterados

#### **Consultar Itens**
* Exibição formatada de todo o catálogo
* Informações detalhadas incluindo status de estoque
* Interface clara e organizada

**Estrutura de cada item:**
* `código`: identificador único (gerado automaticamente)
* `nome`: nome do produto
* `descrição`: detalhes sobre o item
* `preço`: valor monetário (validado)
* `estoque`: quantidade disponível

### 🔹 Gerenciamento de Pedidos
#### **Criar Pedido**
* Seleção de itens do catálogo disponível
* Validação de quantidades contra estoque
* Sistema de cupons de desconto (DESCONTO10 - 10%, DESCONTO20 - 20%)
* Cálculo automático de subtotais e valor final
* Redução automática do estoque
* Status inicial: **AGUARDANDO APROVACAO**

#### **Processar Pedidos**
* Interface dedicada para gerenciamento do fluxo operacional
* Processamento sequencial (FIFO - First In, First Out)
* Controle individual de cada etapa do processo
* Feedback em tempo real sobre status dos pedidos

#### **Consultar Pedidos**
* Visualização de histórico completo
* Filtros por status específico
* Detalhamento completo de cada pedido
* Interface organizada com separação clara de informações

#### **Cancelar Pedido**
* Cancelamento controlado por regras de negócio
* Devolução automática de itens ao estoque
* Restrições baseadas no status atual
* Rastreamento de pedidos cancelados

### 🔹 Sistema de Filas e Controle de Fluxo
O sistema implementa **9 filas especializadas** para organização total dos pedidos:

* `pedido_aguardando_aprovacao` → Novos pedidos aguardando análise
* `pedido_aceito` → Pedidos aprovados para início de preparo
* `pedido_fazendo` → Pedidos em processo de preparação
* `pedido_feito` → Pedidos prontos aguardando disponibilidade de entregador
* `pedido_esperando_entregador` → Pedidos aguardando designação de entregador
* `pedido_saiu_entrega` → Pedidos em rota de entrega
* `pedido_entregue` → Pedidos finalizados com sucesso
* `pedido_rejeitado` → Pedidos não aprovados
* `pedido_cancelado` → Pedidos cancelados pelo sistema

### 🔹 Fluxo Completo de Status
```
AGUARDANDO APROVACAO → ACEITO → FAZENDO → FEITO → ESPERANDO ENTREGADOR → SAIU PARA ENTREGA → ENTREGUE
                    ↘         ↘         ↘        ↘
                   REJEITADO  CANCELADO  CANCELADO  CANCELADO
```

**Status disponíveis:**
1. **AGUARDANDO APROVACAO** - Pedido criado, aguardando análise
2. **ACEITO** - Pedido aprovado, pronto para iniciar o preparo
3. **FAZENDO** - Pedido em preparação na cozinha
4. **FEITO** - Pedido pronto, aguardando entregador
5. **ESPERANDO ENTREGADOR** - Aguardando disponibilidade de entregador
6. **SAIU PARA ENTREGA** - Pedido em rota de entrega
7. **ENTREGUE** - Pedido finalizado com sucesso
8. **CANCELADO** - Pedido cancelado (apenas nos status iniciais)
9. **REJEITADO** - Pedido não aprovado

### 🔹 Funcionalidades Avançadas
#### **Sistema de Validação**
* Validação de entrada para todos os campos numéricos
* Prevenção de valores negativos
* Verificação de disponibilidade de estoque
* Tratamento de erros robusto

#### **Gestão de Estoque**
* Redução automática no momento da criação do pedido
* Devolução automática em caso de cancelamento
* Verificação de disponibilidade antes da venda
* Controle de itens sem estoque

#### **Sistema de Cupons**
* DESCONTO10: 10% de desconto no valor total
* DESCONTO20: 20% de desconto no valor total
* Validação automática de cupons
* Aplicação transparente com detalhamento

## 🛠️ Tecnologias Utilizadas
* **Python 3.x** - Linguagem principal
* **Estruturas de dados nativas** - Listas para filas e armazenamento
* **Menu interativo** - Interface de linha de comando
* **Validação de entrada** - Tratamento robusto de dados
* **Sistema FIFO** - Processamento sequencial de pedidos

## 🚀 Como Executar
1. Certifique-se de ter Python 3.x instalado
2. Execute o arquivo principal:
   ```bash
   python sistema_pedidos.py
   ```
3. Use o menu interativo para navegar pelas funcionalidades

## 📋 Menu Principal
```
==================================================
           SISTEMA DE PEDIDOS
==================================================
(1) Cadastrar Item
(2) Modificar Item
(3) Consultar Itens
(4) Criar Pedido
(5) Processar Pedidos
(6) Consultar Pedidos
(0) Sair
==================================================
```

## 🎯 Características Técnicas
* **Arquitetura modular** com funções especializadas
* **Separação de responsabilidades** para cada operação
* **Controle de fluxo** baseado em filas organizadas
* **Validação robusta** de todas as entradas
* **Interface intuitiva** com feedback claro
* **Gerenciamento de estado** completo dos pedidos
* **Sistema de rastreamento** para auditoria e controle
