import sys
sys.path.append(r'c:\Users\kauam\OneDrive\Documentos\Área de Trabalho\BCC\2° PERIODO\ALGORITMO2\Clinica sistema')
from flask import Flask, render_template
from CONTROLLER.dados import carregar_arvore_indices, carregar_dados_json
from MODEL.gerador_de_cod import GeradorCodigo

app = Flask(__name__)
app.secret_key = '123456789'

gerador_cidade = GeradorCodigo('cidade')
gerador_paciente = GeradorCodigo('paciente')
gerador_especialidade = GeradorCodigo('especialidade')
gerador_medico = GeradorCodigo('medico')
gerador_exame = GeradorCodigo('exame')
gerador_consulta = GeradorCodigo('consulta')
gerador_diaria = GeradorCodigo('diaria')

cidades = carregar_dados_json("data/dados_cidades.json")
pacientes = carregar_dados_json("data/dados_paciente.json")
especialidades = carregar_dados_json("data/dados_especialidade.json")
medicos = carregar_dados_json("data/dados_medico.json")
exames = carregar_dados_json("data/dados_exame.json")
consultas = carregar_dados_json("data/dados_consulta.json")
diarias = carregar_dados_json("data/dados_diaria.json")

arvore_cidade = carregar_arvore_indices("data/dados_cidades.json")
arvore_paciente = carregar_arvore_indices("data/dados_paciente.json")
arvore_especialidade = carregar_arvore_indices("data/dados_especialidade.json")
arvore_medico = carregar_arvore_indices("data/dados_medico.json")
arvore_exame = carregar_arvore_indices("data/dados_exame.json")
arvore_consulta = carregar_arvore_indices("data/dados_consulta.json")
arvore_diaria = carregar_arvore_indices("data/dados_diaria.json")

from routes.cidade import cidades_bp 
from routes.paciente import pacientes_bp
from routes.especialidade import especialidades_bp
from routes.medico import medicos_bp
from routes.exame import exames_bp
from routes.consulta import consultas_bp
from routes.diaria import diarias_bp

from routes.exaustiva.cidade_leitura import relatorios_cidade_bp
from routes.exaustiva.consulta_leitura import relatorios_consulta_bp
from routes.exaustiva.especialidade_leitura import relatorios_especialidade_bp
from routes.exaustiva.exame_leitura import relatorios_exame_bp
from routes.exaustiva.medico_leitura import relatorios_medico_bp
from routes.exaustiva.paciente_leitura import relatorios_paciente_bp
from routes.exaustiva.diaria_leitura import relatorios_diaria_bp

from routes.faturamentos.diario import faturamento_diario_bp
from routes.faturamentos.medico_fat import faturamento_medico_bp
from routes.faturamentos.especialidade_fat import faturamento_especialidade_bp
from routes.faturamentos.entre import faturamento_entre_bp

app.register_blueprint(cidades_bp)
app.register_blueprint(pacientes_bp)
app.register_blueprint(especialidades_bp)
app.register_blueprint(medicos_bp)
app.register_blueprint(exames_bp)
app.register_blueprint(consultas_bp)
app.register_blueprint(diarias_bp)

app.register_blueprint(relatorios_cidade_bp)
app.register_blueprint(relatorios_consulta_bp)
app.register_blueprint(relatorios_especialidade_bp)
app.register_blueprint(relatorios_exame_bp)
app.register_blueprint(relatorios_medico_bp)
app.register_blueprint(relatorios_paciente_bp)
app.register_blueprint(relatorios_diaria_bp)

app.register_blueprint(faturamento_diario_bp)
app.register_blueprint(faturamento_medico_bp)
app.register_blueprint(faturamento_especialidade_bp)
app.register_blueprint(faturamento_entre_bp)


@app.route("/")
def menu():
    return render_template("menu.html")

if __name__ == "__main__":
    app.run(debug=True)
