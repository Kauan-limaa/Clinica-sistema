from flask import Blueprint, request, render_template, redirect, url_for
from CONTROLLER.dados import salvar, buscar_por_codigo, excluir_do_json 
from MODEL.exame import Exame
from MODEL.especialidade import Especialidade

exames_bp = Blueprint('exames_bp', __name__, url_prefix='/exames')

@exames_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_exame_flask():
    from app import arvore_exame, exames, arvore_especialidade, especialidades
    if request.method == "POST":
        acao = request.form.get("acao")
        
        if acao == "cadastrar":
            descricao_exa = request.form["descricao_exa"]
            especialidade_str = request.form["especialidade"] 
            valor_exame = request.form["valor_exame"]

            especialidade_dict = buscar_por_codigo(arvore_especialidade, "data/dados_especialidade.json", int(especialidade_str))
            
            especialidade_encontrada = None
            if isinstance(especialidade_dict, dict):
                especialidade_encontrada = Especialidade(
                    especialidade_dict["descricao_esp"],
                    especialidade_dict["valor_consulta"],
                    especialidade_dict["limite_diario"],
                    codigo=especialidade_dict["codigo"]
                )
            
            if especialidade_encontrada:
                exame_obj = Exame(descricao_exa, especialidade_encontrada, valor_exame)
                
                dados_para_salvar = {
                    "codigo": exame_obj.codigo,
                    "descricao_exa": exame_obj.descricao_exa,
                    "especialidade_codigo": especialidade_encontrada.codigo,
                    "valor_exame": exame_obj.valor_exame,
                }

                posicao = salvar(dados_para_salvar, "data/dados_exame.json")
                arvore_exame.inserir(exame_obj.codigo, posicao)
                exames.append(dados_para_salvar)
                
                return redirect(url_for("exames_bp.cadastrar_exame_flask"))
            else:
                return "Erro: Especialidade não encontrada!", 400
        
        elif acao == "excluir":
            codigo_str = request.form["codigo"]
            try:
                codigo = int(codigo_str)
                excluir_do_json(codigo, "data/dados_exame.json")
                arvore_exame.excluir(codigo)

            except ValueError:
                print("Erro: Código inválido para exclusão.")
            
            return redirect(url_for("exames_bp.cadastrar_exame_flask"))

    return render_template("cadastros/cadastro_exame.html",
                           exames=exames,
                           especialidades=especialidades)

@exames_bp.route("/buscar", methods=["GET"])
def buscar():
    from app import arvore_exame, arvore_especialidade, especialidades
    codigo = request.args.get('codigo', type=int)
    exame = None
    
    if codigo:
        exame = buscar_por_codigo(arvore_exame, "data/dados_exame.json", codigo)
               
        if exame: 
            especialidade_dados = buscar_por_codigo(arvore_especialidade, "data/dados_especialidade.json", exame['especialidade_codigo'])
            
            exame['especialidade_descricao'] = especialidade_dados['descricao_esp'] if especialidade_dados else None
            
    return render_template('cadastros/cadastro_exame.html', exame=exame, especialidades=especialidades)
