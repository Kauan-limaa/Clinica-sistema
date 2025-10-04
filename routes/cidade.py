from flask import Blueprint, request, render_template, redirect, url_for
from MODEL.cidade import Cidade 
from CONTROLLER.dados import salvar, buscar_por_codigo, excluir_do_json # Importei a função ajustada

cidades_bp = Blueprint('cidades_bp', __name__, url_prefix='/cidades')


@cidades_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_cidade_flask():
    from app import arvore_cidade, cidades 
    
    if request.method == "POST":
        acao = request.form.get("acao")
        
        if acao == "cadastrar":
            nome = request.form["nome"]
            estado = request.form["estado"]
            cidade = Cidade(nome, estado)
            
            posicao = salvar(cidade.__dict__, "data/dados_cidades.json")
            arvore_cidade.inserir(cidade.codigo, posicao)
            cidades.append({"codigo": cidade.codigo, "nome_cidade": nome, "estado": estado})
            
            return redirect(url_for("cidades_bp.cadastrar_cidade_flask"))
            
        elif acao == "excluir":
            codigo_str = request.form["codigo"]
            try:
                codigo = int(codigo_str)
                excluir_do_json(codigo, "data/dados_cidades.json")
                arvore_cidade.excluir(codigo)
            
            except ValueError:
                print("Código inválido para exclusão.")

            return redirect(url_for("cidades_bp.cadastrar_cidade_flask"))
    
    return render_template("cadastros/cadastro_cidade.html", cidades=cidades)

@cidades_bp.route("/buscar", methods=["GET"])
def buscar():
    from app import arvore_cidade
    codigo = request.args.get('codigo', type=int)
    cidade = None 
    
    if codigo:
        cidade = buscar_por_codigo(arvore_cidade, "data/dados_cidades.json", codigo)
    return render_template('cadastros/cadastro_cidade.html', cidade=cidade)