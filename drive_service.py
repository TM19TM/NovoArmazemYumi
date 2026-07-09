# drive_service.py
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

ID_PASTA_DRIVE = "ID_DA_SUA_PASTA_AQUI" # Substitua pelo ID real da pasta

def conectar_ao_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    # O arquivo 'chave_google_drive.json' deve estar na mesma pasta do projeto
    credenciais = Credentials.from_service_account_file('chave_google_drive.json', scopes=SCOPES)
    return build('drive', 'v3', credentials=credenciais)

def fazer_upload_foto(caminho_foto_celular, nome_arquivo):
    try:
        servico = conectar_ao_drive()
        
        metadados_arquivo = {
            'name': nome_arquivo,
            'parents': [ID_PASTA_DRIVE]
        }
        
        media = MediaFileUpload(caminho_foto_celular, mimetype='image/jpeg')
        
        arquivo_criado = servico.files().create(
            body=metadados_arquivo,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        # Libera a permissão de leitura para o link funcionar no app
        servico.permissions().create(
            fileId=arquivo_criado.get('id'),
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
        
        return arquivo_criado.get('webViewLink')
    except Exception as e:
        print(f"Erro no upload para o Drive: {e}")
        return None