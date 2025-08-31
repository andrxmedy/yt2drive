import os
import yt_dlp
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

#Configurações do Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

def authenticate_drive():
    """Autentica no Google Drive e retorna o serviço."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return build("drive", "v3", credentials=creds)

def download_youtube_video(url, filename="video.mp4"):
    """Baixa o vídeo do YouTube em formato MP4 compatível."""
    ydl_opts = {
        'outtmpl': filename,
        'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best[ext=mp4]',
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }
    
    try:
        print("Iniciando download do vídeo...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            #Encontrar o arquivo baixado
            actual_filename = ydl.prepare_filename(info)
            if actual_filename != filename and os.path.exists(actual_filename):
                os.rename(actual_filename, filename)
            
            print(f"✅ Download concluído: {filename}")
            return filename
            
    except Exception as e:
        print(f"Erro no download: {str(e)}")
        return download_fallback_youtube_video(url, filename)

def download_fallback_youtube_video(url, filename="video.mp4"):
    """Método fallback mais simples para download."""
    ydl_opts = {
        'outtmpl': filename,
        'format': 'worst[ext=mp4]',  
        'quiet': False,
    }
    
    try:
        print("Tentando método fallback...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            if os.path.exists(filename):
                print(f"Download fallback concluído: {filename}")
                return filename
            else:
                for file in os.listdir('.'):
                    if file.endswith(('.mp4', '.webm', '.mkv')):
                        os.rename(file, filename)
                        print(f"Arquivo renomeado para: {filename}")
                        return filename
                
                raise Exception("Nenhum arquivo de vídeo encontrado")
                
    except Exception as e:
        print(f"Fallback também falhou: {str(e)}")
        raise

def upload_to_drive(service, file_path):
    """Faz upload para o Drive e retorna link público."""
    try:
        if not os.path.exists(file_path):
            raise Exception(f"Arquivo {file_path} não encontrado para upload")
        
        print("Iniciando upload para Google Drive...")
        
        file_metadata = {
            "name": os.path.basename(file_path),
            "mimeType": "video/mp4"
        }
        
        media = MediaFileUpload(
            file_path, 
            mimetype="video/mp4", 
            resumable=True,
            chunksize=1024*1024 
        )
        
        file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields="id"
        ).execute()
        
        file_id = file.get("id")
        print(f"Arquivo criado no Drive: {file_id}")

        #Tornar o arquivo público
        print("Tornando arquivo público...")
        service.permissions().create(
            fileId=file_id,
            body={"role": "reader", "type": "anyone"}
        ).execute()

        drive_link = f"https://drive.google.com/file/d/{file_id}/view"
        print(f"Upload concluído! Link público: {drive_link}")
        return drive_link
        
    except Exception as e:
        print(f"Erro no upload: {str(e)}")
        raise

def wait_for_drive_processing(service, file_id, max_attempts=10):
    """Aguarda o processamento do vídeo no Drive."""
    import time
    print("Aguardando processamento do vídeo no Drive...")
    
    for attempt in range(max_attempts):
        try:
            file = service.files().get(fileId=file_id, fields="videoMediaMetadata").execute()
            if file.get('videoMediaMetadata'):
                print("Vídeo processado pelo Drive")
                return True
        except:
            pass
        
        print(f"Tentativa {attempt + 1}/{max_attempts} - Aguardando...")
        time.sleep(5)
    
    print("Timeout aguardando processamento do vídeo")
    return False

if __name__ == "__main__":
    try:
        youtube_url = input("Cole o link do YouTube: ").strip()
        print(f"Processando: {youtube_url}")

        video_file = download_youtube_video(youtube_url)

        if os.path.exists(video_file):
            file_size = os.path.getsize(video_file) / (1024*1024) 
            print(f"Tamanho do arquivo: {file_size:.2f} MB")
            if file_size < 0.1:  
                raise Exception("Arquivo muito pequeno - download pode ter falhado")

        print("Autenticando no Google Drive...")
        drive_service = authenticate_drive()

        #Upload e link público
        link = upload_to_drive(drive_service, video_file)

        file_id = link.split('/d/')[1].split('/')[0]
        wait_for_drive_processing(drive_service, file_id)

        #Remove arquivo local
        if os.path.exists(video_file):
            os.remove(video_file)
            print("Arquivo local removido")

        print("\nTudo pronto!")
        print(f"Link público do vídeo: {link}")
        print("Pode levar alguns minutos para o vídeo ficar totalmente disponível para reprodução")
        
    except Exception as e:
        print(f"Erro no processo: {str(e)}")
        for file in os.listdir('.'):
            if file.startswith('video') and file.endswith(('.mp4', '.webm', '.part')):
                try:
                    os.remove(file)
                    print(f"🧹 Limpando: {file}")
                except:
                    pass