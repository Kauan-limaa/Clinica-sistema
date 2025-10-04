from flask import Blueprint, render_template
from CONTROLLER.dados import buscar_por_codigo

relatorios_paciente_bp = Blueprint('relatorios_paciente_bp', __name__, url_prefix='/relatorios')

@relatorios_paciente_bp.route("/pacientes")
def relatorio_paciente_flask():
    from app import arvore_paciente, arvore_cidade

    relatorio_pacientes = []
    
    nos_arvore = arvore_paciente.percorrer_em_ordem()

    for no in nos_arvore:
        paciente = buscar_por_codigo(arvore_paciente, "data/dados_paciente.json", no['codigo'])
        if paciente:

            cidade = buscar_por_codigo(arvore_cidade, "data/dados_cidades.json", paciente['cidade_codigo'])
            
            paciente['cidade'] = cidade['nome_cidade'] if cidade else 'Não encontrado'
    
            relatorio_pacientes.append(paciente)
    
    return render_template("relatorios/paciente_relatorio.html", pacientes=relatorio_pacientes)
