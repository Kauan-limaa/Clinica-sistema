import os
import json

class GeradorCodigo:
    def __init__(self, nome_entidade, pasta='data/codigos', arquivo_dados_principal=None):
        self.pasta = pasta
        self.nome_entidade = nome_entidade
        self.arquivo_dados_principal = arquivo_dados_principal
        self.nome_arquivo = os.path.join(self.pasta, f'ultimo_codigo_{nome_entidade}.json')
        
        if not os.path.exists(self.pasta):
            os.makedirs(self.pasta)
            print(f"DEBUG: Pasta '{self.pasta}' criada.")
            
        self.atual = self._carregar_ultimo_codigo()

    def _obter_max_codigo_do_json_principal(self):
        if not self.arquivo_dados_principal or not os.path.exists(self.arquivo_dados_principal):
            return 0
            
        try:
            with open(self.arquivo_dados_principal, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                
            if not isinstance(dados, list) or not dados:
                return 0
                
            max_codigo = 0
            for item in dados:
                try:
                    codigo = int(item.get('codigo', 0))
                    if codigo > max_codigo:
                        max_codigo = codigo
                except (ValueError, TypeError):
                    continue
                    
            return max_codigo
            
        except (json.JSONDecodeError, FileNotFoundError):
            return 0

    def _carregar_ultimo_codigo(self):
        codigo_salvo = 0
        if os.path.exists(self.nome_arquivo):
            with open(self.nome_arquivo, 'r') as f:
                try:
                    dados = json.load(f)
                    codigo_salvo = dados.get('ultimo_codigo', 0)
                except (json.JSONDecodeError, FileNotFoundError):
                    pass
        
        max_codigo_principal = self._obter_max_codigo_do_json_principal()
        
        return max(codigo_salvo, max_codigo_principal)

    def _salvar_codigo(self):
        with open(self.nome_arquivo, 'w') as f:
            dados = {'ultimo_codigo': self.atual}
            json.dump(dados, f)
            print(f"DEBUG: Código {self.atual} salvo em '{self.nome_arquivo}'.")

    def proximo(self):
        self.atual += 1
        self._salvar_codigo()
        return self.atual