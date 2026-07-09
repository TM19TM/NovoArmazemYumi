# drive_service.py
import requests
import base64
import os

# Cole aqui a URL azul que o Google te deu no final do Passo 2
URL_SCRIPT_GOOGLE = "https://script.google.com/macros/s/AKfycbyeCTvwHkdChT5tNk80xkWWzyJ42IZzvVa803-cnYSy3tvU8eNr7mTVCOmLQFeMYQL2mg/exec"

def fazer_upload_foto(caminho_foto_celular, nome_arquivo):
    try:
        if not os.path.exists(caminho_foto_celular):
            print("Arquivo local não encontrado.")
            return None
        
        # Converte a imagem do celular em texto (Base64) para enviar via JSON
        with open(caminho_foto_celular, "rb") as imagem_arquivo:
            foto_base64 = base64.b64encode(imagem_arquivo.read()).decode('utf-8')
        
        dados_envio = {
            "nome": nome_arquivo,
            "arquivo_base64": foto_base64
        }
        
        # Envia para o Google Apps Script
        resposta = requests.post(URL_SCRIPT_GOOGLE, json=dados_envio)
        
        if resposta.status_code == 200:
            resultado = resposta.json()
            if resultado.get("status") == "sucesso":
                return resultado.get("link")
            else:
                print(f"Erro no script do Google: {resultado.get('mensagem')}")
        else:
            print(f"Erro na requisição HTTP: {resposta.status_code}")
            
        return None
    except Exception as e:
        print(f"Erro geral no upload: {e}")
        return None