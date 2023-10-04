import boto3
import os
import subprocess
import mysql.connector

# Inicializar S3 y la conexión a la base de datos
s3 = boto3.client('s3')
conn = mysql.connector.connect(
    host="bbdd-proyecto-terminal-ttt-2023-1-13.cguzejqj5irq.us-east-2.rds.amazonaws.com",
    user="admin",
    password="Canela23.",
    database="bbdd-proyecto-terminal-ttt-2023-1-13"
)
cursor = conn.cursor()

def download_files_from_s3(bucket_name):
    base_path = 'Audios_Sin_Preprocesar'
    
    # Selecciona todas las URLs de los audios que se quieren procesar
    cursor.execute("SELECT audio_url FROM audios WHERE preprocessing_state = 'si'")
    audio_urls = [item[0] for item in cursor.fetchall()]

    for audio_url in audio_urls:
        s3_path = audio_url.replace("https://proyecto-terminal-ttt-2023-1-13.s3.amazonaws.com/", "")
        local_file_path = os.path.join('.', s3_path)
        local_folder = os.path.dirname(local_file_path)
        
        if not os.path.exists(local_folder):
            os.makedirs(local_folder)

        s3.download_file(bucket_name, s3_path, local_file_path)

def upload_to_github():
    subprocess.check_call(['git', 'add', '.'])
    subprocess.check_call(['git', 'commit', '-m', 'Add audio files'])
    subprocess.check_call(['git', 'push'])

def main():
    bucket_name = 'proyecto-terminal-ttt-2023-1-13'
    
    # 1. Descargar archivos desde S3 a la máquina local
    download_files_from_s3(bucket_name)

    # 2. Subir archivos al repositorio de GitHub
    upload_to_github()

    # 3. Eliminar archivos descargados de la máquina local
    for root, dirs, files in os.walk('Audios_Sin_Preprocesar'):
        for file in files:
            os.remove(os.path.join(root, file))
        if not os.listdir(root):
            os.rmdir(root)

    conn.close()

if __name__ == '__main__':
    main()
