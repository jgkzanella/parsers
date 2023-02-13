from __future__ import annotations
from typing import Iterator
from producao import Producao


class Item:
    def __init__(self, anterior: Item, producoes: list[Producao]) -> None:
        self.anterior: Item = anterior
        self.producoes: list[Producao] = producoes


    def __str__(self) -> str:
        imprimir = ""
        for producao in self.producoes:
            imprimir += producao.__str__() + "\n"

        return imprimir[:len(imprimir)-1]


    def __iter__(self) -> Iterator[Producao]:
        return iter(self.producoes)


    def __eq__(self, outro: Item) -> bool:
        if self.anterior == outro.anterior:
            for i in range(len(self.producoes)):
                if self.producoes[i] != outro.producoes[i]:
                    return False
        
        return True


    # Calcula todas as transições possíveis do item
    def calcular_transicoes(self):
        transicoes = []
        transicao = ""

        for producao in self.__iter__():
            transicao = producao.pegar_proximo()
            if transicao:
                transicoes.append(transicao)

        return list(dict.fromkeys(transicoes))  # Remove duplicados