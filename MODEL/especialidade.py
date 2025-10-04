from MODEL.gerador_de_cod import GeradorCodigo

gerador_especialidade = GeradorCodigo('especialidade')  

class Especialidade:
    def __init__(self, descricao_esp, valor_consulta, limite_diario, codigo=None ):
        if codigo is None:
            self.codigo = gerador_especialidade.proximo()
        else:
            self.codigo = codigo
        self.descricao_esp = descricao_esp
        self.valor_consulta = valor_consulta
        self.limite_diario = limite_diario