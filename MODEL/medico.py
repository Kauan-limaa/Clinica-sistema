from MODEL.gerador_de_cod import GeradorCodigo

gerador_medico = GeradorCodigo('medico')  

class Medico:
    def __init__(self, nome_medico, endereco, telefone, cidade, especialidade, codigo=None):
        if codigo is None:
            self.codigo = gerador_medico.proximo()
        else:
            self.codigo = codigo
        self.nome_medico = nome_medico
        self.endereco = endereco
        self.telefone = telefone
        self.cidade = cidade
        self.especialidade = especialidade