from __future__ import annotations


class Producao:
    
    def __init__(self, regra, derivacao) -> None:
        self.regra = regra
        self.derivacao = derivacao
        self.indice_ponto = -1  # Indica que ponto não foi adicionado
        

    def __str__(self) -> str:
        return f"{self.regra} -> {self.derivacao}"


    def __eq__(self, outro: Producao) -> bool:
        if self.regra == outro.regra and self.derivacao == outro.derivacao:
            return True
            
        return False


    def adicionar_ponto(self) -> None:
        self.derivacao = f".{self.derivacao}"
        self.indice_ponto = 0
        
    
    def avancar_ponto(self) -> bool:
        if not self.eh_final():
            x = self.derivacao[self.indice_ponto]
            y = self.derivacao[self.indice_ponto + 1]

            self.derivacao = self.derivacao.replace(f"{x}{y}", f"{y}{x}")
            self.indice_ponto += 1
            return True

        return False
        
    # Verifica se ponto está no final
    def eh_final(self) -> bool:
        if (self.indice_ponto + 1) == len(self.derivacao):
            return True
    
        return False
    
    # Verifica se o proximo do ponto é não-terminal
    def proximo_nao_terminal(self) -> bool:
        if self.indice_ponto + 1 != len(self.derivacao):
            if (self.derivacao[self.indice_ponto + 1]).isupper():
                return True
        
        return False
    
    # Retorna variável seguinte do ponto
    def pegar_proximo(self) -> str:
        if not self.eh_final():
            return self.derivacao[self.indice_ponto + 1]

        return None


    # Verifica se o próximo do ponto é igual ao passado por parâmetro
    def eh_igual_proximo(self, comparacao: str) -> bool:
        if not self.eh_final():
            return (self.derivacao[self.indice_ponto + 1] == comparacao)

        return False
