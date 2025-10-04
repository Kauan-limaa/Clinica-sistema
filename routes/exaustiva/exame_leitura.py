from flask import Blueprint, render_template
from CONTROLLER.dados import buscar_por_codigo

relatorios_exame_bp = Blueprint('relatorios_exame_bp', __name__, url_prefix='/relatorios')

@relatorios_exame_bp.route("/exames")
def relatorio_exame_flask():
    from app import arvore_exame, arvore_especialidade

    relatorio_exames = []
    
    nos_arvore = arvore_exame.percorrer_em_ordem()

    for no in nos_arvore:
        exame = buscar_por_codigo(arvore_exame, "data/dados_exame.json", no['codigo'])
        if exame:

            especialidade = buscar_por_codigo(arvore_especialidade, "data/dados_especialidade.json", exame['especialidade_codigo'])
            
            exame['especialidade'] = especialidade['descricao_esp'] if especialidade else 'Não encontrado'
    
            relatorio_exames.append(exame)
    
    return render_template("relatorios/exame_relatorio.html", exames=relatorio_exames)
