from flask import Blueprint, request, render_template, redirect, url_for
from CONTROLLER.dados import salvar, buscar_por_codigo, excluir_do_json 
from MODEL.especialidade import Especialidade 

especialidades_bp = Blueprint('especialidades_bp', __name__, url_prefix='/especialidades')

@especialidades_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_especialidade_flask():
    from app import especialidades, arvore_especialidade 

    if request.method == "POST":
        acao = request.form.get("acao")
        
        if acao == "cadastrar":
            descEspecialidade = request.form["especialidade"]
            valorConsulta = request.form["valor"]
            limiteDiario = request.form["limite"]

            especialidade = Especialidade(descEspecialidade, valorConsulta, limiteDiario)
            posicao = salvar(especialidade.__dict__, "data/dados_especialidade.json")
            arvore_especialidade.inserir(especialidade.codigo, posicao)

            especialidades.append({"codigo": especialidade.codigo, "descricao_esp": descEspecialidade, "valor_consulta": valorConsulta, "limite_diario" : limiteDiario})

            return redirect(url_for("especialidades_bp.cadastrar_especialidade_flask"))
        
        elif acao == "excluir":
            codigo_str = request.form["codigo"]
            try:
                codigo = int(codigo_str)
                excluir_do_json(codigo, "data/dados_especialidade.json")
                arvore_especialidade.excluir(codigo)
    
            except ValueError:
                print("Código inválido para exclusão.")
            
            return redirect(url_for("especialidades_bp.cadastrar_especialidade_flask"))
    
    return render_template("cadastros/cadastro_especialidade.html", especialidades=especialidades)

@especialidades_bp.route("/buscar", methods=["GET"])
def buscar():
    from app import arvore_especialidade
    codigo = request.args.get('codigo', type=int)
    especialidade = None 
    
    if codigo:
        especialidade = buscar_por_codigo(arvore_especialidade, "data/dados_especialidade.json", codigo)
        
    return render_template('cadastros/cadastro_especialidade.html', especialidade=especialidade)