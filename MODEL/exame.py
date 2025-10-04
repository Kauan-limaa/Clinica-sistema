from MODEL.gerador_de_cod import GeradorCodigo

gerador_exame = GeradorCodigo('exame')  

class Exame:
    def __init__(self, descricao_exa, especialidade, valor_exame, codigo=None ):
        if codigo is None:
            self.codigo = gerador_exame.proximo()
        else:
            self.codigo = codigo
        self.descricao_exa = descricao_exa
        self.especialidade = especialidade
        self.valor_exame = valor_exame