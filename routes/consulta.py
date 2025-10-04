from flask import Blueprint, request, render_template, redirect, url_for, flash
from CONTROLLER.dados import salvar, buscar_por_codigo, excluir_do_json, diminuir, atualizar_ou_criar_diaria
from MODEL.consulta import Consulta
import json

def carregar_diarias():
    try:
        with open("data/dados_diarias.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def obter_contagem_diaria(data, especialidade_codigo):
    diarias = carregar_diarias()
    
    data_sem_traco = data.replace("-", "")
    chave_diaria = f"{data_sem_traco}{especialidade_codigo}"
    
    for diaria in diarias:
        if diaria.get("codigo") == chave_diaria:
            try:
                return int(diaria["quantidade_consultas"])
            except ValueError:
                return 0
                
    return 0

def obter_limite_da_especialidade(arvore_especialidade, especialidade_codigo):

    especialidade_dict = buscar_por_codigo(arvore_especialidade, "data/dados_especialidade.json", especialidade_codigo)
    if especialidade_dict and 'limite_diario' in especialidade_dict:
        try:
            return int(especialidade_dict['limite_diario'])
        except ValueError:
            return 5 
    return 5 

def carregar_todas_consultas():
    try:
        with open("data/dados_consulta.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

consultas_bp = Blueprint('consultas_bp', __name__, url_prefix='/consultas')

@consultas_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_consulta_flask():

    from app import arvore_consulta, consultas, arvore_paciente, arvore_medico, arvore_exame, pacientes, medicos, exames, arvore_especialidade
    
    if request.method == "POST":
        acao = request.form.get("acao")
        
        if acao == "cadastrar":
            paciente_str = request.form["paciente"]
            medico_str = request.form["medico"]
            exame_str = request.form["exame"]
            data = request.form["data"]
            hora = request.form["hora"]

            paciente_dict = buscar_por_codigo(arvore_paciente, "data/dados_paciente.json", int(paciente_str))
            medico_dict = buscar_por_codigo(arvore_medico, "data/dados_medico.json", int(medico_str))
            exame_dict = buscar_por_codigo(arvore_exame, "data/dados_exame.json", int(exame_str))
            
            if isinstance(paciente_dict, dict) and isinstance(medico_dict, dict) and isinstance(exame_dict, dict):
                
                especialidade_codigo = medico_dict.get("especialidade_codigo") 
                
                if not especialidade_codigo:
                    flash("Erro: Médico sem código de especialidade definido.", "error")
                    return redirect(url_for("consultas_bp.cadastrar_consulta_flask"))

                limite_por_especialidade = obter_limite_da_especialidade(arvore_especialidade, especialidade_codigo)
                
                consultas_agendadas = obter_contagem_diaria(data, especialidade_codigo)

                if consultas_agendadas >= limite_por_especialidade:
                    flash(f"Limite diário de consultas já atingido!", "warning")
                    return redirect(url_for("consultas_bp.cadastrar_consulta_flask"))
                
                consulta_obj = Consulta(paciente_dict["codigo"], medico_dict["codigo"], exame_dict["codigo"], data, hora)
                
                dados_para_salvar = {
                    "codigo": consulta_obj.codigo,
                    "paciente": consulta_obj.paciente,
                    "medico": consulta_obj.medico,
                    "exame": consulta_obj.exame,
                    "data": consulta_obj.data,
                    "hora": consulta_obj.hora
                }

                posicao = salvar(dados_para_salvar, "data/dados_consulta.json")
                arvore_consulta.inserir(consulta_obj.codigo, posicao)
                
                consultas.append(dados_para_salvar)
                
                atualizar_ou_criar_diaria(data, especialidade_codigo)

                return redirect(url_for("consultas_bp.cadastrar_consulta_flask"))
            else:
                return redirect(url_for("consultas_bp.cadastrar_consulta_flask"))
            
        elif acao == "excluir":
            
            codigo_str = request.form["codigo"]
            try:
                codigo = int(codigo_str)
                
                consulta_para_excluir = buscar_por_codigo(arvore_consulta, "data/dados_consulta.json", codigo)
                
                if consulta_para_excluir:
                    if excluir_do_json(codigo, "data/dados_consulta.json"):
                        arvore_consulta.excluir(codigo)
                        
                        data_consulta = consulta_para_excluir.get('data')
                        medico_codigo = consulta_para_excluir.get('medico')
                        
                        if data_consulta and medico_codigo:
                            medico_dict = buscar_por_codigo(arvore_medico, "data/dados_medico.json", medico_codigo)
                            especialidade_codigo = medico_dict.get("especialidade_codigo") if medico_dict else None
                            
                            if especialidade_codigo:
                                diminuir(data_consulta, especialidade_codigo)
                        
                        consultas[:] = [c for c in consultas if c.get('codigo') != codigo]

            except ValueError:
                flash("Código inválido para exclusão.", "error")
            except Exception as e:
                flash(f"Ocorreu um erro durante a exclusão: {e}", "error")

            return redirect(url_for("consultas_bp.cadastrar_consulta_flask"))
    
    return render_template("cadastros/cadastro_consulta.html",
                            pacientes=pacientes,
                            medicos=medicos,
                            exames=exames,
                            consultas=consultas)

@consultas_bp.route("/buscar", methods=["GET"])
def buscar():
    
    from app import arvore_consulta, arvore_paciente, arvore_medico, arvore_exame, pacientes, medicos, exames

    codigo = request.args.get('codigo', type=int)
    consulta = None
    
    if codigo:
        consulta = buscar_por_codigo(arvore_consulta, "data/dados_consulta.json", codigo)
        if consulta:
            paciente_dados = buscar_por_codigo(arvore_paciente, "data/dados_paciente.json", consulta['paciente'])
            consulta['paciente_nome'] = paciente_dados['nome_paciente'] if paciente_dados else None

            medico_dados = buscar_por_codigo(arvore_medico, "data/dados_medico.json", consulta['medico'])
            consulta['medico_nome'] = medico_dados['nome_medico'] if medico_dados else None

            exame_dados = buscar_por_codigo(arvore_exame, "data/dados_exame.json", consulta['exame'])
            consulta['exame_descricao'] = exame_dados['descricao_exa'] if exame_dados else None
            consulta['exame_valor'] = exame_dados['valor_exame'] if exame_dados else None
    
    
    return render_template('cadastros/cadastro_consulta.html',
                            consulta=consulta,
                            pacientes=pacientes,
                            medicos=medicos,
                            exames=exames)