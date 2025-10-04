from flask import Blueprint, render_template
from CONTROLLER.dados import buscar_por_codigo

relatorios_especialidade_bp = Blueprint('relatorios_especialidade_bp', __name__, url_prefix='/relatorios')

@relatorios_especialidade_bp.route("/especialidade")
def relatorio_especialidade_flask():

    from app import arvore_especialidade

    relatorio_especialidade = []
    
    nos_arvore = arvore_especialidade.percorrer_em_ordem()

    for no in nos_arvore:
        especialidade = buscar_por_codigo(arvore_especialidade, "data/dados_especialidade.json", no['codigo'])
        if especialidade:
            relatorio_especialidade.append(especialidade)
    
    return render_template("relatorios/especialidade_relatorio.html", especialidades=relatorio_especialidade)
