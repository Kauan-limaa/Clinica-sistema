from MODEL.cidade import Cidade
from MODEL.gerador_de_cod import GeradorCodigo

gerador_paciente = GeradorCodigo('paciente')  

class Paciente:
    def __init__(self, nome_paciente, dt_nascimento, endereco, 
                 telefone, cidade : Cidade, peso, altura, codigo=None):
        if codigo is None:
            self.codigo = gerador_paciente.proximo()
        else:
            self.codigo = codigo
        self.nome_paciente = nome_paciente
        self.dt_nascimento = dt_nascimento
        self.endereco = endereco
        self.telefone = telefone
        self.cidade = cidade
        self.peso = peso
        self.altura = altura