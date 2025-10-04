from flask import Blueprint, render_template, request
from CONTROLLER.dados import calcular_faturamento_medico 


faturamento_medico_bp = Blueprint('faturamento_medico_bp', __name__, url_prefix='/faturamentos')

@faturamento_medico_bp.route("/medico")
def faturamento_medico_flask():
    codigo_digitado = request.args.get('codigo_medico')

    resultados = None
    
    if codigo_digitado:
        resultados = calcular_faturamento_medico(codigo_digitado)
        
    return render_template(
        'faturamento/medico.html', 
        
        dados_faturamento=resultados['consultas'] if resultados and 'consultas' in resultados else [],
        faturamento_total=resultados['faturamento_total'] if resultados and 'faturamento_total' in resultados else 0.0,
        codigo_digitado=codigo_digitado,
    )