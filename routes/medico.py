from flask import Blueprint, request, render_template, redirect, url_for
from CONTROLLER.dados import salvar, buscar_por_codigo, excluir_do_json 
from MODEL.medico import Medico
from MODEL.cidade import Cidade
from MODEL.especialidade import Especialidade

medicos_bp = Blueprint('medicos_bp', __name__, url_prefix='/medicos')

@medicos_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_medico_flask():
    from app import arvore_medico, medicos, arvore_cidade, arvore_especialidade, cidades, especialidades
    if request.method == "POST":
        acao = request.form.get("acao")
        
        if acao == "cadastrar":
            nome = request.form["medico"]
            endereco = request.form["endereco"]
            telefone = request.form["telefone"]
            cidade_str = request.form["cidade"]
            especialidade_str = request.form["especialidade"]

            cidade_dict = buscar_por_codigo(arvore_cidade, "data/dados_cidades.json", int(cidade_str))
            especialidade_dict = buscar_por_codigo(arvore_especialidade, "data/dados_especialidade.json", int(especialidade_str))

            cidade_encontrada = None
            if isinstance(cidade_dict, dict):
                cidade_encontrada = Cidade(
                    cidade_dict["nome_cidade"],
                    cidade_dict["estado"],
                    codigo=cidade_dict["codigo"]
                )

            especialidade_encontrada = None
            if isinstance(especialidade_dict, dict):
                especialidade_encontrada = Especialidade(
                    especialidade_dict["descricao_esp"],
                    especialidade_dict["valor_consulta"],
                    especialidade_dict["limite_diario"],
                    codigo=especialidade_dict["codigo"]
                )
            
            if cidade_encontrada and especialidade_encontrada:
                medico_obj = Medico(nome, endereco, telefone, cidade_encontrada, especialidade_encontrada)
                
                dados_para_salvar = {
                    "codigo": medico_obj.codigo,
                    "nome_medico": medico_obj.nome_medico,
                    "endereco": medico_obj.endereco,
                    "telefone": medico_obj.telefone,
                    "cidade_codigo": cidade_encontrada.codigo,
                    "especialidade_codigo": especialidade_encontrada.codigo,
                }
                
                posicao = salvar(dados_para_salvar, "data/dados_medico.json")
                arvore_medico.inserir(medico_obj.codigo, posicao)
                medicos.append(dados_para_salvar)
                
                return redirect(url_for("medicos_bp.cadastrar_medico_flask"))
            else:
                return "Erro: Cidade ou Especialidade não encontrada!", 400

        elif acao == "excluir":
            codigo_str = request.form["codigo"]
            try:
                codigo = int(codigo_str)
                excluir_do_json(codigo, "data/dados_medico.json")
                arvore_medico.excluir(codigo)

            except ValueError:
                print("Erro: Código inválido para exclusão.")
            
            return redirect(url_for("medicos_bp.cadastrar_medico_flask"))

    return render_template("cadastros/cadastro_medico.html",
                           cidades=cidades,
                           especialidades=especialidades)

@medicos_bp.route("/buscar", methods=["GET"])
def buscar():
    from app import arvore_medico, arvore_cidade, arvore_especialidade, cidades, especialidades
    codigo = request.args.get('codigo', type=int)
    medico = None 
    
    if codigo:
        medico= buscar_por_codigo(arvore_medico, "data/dados_medico.json", codigo)
        
        if medico:
            cidade_dados = buscar_por_codigo(arvore_cidade, "data/dados_cidades.json", medico['cidade_codigo'])
            medico['cidade'] = cidade_dados['nome_cidade'] if cidade_dados else None
            medico['cidade_estado'] = cidade_dados['estado'] if cidade_dados else None

            especialidade_dados = buscar_por_codigo(arvore_especialidade, "data/dados_especialidade.json", medico['especialidade_codigo'])
            medico['especialidade'] = especialidade_dados['descricao_esp'] if especialidade_dados else None

    return render_template('cadastros/cadastro_medico.html', medico=medico, cidades=cidades, especialidades=especialidades)
