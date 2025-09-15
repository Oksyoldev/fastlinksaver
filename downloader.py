import yt_dlp
import os
import mimetypes
import time
from loguru import logger
from config import DOWNLOAD_PATH, MAX_FILE_SIZE_MB, MAX_PHOTO_SIZE_MB

logger.add("logs/downloads.log", rotation="5 MB")

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
        percent = downloaded / total * 100
        print(f"Скачивание: {percent:.1f}%")
    elif d['status'] == 'finished':
        print("Скачивание завершено!")

def download_media(url: str):
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_PATH}/%(id)s.%(ext)s',
        'format': 'best',
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        'progress_hooks': [progress_hook],
        'socket_timeout': 30,
        'writedescription': False,
        'writeinfojson': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
            # Поиск файла
            if not os.path.exists(file_path):
                base_name = os.path.splitext(file_path)[0]
                for ext in ['.mp4', '.jpg', '.jpeg', '.png', '.webp', '.mkv', '.mov']:
                    alternative_path = base_name + ext
                    if os.path.exists(alternative_path):
                        file_path = alternative_path
                        break
            
            if not os.path.exists(file_path):
                files = [f for f in os.listdir(DOWNLOAD_PATH) 
                        if not f.endswith(('.json', '.description', '.part'))]
                if files:
                    files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_PATH, x)), reverse=True)
                    file_path = os.path.join(DOWNLOAD_PATH, files[0])
            
            mime_type, _ = mimetypes.guess_type(file_path)
            is_video = mime_type and mime_type.startswith('video')
            is_photo = mime_type and mime_type.startswith('image')
            
            description = info.get("description", "").strip()
            if not description:
                description = info.get("title", "").strip()
            
            if not description:
                description = info.get("alt_title", "") or info.get("uploader", "")
            
            if not description:
                description = "Описание недоступно"

            # Проверяем размер
            size_mb = os.path.getsize(file_path) / (1024*1024)
            max_size = MAX_FILE_SIZE_MB if is_video else MAX_PHOTO_SIZE_MB
            
            if size_mb > max_size:
                os.remove(file_path)
                content_type = "видео" if is_video else "фото"
                raise ValueError(f"{content_type.capitalize()} слишком большое ({size_mb:.1f} MB)")

            logger.info(f"Downloaded {url} -> {file_path} (type: {'video' if is_video else 'photo'})")
            return file_path, description, is_video

    except Exception as e:
        logger.error(f"Ошибка при скачивании {url}: {e}")
        raise e