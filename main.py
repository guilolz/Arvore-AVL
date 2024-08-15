class NoAVL:
    def __init__(self, chave):
        self.esquerda = None
        self.direita = None
        self.valor = chave
        self.altura = 1

class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def _altura(self, no):
        if no is None:
            return 0
        return no.altura

    def _fator_balanceamento(self, no):
        if no is None:
            return 0
        return self._altura(no.esquerda) - self._altura(no.direita)

    def _rotacao_direita(self, y):
        x = y.esquerda
        T2 = x.direita
        x.direita = y
        y.esquerda = T2
        y.altura = max(self._altura(y.esquerda), self._altura(y.direita)) + 1
        x.altura = max(self._altura(x.esquerda), self._altura(x.direita)) + 1
        return x

    def _rotacao_esquerda(self, x):
        y = x.direita
        T2 = y.esquerda
        y.esquerda = x
        x.direita = T2
        x.altura = max(self._altura(x.esquerda), self._altura(x.direita)) + 1
        y.altura = max(self._altura(y.esquerda), self._altura(y.direita)) + 1
        return y

    def inserir(self, chave):
        if not self.raiz:
            self.raiz = NoAVL(chave)
        else:
            self.raiz = self._inserir_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, no, chave):
        if no is None:
            return NoAVL(chave)

        if chave < no.valor:
            no.esquerda = self._inserir_recursivo(no.esquerda, chave)
        else:
            no.direita = self._inserir_recursivo(no.direita, chave)

        no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))

        balanceamento = self._fator_balanceamento(no)

        if balanceamento > 1 and chave < no.esquerda.valor:
            return self._rotacao_direita(no)

        if balanceamento < -1 and chave > no.direita.valor:
            return self._rotacao_esquerda(no)

        if balanceamento > 1 and chave > no.esquerda.valor:
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)

        if balanceamento < -1 and chave < no.direita.valor:
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)

        return no

    def remover(self, chave):
        if not self.raiz:
            return
        self.raiz = self._remover_recursivo(self.raiz, chave)

    def _remover_recursivo(self, no, chave):
        if no is None:
            return no

        if chave < no.valor:
            no.esquerda = self._remover_recursivo(no.esquerda, chave)
        elif chave > no.valor:
            no.direita = self._remover_recursivo(no.direita, chave)
        else:
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda

            temp = self._no_valor_minimo(no.direita)
            no.valor = temp.valor
            no.direita = self._remover_recursivo(no.direita, temp.valor)

        if no is None:
            return no

        no.altura = max(self._altura(no.esquerda), self._altura(no.direita)) + 1
        balanceamento = self._fator_balanceamento(no)

        if balanceamento > 1 and self._fator_balanceamento(no.esquerda) >= 0:
            return self._rotacao_direita(no)

        if balanceamento > 1 and self._fator_balanceamento(no.esquerda) < 0:
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)

        if balanceamento < -1 and self._fator_balanceamento(no.direita) <= 0:
            return self._rotacao_esquerda(no)

        if balanceamento < -1 and self._fator_balanceamento(no.direita) > 0:
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)

        return no

    def _no_valor_minimo(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def exibir(self, no=None, prefixo="", eh_esquerda=True):
        if self.raiz is None:
            print("Árvore está vazia")
            return
        
        if no is None:
            no = self.raiz

        if no.direita is not None:
            novo_prefixo = prefixo + ("│   " if eh_esquerda else "    ")
            self.exibir(no.direita, novo_prefixo, False)

        print(prefixo + ("└── " if eh_esquerda else "┌── ") + str(no.valor))

        if no.esquerda is not None:
            novo_prefixo = prefixo + ("    " if eh_esquerda else "│   ")
            self.exibir(no.esquerda, novo_prefixo, True)

    def salvar_em_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'w') as arquivo:
            self._salvar_recursivo(self.raiz, arquivo)

    def _salvar_recursivo(self, no, arquivo):
        if no is None:
            arquivo.write("#\n")  # Indicador de nó nulo
            return
        arquivo.write(str(no.valor) + '\n')
        self._salvar_recursivo(no.esquerda, arquivo)
        self._salvar_recursivo(no.direita, arquivo)

    def carregar_de_arquivo(self, nome_arquivo):
        with open(nome_arquivo, 'r') as arquivo:
            linhas = iter(arquivo.readlines())
            self.raiz = self._carregar_recursivo(linhas)

    def _carregar_recursivo(self, linhas):
        try:
            valor = next(linhas).strip()
            if valor == "#":
                return None
            no = NoAVL(int(valor))
            no.esquerda = self._carregar_recursivo(linhas)
            no.direita = self._carregar_recursivo(linhas)
            no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))
            return no
        except StopIteration:
            return None

if __name__ == "__main__":
    arvore = ArvoreAVL()

    while True:
        try:
            opcao = int(input("\nEscolha uma opção: \n" +
                              "[1] - Inserir apenas um número\n" +
                              "[2] - Remover apenas um número\n" +
                              "[3] - Exibir\n" +
                              "[4] - Adicionar vetor inteiro\n" +
                              "[5] - Remover vetor inteiro\n" +
                              "[6] - Salvar árvore em arquivo\n" +
                              "[7] - Carregar árvore de arquivo\n" +
                              "[0] - Sair\n"))
        except ValueError:
            print("\nPor favor, insira um número válido.")
            continue

        if opcao == 0:
            print("\nSaindo do programa.")
            break

        elif opcao == 1:
            try:
                valor = int(input("\nDigite um valor a ser inserido: "))
                arvore.inserir(valor)
                arvore.exibir()
                input("\nPressione <enter> para continuar")
            except ValueError:
                print("\nPor favor, insira um número válido.")

        elif opcao == 2:
            try:
                valor = int(input("\nDigite um valor a ser removido: "))
                arvore.remover(valor)
                arvore.exibir()
                input("\nPressione <enter> para continuar")
            except ValueError:
                print("\nPor favor, insira um número válido.")

        elif opcao == 3:
            arvore.exibir()
            input("\nPressione <enter> para continuar")

        elif opcao == 4:
            while True:
                valor = input("\nDigite um valor a ser inserido (ou 'sair' para voltar ao menu): ")
                if valor.lower() == 'sair':
                    break
                try:
                    valor_int = int(valor)
                    arvore.inserir(valor_int)
                    arvore.exibir()
                except ValueError:
                    print("\nPor favor, insira um número válido.")
            input("\nPressione <enter> para continuar")

        elif opcao == 5:
            while True:
                valor = input("\nDigite um valor a ser removido (ou 'sair' para voltar ao menu): ")
                if valor.lower() == 'sair':
                    break
                try:
                    valor_int = int(valor)
                    arvore.remover(valor_int)
                    arvore.exibir()
                except ValueError:
                    print("\nPor favor, insira um número válido.")
            input("\nPressione <enter> para continuar")

        elif opcao == 6:
            nome_arquivo = input("\nDigite o nome do arquivo para salvar a árvore: ")
            arvore.salvar_em_arquivo(nome_arquivo)
            print(f"\nÁrvore salva no arquivo '{nome_arquivo}'.")
            input("\nPressione <enter> para continuar")

        elif opcao == 7:
            nome_arquivo = input("\nDigite o nome do arquivo para carregar a árvore: ")
            arvore.carregar_de_arquivo(nome_arquivo)
            print(f"\nÁrvore carregada do arquivo '{nome_arquivo}'.")
            arvore.exibir()
            input("\nPressione <enter> para continuar")

        else:
            print("\nOpção inválida. Tente novamente.")
