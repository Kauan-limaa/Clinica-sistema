from flask import Blueprint, render_template
from CONTROLLER.dados import buscar_por_codigo

relatorios_consulta_bp = Blueprint('relatorios_consulta_bp', __name__, url_prefix='/relatorios')

@relatorios_consulta_bp.route("/consultas")
def relatorio_consultas_flask():
    from app import arvore_consulta, arvore_paciente, arvore_medico, arvore_exame

    relatorio_consultas = []
    
    nos_arvore = arvore_consulta.percorrer_em_ordem()

    for no in nos_arvore:
        consulta = buscar_por_codigo(arvore_consulta, "data/dados_consulta.json", no['codigo'])
        if consulta:
    
            paciente = buscar_por_codigo(arvore_paciente, "data/dados_paciente.json", consulta['paciente'])
            medico = buscar_por_codigo(arvore_medico, "data/dados_medico.json", consulta['medico'])
            exame = buscar_por_codigo(arvore_exame, "data/dados_exame.json", consulta['exame'])
            
            consulta['paciente'] = paciente['nome_paciente'] if paciente else 'Não encontrado'
            consulta['medico'] = medico['nome_medico'] if medico else 'Não encontrado'
            consulta['exame'] = exame['descricao_exa'] if exame else 'Não encontrado'
            
            relatorio_consultas.append(consulta)
    
    return render_template("relatorios/consulta_relatorio.html", consultas=relatorio_consultas)
