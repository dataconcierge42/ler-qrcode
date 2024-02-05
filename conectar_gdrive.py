from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import json

# Substitua 'credentials.json' pelo caminho para o seu arquivo de credenciais baixado
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'

def service_account_login():
    creds = None
    # O arquivo token.json armazena os tokens de acesso e atualização do usuário e é
    # criado automaticamente quando o fluxo de autorização é concluído pela primeira vez.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Se não há credenciais disponíveis ou são inválidas, faça o fluxo de login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva as credenciais para a próxima execução
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def ler_e_atualizar_json(service, file_id):
    # Solicita o download do arquivo JSON
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    # Lê o conteúdo do JSON
    json_data = json.load(fh)

    # Aqui você pode modificar o json_data conforme necessário
    # Por exemplo: json_data['novo'] = 'valor'

    # Salva as alterações no mesmo arquivo
    fh.seek(0)
    fh.truncate()
    json.dump(json_data, fh)
    fh.seek(0)
    media = MediaIoBaseUpload(fh, mimetype='application/json')
    updated_file = service.files().update(fileId=file_id, media_body=media).execute()

    print('Arquivo JSON atualizado')

# Substitua 'YOUR_FILE_ID' pelo ID real do arquivo JSON no Google Drive
service = service_account_login()
ler_e_atualizar_json(service, 'YOUR_FILE_ID')
