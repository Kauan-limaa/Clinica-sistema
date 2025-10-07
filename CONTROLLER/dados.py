import json
from datetime import datetime
from MODEL.arvore import ArvoreBinaria
from pathlib import Path
import sys

def carregar_arvore_indices(arquivo_dados):
    arvore = ArvoreBinaria()
    try:
        with open(arquivo_dados, "r", encoding="utf-8") as f:
            dados = json.load(f)
        for posicao, registro in enumerate(dados):
            arvore.inserir(registro["codigo"], posicao)  
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return arvore

def carregar_dados_json(arquivo):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if not isinstance(dados, list):
                return []
            return dados
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar(chave, arquivo):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if not isinstance(dados, list):  
                dados = []
    except (FileNotFoundError, json.JSONDecodeError):
        dados = []

    dados.append(chave)

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    return len(dados) - 1  

import json

def excluir_do_json(codigo, arquivo):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if not isinstance(dados, list):
                dados = []
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    item_encontrado = False
    novos_dados = []
    for item in dados:
        if 'codigo' in item and item['codigo'] == int(codigo):
            item_encontrado = True
        else:
            novos_dados.append(item)
    
    if item_encontrado:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(novos_dados, f, indent=4, ensure_ascii=False)
        return True
    else:
        return False

def salvar_diaria(registro, arquivo):
    try:

        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if not isinstance(dados, list): 
                dados = []
    except (FileNotFoundError, json.JSONDecodeError):
        dados = []

    agora = datetime.now()
    codigo_dia = agora.strftime("%Y%m%d")
    
    if "especialidade_codigo" not in registro:
        
        return -1
    
    codigo_especialidade = registro["especialidade_codigo"]
    
    codigo_unico = f"{codigo_dia}{codigo_especialidade}"

    for item in dados:
        if "codigo" in item and item["codigo"] == codigo_unico:
            print(f"Erro: Já existe uma diária registrada para a especialidade {codigo_especialidade} na data {codigo_dia}.")
            return -1

    registro["codigo"] = codigo_unico
    dados.append(registro)

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print(f"Diária para a especialidade {codigo_especialidade} na data {codigo_dia} salva com sucesso!")
    return len(dados) - 1


def buscar_por_codigo(arvore, arquivo, codigo_a_buscar):
    op = arvore.buscar(codigo_a_buscar)

    if isinstance(op, list):
        posicao = op[0]
    else:
        posicao = op

    if posicao is None:
        return None

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            
            if not isinstance(dados, list):
                return None
            
            if 0 <= posicao < len(dados):
                return dados[posicao]
            else:
                return None
                
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    
def escrever_dados_json(dados, arquivo):
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao escrever dados no arquivo {arquivo}: {e}")

def atualizar_ou_criar_diaria(data_consulta, especialidade_codigo):
    ARQUIVO_DIARIAS = "data/dados_diarias.json"
    
    diarias = carregar_dados_json(ARQUIVO_DIARIAS)
    
    data_sem_traco = data_consulta.replace("-", "")
    chave_diaria = f"{data_sem_traco}{especialidade_codigo}"
    
    encontrado = False
    
    for diaria in diarias:
        if str(diaria.get("codigo")) == chave_diaria:
            try:
                quantidade_atual = int(diaria.get("quantidade_consultas", 0))
                diaria["quantidade_consultas"] = str(quantidade_atual + 1)
                encontrado = True
                break
            except ValueError:
                diaria["quantidade_consultas"] = "1"
                encontrado = True
                break
            
    if not encontrado:
        nova_diaria = {
            "especialidade_codigo": especialidade_codigo,
            "quantidade_consultas": "1",
            "codigo": chave_diaria
        }
        diarias.append(nova_diaria)
        
    escrever_dados_json(diarias, ARQUIVO_DIARIAS)

def diminuir(data_consulta, especialidade_codigo):
    ARQUIVO_DIARIAS = "data/dados_diarias.json"
    diarias = carregar_dados_json(ARQUIVO_DIARIAS)
    
    data_sem_traco = data_consulta.replace("-", "")
    chave_diaria = f"{data_sem_traco}{especialidade_codigo}"
    
    for diaria in diarias:
        if str(diaria.get("codigo")) == chave_diaria:
            try:
                quantidade_atual = int(diaria.get("quantidade_consultas", 0))
                if quantidade_atual > 0:
                    diaria["quantidade_consultas"] = str(quantidade_atual - 1)
                break
            except ValueError:
                break
    
    diarias_filtradas = [d for d in diarias if int(d.get("quantidade_consultas", 0)) > 0]
    
    escrever_dados_json(diarias_filtradas, ARQUIVO_DIARIAS)

def carregar_arvore_indices_por_data(arquivo_dados):
    arvore = ArvoreBinaria()
    try:
        with open(arquivo_dados, "r", encoding="utf-8") as f:
            dados = json.load(f)
        for posicao, registro in enumerate(dados):
    
            if "data" in registro:
                arvore.inserir(registro["data"], posicao)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return arvore


BASE_DIR = Path(__file__).resolve().parent.parent 
EXAMES_FILE = BASE_DIR / 'data' / 'dados_exame.json' 
CONSULTAS_FILE = BASE_DIR / 'data' / 'dados_consulta.json'


def calcular_faturamento_por_periodo(data_inicio_str, data_fim_str):
    
    faturamento_total = 0.0
    consultas_do_periodo = []
    mapa_exames = {}

    try:
        data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()

        if data_inicio > data_fim:
            raise ValueError("A data de início não pode ser posterior à data de fim.")
        
        with open(EXAMES_FILE, 'r', encoding='utf-8') as f:
            exames = json.load(f)
            
            for exame in exames:
                valor_str = exame.get('valor_exame', '0,00').replace('.', '').replace(',', '.')
                try:
                    codigo_int = int(exame['codigo'])
                except (ValueError, TypeError):
                    continue 
                mapa_exames[codigo_int] = {
                    "valor": float(valor_str),
                    "descricao": exame.get('descricao_exa', 'N/A')
                }
        
        with open(CONSULTAS_FILE, 'r', encoding='utf-8') as f:
            consultas = json.load(f)
            
            consultas_processadas = 0

            for consulta in consultas:
                data_consulta_str = consulta.get('data')

                try:
                    data_consulta = datetime.strptime(data_consulta_str, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    continue

                if data_inicio <= data_consulta <= data_fim: 
                    
                    codigo_exame = consulta.get('exame')
                    if isinstance(codigo_exame, str) and codigo_exame.isdigit():
                         codigo_exame = int(codigo_exame)
                    elif isinstance(codigo_exame, float):
                         codigo_exame = int(codigo_exame)
                   

                    dados_exame = mapa_exames.get(codigo_exame, {"valor": 0.0, "descricao": "Exame Não Encontrado"})
                    
                    valor_exame = dados_exame["valor"]
                    faturamento_total += valor_exame
                    consultas_processadas += 1
                    
                    consulta_detalhada = {
                        "codigo": consulta.get('codigo'),
                        "paciente_codigo": consulta.get('paciente'),
                        "medico_codigo": consulta.get('medico'),
                        "data": data_consulta_str,
                        "descricao": dados_exame["descricao"],
                        "valor": valor_exame 
                    }
                    consultas_do_periodo.append(consulta_detalhada)
            
        return {
            "faturamento_total": faturamento_total,
            "consultas": consultas_do_periodo
        }
        
    except FileNotFoundError as e:
        erro_msg = f"Arquivo não encontrado: '{e.filename}'"
        print(erro_msg, file=sys.stderr) 
        return {"faturamento_total": 0.0, "consultas": [], "erro": erro_msg}
    except ValueError as e:
        erro_msg = f"{e}. Certifique-se de que as datas estão no formato 'AAAA-MM-DD'."
        print(erro_msg, file=sys.stderr)
        return {"faturamento_total": 0.0, "consultas": [], "erro": erro_msg}
    except Exception as e:
        erro_msg = f"ERRO CRÍTICO NO PROCESSAMENTO: {e}"
        print(erro_msg, file=sys.stderr)
        return {"faturamento_total": 0.0, "consultas": [], "erro": erro_msg}
    

def calcular_faturamento_diario(data_desejada):
    
    faturamento_total = 0.0
    consultas_do_dia = []
    mapa_exames = {}
    data_alvo_str = str(data_desejada).strip()

    try:
      
        with open(EXAMES_FILE, 'r', encoding='utf-8') as f:
            exames = json.load(f)
            print(f"DEBUG: Total de Exames Carregados: {len(exames)}", file=sys.stderr)
            
            for exame in exames:
                valor_str = exame.get('valor_exame', '0,00').replace('.', '').replace(',', '.')
                try:
                    codigo_int = int(exame['codigo'])
                except (ValueError, TypeError):
                    continue 
                mapa_exames[codigo_int] = {
                    "valor": float(valor_str),
                    "descricao": exame.get('descricao_exa', 'N/A')
                }
        
        with open(CONSULTAS_FILE, 'r', encoding='utf-8') as f:
            consultas = json.load(f)
           
            consultas_encontradas = 0
            for consulta in consultas:
                data_consulta = consulta.get('data')

                if str(data_consulta) == data_alvo_str: 
                    consultas_encontradas += 1

                    codigo_exame = consulta.get('exame')
                    if isinstance(codigo_exame, str) and codigo_exame.isdigit():
                        codigo_exame = int(codigo_exame)
                    elif isinstance(codigo_exame, float):
                         codigo_exame = int(codigo_exame) 

                    dados_exame = mapa_exames.get(codigo_exame, {"valor": 0.0, "descricao": "Exame Não Encontrado"})
                    
                    valor_exame = dados_exame["valor"]
                    faturamento_total += valor_exame
                    
                    consulta_detalhada = {
                        "codigo": consulta.get('codigo'),
                        "paciente_codigo": consulta.get('paciente'),
                        "medico_codigo": consulta.get('medico'),
                        "descricao": dados_exame["descricao"],
                        "valor": valor_exame 
                    }
                    consultas_do_dia.append(consulta_detalhada)
            
            print(f"DEBUG: Consultas Filtradas e Encontradas: {consultas_encontradas}", file=sys.stderr)

        return {
            "faturamento_total": faturamento_total,
            "consultas": consultas_do_dia
        }
        
    except FileNotFoundError as e:
        erro_msg = f"ERRO FATAL: Arquivo não encontrado. O sistema buscou em: '{e.filename}'"
        print(erro_msg, file=sys.stderr) 
        return {"faturamento_total": 0.0, "consultas": [], "erro": erro_msg}
    except Exception as e:
        erro_msg = f"ERRO CRÍTICO NO PROCESSAMENTO DE DADOS: {e}"
        print(erro_msg, file=sys.stderr)
        return {"faturamento_total": 0.0, "consultas": [], "erro": erro_msg}
    


MEDICOS_FILE = BASE_DIR / 'data' / 'dados_medico.json'
def calcular_faturamento_medico(codigo_medico_desejado):
  
    faturamento_total = 0.0
    consultas_do_medico = []
    mapa_exames = {}
    
    try:
        medico_alvo_int = int(codigo_medico_desejado)
    except (ValueError, TypeError):
        return {"faturamento_total": 0.0, "consultas": [], "erro": "Código do Médico inválido."}


    try:
        with open(EXAMES_FILE, 'r', encoding='utf-8') as f:
            exames = json.load(f)
            for exame in exames:
                valor_str = exame.get('valor_exame', '0,00').replace('.', '').replace(',', '.')
                try:
                    codigo_int = int(exame['codigo'])
                except (ValueError, TypeError):
                    continue 
                mapa_exames[codigo_int] = {
                    "valor": float(valor_str),
                    "descricao": exame.get('descricao_exa', 'N/A')
                }

        with open(CONSULTAS_FILE, 'r', encoding='utf-8') as f:
            consultas = json.load(f)
            
            consultas_encontradas = 0
            for consulta in consultas:
                codigo_medico_consulta = consulta.get('medico')
                
                if isinstance(codigo_medico_consulta, str) and codigo_medico_consulta.isdigit():
                    codigo_medico_consulta = int(codigo_medico_consulta)
                
                if codigo_medico_consulta == medico_alvo_int: 
                    
                    consultas_encontradas += 1
                    
                    codigo_exame = consulta.get('exame')
                    if isinstance(codigo_exame, str) and codigo_exame.isdigit():
                        codigo_exame = int(codigo_exame)
                    elif isinstance(codigo_exame, float):
                         codigo_exame = int(codigo_exame) 

                    dados_exame = mapa_exames.get(codigo_exame, {"valor": 0.0, "descricao": "Exame Não Encontrado"})
                    
                    valor_exame = dados_exame["valor"]
                    faturamento_total += valor_exame
                    
                    
                    consulta_detalhada = {
                        "codigo": consulta.get('codigo'),
                        "paciente_codigo": consulta.get('paciente'),
                        "medico_codigo": consulta.get('medico'),
                        "descricao": dados_exame["descricao"],
                        "data": consulta.get('data'), 
                        "valor": valor_exame 
                    }
                    consultas_do_medico.append(consulta_detalhada)
            
            print(f"DEBUG_MEDICO: Consultas Filtradas e Encontradas: {consultas_encontradas}", file=sys.stderr)

        return {
            "faturamento_total": faturamento_total,
            "consultas": consultas_do_medico
        }
        
    except FileNotFoundError as e:
        erro_msg = f"ERRO FATAL: Arquivo não encontrado. O sistema buscou em: '{e.filename}'"
        print(erro_msg, file=sys.stderr) 
        return {"faturamento_total": 0.0, "consultas": [], "erro": erro_msg}
    except Exception as e:
        return {"faturamento_total": 0.0, "consultas": [], "erro": erro_msg}
    

def calcular_faturamento_especialidade(codigo_especialidade_desejado):
    faturamento_total = 0.0
    consultas_da_especialidade = []
    mapa_exames = {}
    medicos_da_especialidade = set()
    
    try:
        especialidade_alvo_int = int(codigo_especialidade_desejado)
    except (ValueError, TypeError):
        return {"faturamento_total": 0.0, "consultas": [], "erro": "Código da Especialidade inválido."}

    try:
        with open(EXAMES_FILE, 'r', encoding='utf-8') as f:
            exames = json.load(f)
            for exame in exames:
                valor_str = exame.get('valor_exame', '0,00').replace('.', '').replace(',', '.')
                try:
                    codigo_int = int(exame['codigo'])
                except (ValueError, TypeError):
                    continue 
                mapa_exames[codigo_int] = {
                    "valor": float(valor_str),
                    "descricao": exame.get('descricao_exa', 'N/A')
                }
    except FileNotFoundError as e:
        return {"faturamento_total": 0.0, "consultas": [], "erro": f"Arquivos JSON não encontrados: {e.filename}"}

    try:
        with open(MEDICOS_FILE, 'r', encoding='utf-8') as f:
            medicos = json.load(f)
           
            for medico in medicos:
                codigo_medico = medico.get('codigo')
                codigo_especialidade = medico.get('especialidade_codigo')
                
                try:
                    codigo_medico_int = int(codigo_medico)
                    codigo_especialidade_int = int(codigo_especialidade)
                except:
                    continue
                
                if codigo_especialidade_int == especialidade_alvo_int:
                    medicos_da_especialidade.add(codigo_medico_int)
        
    except FileNotFoundError as e:
        return {"faturamento_total": 0.0, "consultas": [], "erro": f"Arquivos JSON não encontrados: {e.filename}"}


    try:
        with open(CONSULTAS_FILE, 'r', encoding='utf-8') as f:
            consultas = json.load(f)
  
            consultas_encontradas = 0
            for consulta in consultas:
                codigo_medico_consulta = consulta.get('medico')
        
                try:
                    codigo_medico_consulta_int = int(codigo_medico_consulta)
                except:
                    continue

                if codigo_medico_consulta_int in medicos_da_especialidade: 
                    
                    consultas_encontradas += 1
                    
                    codigo_exame = consulta.get('exame')
                    
                    try:
                        codigo_exame = int(codigo_exame)
                    except (ValueError, TypeError):
                        codigo_exame = None    
                
                    dados_exame = mapa_exames.get(codigo_exame, {"valor": 0.0, "descricao": "Exame Não Encontrado"})
                    valor_exame = dados_exame["valor"]
                    faturamento_total += valor_exame
                    
                    consulta_detalhada = {
                        "codigo": consulta.get('codigo'),
                        "paciente_codigo": consulta.get('paciente'),
                        "medico_codigo": consulta.get('medico'),
                        "descricao": dados_exame["descricao"],
                        "data": consulta.get('data'), 
                        "valor": valor_exame 
                    }
                    consultas_da_especialidade.append(consulta_detalhada)

        return {
            "faturamento_total": faturamento_total,
            "consultas": consultas_da_especialidade
        }
        
    except Exception as e:
        return {"faturamento_total": 0.0, "consultas": [], "erro": f"Erro ao processar dados: {e}"}