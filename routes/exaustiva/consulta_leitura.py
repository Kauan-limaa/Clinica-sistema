from flask import Blueprint, render_template
from CONTROLLER.dados import buscar_por_codigo

relatorios_consulta_bp = Blueprint('relatorios_consulta_bp', __name__, url_prefix='/relatorios')

@relatorios_consulta_bp.route("/consultas")
def relatorio_consultas_flask():
    from app import arvore_consulta, arvore_paciente, arvore_medico, arvore_exame

    relatorio_consultas = []
    
    nos_arvore = arvore_consulta.percorrer_em_ordem()

    contador = 0
    exame_valor = 0
    valor_total = 0

    for no in nos_arvore:
        consulta = buscar_por_codigo(arvore_consulta, "data/dados_consulta.json", no['codigo'])
        if consulta:
    
            paciente = buscar_por_codigo(arvore_paciente, "data/dados_paciente.json", consulta['paciente'])
            medico = buscar_por_codigo(arvore_medico, "data/dados_medico.json", consulta['medico'])
            exame = buscar_por_codigo(arvore_exame, "data/dados_exame.json", consulta['exame'])
            
            consulta['paciente'] = paciente['nome_paciente'] if paciente else 'Não encontrado'
            consulta['medico'] = medico['nome_medico'] if medico else 'Não encontrado'
            consulta['exame'] = exame['descricao_exa'] if exame else 'Não encontrado'
            consulta['valor'] = exame['valor_exame'] if exame else 'Não encontrado'

            exame_valor = exame.get('valor_exame', '0,00').replace('.', '').replace(',', '.')
            exame_valor = float(exame_valor)

            valor_total = valor_total + exame_valor

            
            relatorio_consultas.append(consulta)
            contador = contador + 1
    
    return render_template("relatorios/consulta_relatorio.html", consultas=relatorio_consultas, contador = contador, valor_total = valor_total)
