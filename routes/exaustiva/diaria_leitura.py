from flask import Blueprint, render_template
from CONTROLLER.dados import buscar_por_codigo

relatorios_diaria_bp = Blueprint('relatorios_diaria_bp', __name__, url_prefix='/relatorios')

@relatorios_diaria_bp.route("/diarias")
def relatorio_diarias_flask():
    from app import arvore_diaria, arvore_especialidade

    relatorio_diarias = []
    
    nos_arvore = arvore_diaria.percorrer_em_ordem()

    for no in nos_arvore:
        diaria = buscar_por_codigo(arvore_diaria, "data/dados_diaria.json", no['codigo'])
        if diaria:
    
            especialidade = buscar_por_codigo(arvore_especialidade, "data/dados_especialidade.json", diaria['especialidade_codigo'])
            diaria['especialidade'] = especialidade['descricao_esp'] if especialidade else 'Não encontrado'
            
            relatorio_diarias.append(diaria)
    
    return render_template("relatorios/diaria_relatorio.html", diarias=relatorio_diarias)
