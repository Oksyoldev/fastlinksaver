import os
import glob

TOKEN = "8368058845:AAGexFOUWvbqzjNc4Q9ioc1-Ki1rmtXKaYg"
DOWNLOAD_PATH = "downloads"
MAX_FILE_SIZE_MB = 50
MAX_PHOTO_SIZE_MB = 20
REQUEST_TIMEOUT = 60

os.makedirs(DOWNLOAD_PATH, exist_ok=True)
os.makedirs("logs", exist_ok=True)

for old_file in glob.glob(os.path.join(DOWNLOAD_PATH, '*')):
    try:
        os.remove(old_file)
    except:
        pass