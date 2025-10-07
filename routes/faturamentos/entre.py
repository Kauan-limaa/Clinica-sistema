from flask import Blueprint, render_template, request
from CONTROLLER.dados import calcular_faturamento_por_periodo 

faturamento_entre_bp = Blueprint('faturamento_entre_bp', __name__, url_prefix='/faturamentos')

@faturamento_entre_bp.route("/periodo")
def faturamento_entre_flask():

    data_digitada_inicio = request.args.get('data_inicio')
    data_digitada_fim = request.args.get('data_fim')

    resultados = None

    if data_digitada_inicio and data_digitada_fim:
        
        resultados = calcular_faturamento_por_periodo(data_digitada_inicio, data_digitada_fim)
        
    return render_template(
        'faturamento/entre.html', 
        
        dados_faturamento=resultados['consultas'] if resultados and 'consultas' in resultados else [],
    
        faturamento_total=resultados['faturamento_total'] if resultados and 'faturamento_total' in resultados else 0.0,
        
        data_digitada_inicio=data_digitada_inicio,
        data_digitada_fim=data_digitada_fim,
    )