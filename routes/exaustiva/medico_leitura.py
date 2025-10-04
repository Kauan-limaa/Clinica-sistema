from flask import Blueprint, render_template
from CONTROLLER.dados import buscar_por_codigo

relatorios_medico_bp = Blueprint('relatorios_medico_bp', __name__, url_prefix='/relatorios')

@relatorios_medico_bp.route("/medicos")
def relatorio_medico_flask():
    from app import arvore_medico, arvore_especialidade, arvore_cidade

    relatorio_medicos = []
    
    nos_arvore = arvore_medico.percorrer_em_ordem()

    for no in nos_arvore:
        medico = buscar_por_codigo(arvore_medico, "data/dados_medico.json", no['codigo'])
        if medico:

            cidade = buscar_por_codigo(arvore_cidade, "data/dados_cidades.json", medico['cidade_codigo'])
            especialidade = buscar_por_codigo(arvore_especialidade, "data/dados_especialidade.json", medico['especialidade_codigo'])
            
            medico['cidade'] = cidade['nome_cidade'] if cidade else 'Não encontrado'
            medico['especialidade'] = especialidade['descricao_esp'] if especialidade else 'Não encontrado'
    
            relatorio_medicos.append(medico)
    
    return render_template("relatorios/medico_relatorio.html", medicos=relatorio_medicos)
