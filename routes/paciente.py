from flask import Blueprint, request, render_template, redirect, url_for
from CONTROLLER.dados import salvar, carregar_dados_json, buscar_por_codigo, excluir_do_json
from MODEL.paciente import Paciente 
from MODEL.cidade import Cidade 

pacientes_bp = Blueprint('pacientes_bp', __name__, url_prefix='/pacientes')

@pacientes_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_paciente_flask():
    from app import arvore_paciente, pacientes, arvore_cidade, cidades
    
    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "cadastrar":
            nome = request.form["paciente"]
            dtnascimento = request.form["dt_nascimento"] 
            endereco = request.form["endereco"] 
            telefone = request.form["telefone"] 
            idcidade_str = request.form["cidade"] 
            peso = request.form["peso"]
            altura = request.form["altura"]

            posicao_cidade = arvore_cidade.buscar(int(idcidade_str))
            
            cidade_encontrada = None
            if posicao_cidade is not None:
                
                cidade = buscar_por_codigo(arvore_cidade, "data/dados_cidades.json", int(idcidade_str))
                cidade_encontrada = Cidade(
                    cidade["nome_cidade"],
                    cidade["estado"],
                    codigo=cidade["codigo"]
                )
            
            if cidade_encontrada:
                paciente_obj = Paciente(nome, dtnascimento, endereco, telefone, cidade_encontrada, peso, altura)
                
                dados_para_salvar = {
                    "codigo": paciente_obj.codigo,
                    "nome_paciente": paciente_obj.nome_paciente,
                    "dt_nascimento": paciente_obj.dt_nascimento,
                    "endereco": paciente_obj.endereco,
                    "telefone": paciente_obj.telefone,
                    "cidade_codigo": cidade_encontrada.codigo,
                    "peso": paciente_obj.peso,
                    "altura": paciente_obj.altura
                }
                
                posicao = salvar(dados_para_salvar, "data/dados_paciente.json")
                arvore_paciente.inserir(paciente_obj.codigo, posicao)
                pacientes.append(dados_para_salvar)
                
                return redirect(url_for("pacientes_bp.cadastrar_paciente_flask"))
            else:
                return "Erro: Cidade não encontrada!", 400

        elif acao == "excluir":
            codigo_str = request.form.get("codigo")
            try:
                codigo = int(codigo_str)
                excluir_do_json(codigo, "data/dados_paciente.json")
                arvore_paciente.excluir(codigo)

            except ValueError:
                print("Erro: Código inválido para exclusão.")

            return redirect(url_for("pacientes_bp.cadastrar_paciente_flask"))
    
    return render_template("cadastros/cadastro_paciente.html",
                           pacientes=pacientes,
                           cidades=cidades)

@pacientes_bp.route("/buscar", methods=["GET"])
def buscar():
    from app import arvore_paciente, arvore_cidade, cidades
    codigo = request.args.get('codigo', type=int)
    paciente = None 
    
    if codigo:
        paciente = buscar_por_codigo(arvore_paciente, "data/dados_paciente.json", codigo)
        if paciente: 
            cidade_dados = buscar_por_codigo(arvore_cidade, "data/dados_cidades.json", paciente['cidade_codigo'])
            
            try:
                peso_str = str(paciente.get('peso', '')).replace(',', '.').strip()
                altura_str = str(paciente.get('altura', '')).replace(',', '.').strip()
                peso = float(peso_str) if peso_str else None
                altura = float(altura_str) if altura_str else None
            except (ValueError, TypeError):
                peso, altura = None, None

            if peso is not None and altura is not None and altura > 0:
                imc = round(peso / (altura ** 2), 2)
                paciente['imc'] = imc

                if imc < 18.5:
                    paciente['diagnostico'] = "Abaixo do peso"
                elif 18.5 <= imc < 25:
                    paciente['diagnostico'] = "Peso normal"
                elif 25 <= imc < 30:
                    paciente['diagnostico'] = "Sobrepeso"
                else:
                    paciente['diagnostico'] = "Obesidade"
            else:
                paciente['imc'] = None
                paciente['diagnostico'] = "Dados insuficientes"

            paciente['cidade_descricao'] = cidade_dados['nome_cidade'] if cidade_dados else None
            paciente['cidade_estado'] = cidade_dados['estado'] if cidade_dados else None

    return render_template('cadastros/cadastro_paciente.html', paciente=paciente, cidades=cidades)
