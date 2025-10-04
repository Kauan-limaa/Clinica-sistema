from flask import Blueprint, render_template, request
from CONTROLLER.dados import calcular_faturamento_diario 

faturamento_diario_bp = Blueprint('faturamento_diario_bp', __name__, url_prefix='/faturamentos')

@faturamento_diario_bp.route("/diarios")
def faturamento_diario_flask():

    data_digitada = request.args.get('data')

    resultados = None

    if data_digitada:
        
        resultados = calcular_faturamento_diario(data_digitada)
        
    return render_template(
        'faturamento/diarios.html', 
       
        dados_faturamento=resultados['consultas'] if resultados and 'consultas' in resultados else [],
    
        faturamento_total=resultados['faturamento_total'] if resultados and 'faturamento_total' in resultados else 0.0,
      
        data_digitada=data_digitada,
    )