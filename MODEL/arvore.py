class No:
    def __init__(self, codigo, posicao_json):
        self.codigo = codigo
        self.posicao_json = [posicao_json]
        self.esq = None
        self.dir = None

class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inserir(self, codigo, posicao_json):
        no = No(codigo, posicao_json)
        if self.raiz is None:
            self.raiz = no
        else:
            self._inserir(self.raiz, no)

    def _inserir(self, atual, no):
        if no.codigo == atual.codigo:
            atual.posicao_json.append(no.posicao_json[0])
        elif no.codigo < atual.codigo:
            if atual.esq is None:
                atual.esq = no
            else:
                self._inserir(atual.esq, no)
        else:  
            if atual.dir is None:
                atual.dir = no
            else:
                self._inserir(atual.dir, no)

    def buscar(self, codigo):
        return self._buscar(self.raiz, codigo)

    def _buscar(self, atual, codigo):
        if atual is None:
            return None
        if codigo == atual.codigo:
            return atual.posicao_json
        elif codigo < atual.codigo:
            return self._buscar(atual.esq, codigo)
        else:
            return self._buscar(atual.dir, codigo)

    def _menor_no(self, no_atual):
        atual = no_atual
        while atual.esq is not None:
            atual = atual.esq
        return atual

    def excluir(self, codigo):
        self.raiz = self._excluir_recursivo(self.raiz, codigo)

    def _excluir_recursivo(self, raiz, codigo):
        
        if raiz is None:
            return raiz
    
        if codigo < raiz.codigo:
            raiz.esq = self._excluir_recursivo(raiz.esq, codigo)
        elif codigo > raiz.codigo:
            raiz.dir = self._excluir_recursivo(raiz.dir, codigo)
        else:
            if raiz.esq is None:
                return raiz.dir
            elif raiz.dir is None:
                return raiz.esq
        
            sucessor = self._menor_no(raiz.dir)
            
            raiz.codigo = sucessor.codigo
            raiz.posicao_json = sucessor.posicao_json
            
            raiz.dir = self._excluir_recursivo(raiz.dir, sucessor.codigo)
            
        return raiz
    
    def percorrer_em_ordem(self):
        resultados = []

        def _percorrer_recursivo(no):
            if no:
                _percorrer_recursivo(no.esq)
                resultados.append({"codigo": no.codigo, "posicao_json": no.posicao_json})
                _percorrer_recursivo(no.dir)
        
        _percorrer_recursivo(self.raiz)
        return resultados