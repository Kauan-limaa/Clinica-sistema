from flask import Blueprint, render_template
from CONTROLLER.dados import buscar_por_codigo

relatorios_cidade_bp = Blueprint('relatorios_cidade_bp', __name__, url_prefix='/relatorios')

@relatorios_cidade_bp.route("/cidades")
def relatorio_cidades_flask():

    from app import arvore_cidade

    relatorio_cidades = []
    
    nos_arvore = arvore_cidade.percorrer_em_ordem()

    for no in nos_arvore:
        cidade = buscar_por_codigo(arvore_cidade, "data/dados_cidades.json", no['codigo'])
        if cidade:
            relatorio_cidades.append(cidade)
    
    return render_template("relatorios/cidade_relatorio.html", cidades=relatorio_cidades)
