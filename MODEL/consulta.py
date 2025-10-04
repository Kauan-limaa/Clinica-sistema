from MODEL.gerador_de_cod import GeradorCodigo

gerador_consulta = GeradorCodigo('consulta')  

class Consulta:
    def __init__(self, paciente, medico, exame, data, hora, codigo=None ):
        if codigo is None:
            self.codigo = gerador_consulta.proximo()
        else:
            self.codigo = codigo
        self.paciente = paciente
        self.medico = medico
        self.exame = exame
        self.data = data
        self.hora = hora