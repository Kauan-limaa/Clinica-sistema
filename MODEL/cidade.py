from MODEL.gerador_de_cod import GeradorCodigo

gerador_cidade = GeradorCodigo('cidade')  

class Cidade:
    def __init__(self, nome_cidade, estado, codigo=None):
        if codigo is None:
            self.codigo = gerador_cidade.proximo()
        else:
            self.codigo = codigo
        self.nome_cidade = nome_cidade
        self.estado = estado
