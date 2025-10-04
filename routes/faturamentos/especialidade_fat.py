from flask import Blueprint, render_template, request
from CONTROLLER.dados import calcular_faturamento_especialidade 


faturamento_especialidade_bp = Blueprint('faturamento_especialidade_bp', __name__, url_prefix='/faturamentos')

@faturamento_especialidade_bp.route("/especialidade")
def faturamento_especialidade_flask():

    codigo_digitado = request.args.get('codigo_especialidade')

    resultados = None
    
    if codigo_digitado:
      
        resultados = calcular_faturamento_especialidade(codigo_digitado)
        
    return render_template(
        'faturamento/especialidade.html', 
    
        dados_faturamento=resultados['consultas'] if resultados and 'consultas' in resultados else [],
        faturamento_total=resultados['faturamento_total'] if resultados and 'faturamento_total' in resultados else 0.0,
        codigo_digitado=codigo_digitado,
    )