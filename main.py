from producao import Producao
from item import Item
from copy import deepcopy


# Recebe um arquivo com uma gramática no formato "S -> Aa | bb" e converte para objeto do tipo "Item"
def ler_gramatica(caminho: str) -> Item:
    formatada = []
    
    with open(caminho, 'r') as f:
        gramatica = f.readlines()
    
    for producao in gramatica:
        regra, derivacoes = producao.split("->")
        
        derivacoes = derivacoes.split("|")
        for i in range(len(derivacoes)):
            producao = Producao(regra.strip(), derivacoes[i].strip())
            
            if producao is None:
                continue
            else:
                formatada.append(producao)
    return Item(None, formatada)


def estender_gramatica(gramatica: Item) -> None:
    primeiro = gramatica.producoes[0]
    gramatica.producoes.insert(0, Producao(primeiro.regra + "'", primeiro.regra))


def construir_item_inicial(gramatica_estendida: Item) -> Item:
    inicial = deepcopy(gramatica_estendida)

    for producao in inicial:
        producao.adicionar_ponto()

    return inicial


def imprimir(lista: list) -> None:
    for valor in lista:
        print("========")
        print(valor)
        print("========\n")


# Faz o cálculo do conjunto fechamento dado uma regra e a gramática estendida e retorna uma lista com as produções geradas
def calcular_fechamento(gramatica_estendida: Item, regra: str) -> list[Producao]:
    item = deepcopy(gramatica_estendida)
    fechamento = []

    for producao in item:
        if regra == producao.regra:
            producao.adicionar_ponto()
            fechamento.append(producao)

    return fechamento


# Retorna uma lista com as produções que contém a transição antecedidas de ponto
def shift(anterior: Item, transicao: str) -> list[Producao]:
    anterior = deepcopy(anterior)
    atual = []

    for producao in anterior:
        if producao.eh_igual_proximo(transicao):
            producao.avancar_ponto()
            atual.append(producao)

    return atual


# Verifica se é necessário fazer operações de fechamento após a operação de shift e retorna os não-terminais para executar os fechamentos
def verificar_fechamentos(producoes: list[Producao]) -> list[str]:
    fechamentos = []

    for i in range(len(producoes)):
        if producoes[i].proximo_nao_terminal():
            fechamentos.append(producoes[i].pegar_proximo())

    return fechamentos


def x(gramatica_estendida: Item, transicao: str, atual: Item) -> Item:
    atual_copia = deepcopy(atual)
    producoes_novo = []

    producoes_novo.extend(shift(atual_copia, transicao))

    simbolos_verificados = []
    while True:
        simbolos = verificar_fechamentos(producoes_novo)
        
        simbolos = set(simbolos)
        simbolos_verificados = set(simbolos_verificados)

        repetidos = list(simbolos_verificados.intersection(simbolos))  # Retorna uma lista com os simbolos repetidos

        simbolos = list(simbolos)
        simbolos_verificados = list(simbolos_verificados)

        for repetido in repetidos:  # Remove todos os repetidos da lista de símbolos
            simbolos = [i for i in simbolos if i != repetido]

        simbolos_verificados.extend(simbolos)

        for simbolo in simbolos:
            producoes_novo.extend(calcular_fechamento(gramatica_estendida, simbolo))

        return Item(atual, producoes_novo)



# Gera um novo item dado uma transição para o novo item, o item atual que está gerando o novo e a gramática estendida para cálculo do fechamento
def gerar_item_lr0(gramatica_estendida: Item, transicao: str, atual: Item) -> Item:
    copia_atual = deepcopy(atual)
    novo_producoes = []

    novo_producoes.extend(shift(copia_atual, transicao))
    
    verificados = []
    sao_iguais = False
    while sao_iguais == False:  # Loop roda até terminar de calcular fechamentos
        simbolos = verificar_fechamentos(novo_producoes)

        if verificados == simbolos:  # Se os verificados forem iguais aos símbolos calculados, para o loop para evitar repetição infinita
            sao_iguais = True
        else:
            verificados.extend(simbolos)

            for simbolo in simbolos:
                novo_producoes.extend(calcular_fechamento(gramatica_estendida, simbolo))

    return Item(atual, novo_producoes)


def eh_item_igual(itens: list[Item], verificar: Item) -> bool:
    for item in itens:
        if item == verificar:
            return True
    return False


if __name__ == "__main__":
    itens = []
    fila = []

    gramatica_estendida = ler_gramatica("exemplos/ex3.in")
    estender_gramatica(gramatica_estendida)

    itens.append(construir_item_inicial(gramatica_estendida))
    fila.append(itens[-1])

    while len(fila) > 0:
        item_atual = fila.pop(0)
        transicoes = item_atual.calcular_transicoes()

        for transicao in transicoes:
            item_novo = x(gramatica_estendida, transicao, item_atual)
            if not eh_item_igual(itens, item_novo):
                itens.append(item_novo)
                fila.append(itens[-1])
        
    imprimir(itens)
    print(len(itens))