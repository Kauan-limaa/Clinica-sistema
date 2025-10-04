from flask import Blueprint, request, render_template, redirect, url_for
from datetime import datetime
from CONTROLLER.dados import salvar_diaria, buscar_por_codigo, excluir_do_json
from MODEL.diaria import Diaria

diarias_bp = Blueprint('diarias_bp', __name__, url_prefix='/diarias')

@diarias_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_diaria_flask():
    from app import arvore_diaria, diarias, arvore_especialidade, especialidades 
    
    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "cadastrar":
            especialidade_str = request.form["especialidade"]
            quantidade_consultas = request.form["quantidade_consultas"]

            especialidade_dict = buscar_por_codigo(arvore_especialidade, "data/dados_especialidade.json", int(especialidade_str))
            
            especialidade_encontrada = None
            if isinstance(especialidade_dict, dict):
                especialidade_encontrada = especialidade_dict
            
            if especialidade_encontrada:
                
                dados_para_salvar = {
                    "especialidade_codigo": especialidade_encontrada["codigo"],
                    "quantidade_consultas": quantidade_consultas
                }

                posicao = salvar_diaria(dados_para_salvar, "data/dados_diaria.json")

                if posicao != -1:
                    
                    codigo_unico_diaria = f"{datetime.now().strftime('%Y%m%d')}{especialidade_encontrada['codigo']}"
                    arvore_diaria.inserir(codigo_unico_diaria, posicao)
                    diarias.append(dados_para_salvar)
                    
                    return redirect(url_for("diarias_bp.cadastrar_diaria_flask"))
                else:
                    return "Erro: Diária já existe para esta especialidade e data.", 400
            else:
                return "Erro: Especialidade não encontrada!", 400
        
        elif acao == "excluir":
            codigo_str = request.form.get("codigo")
            if codigo_str:
                excluir_do_json(codigo_str, "data/dados_diaria.json")
                arvore_diaria.excluir(codigo_str)
                print(f"Diária com código {codigo_str} excluída com sucesso.")
            
            else:
                print("Código de diária não fornecido para exclusão.")
            
            return redirect(url_for("diarias_bp.cadastrar_diaria_flask"))

    
    return render_template("cadastros/cadastro_diaria.html",
                           especialidades=especialidades)

@diarias_bp.route("/buscar", methods=["GET"])
def buscar():
    from app import arvore_diaria, arvore_especialidade, especialidades
    codigo = request.args.get('codigo')
    diaria = None 
    
    if codigo:
        diaria = buscar_por_codigo(arvore_diaria, "data/dados_diaria.json", codigo)

        if diaria:
            especialidade_dados = buscar_por_codigo(arvore_especialidade, "data/dados_especialidade.json", diaria['especialidade_codigo'])
            diaria['especialidade'] = especialidade_dados['descricao_esp'] if especialidade_dados else None
    
    return render_template('cadastros/cadastro_diaria.html', diaria=diaria, especialidades=especialidades)
