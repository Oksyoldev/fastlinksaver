# ClipsyLoader Bot 🤖

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-async-brightgreen)](https://core.telegram.org/bots/api)

Telegram-бот для быстрого скачивания медиа с популярных платформ.  
Поддерживает **TikTok, Instagram, YouTube Shorts, VK** и другие — избавляет от необходимости использовать сторонние приложения или сайты для загрузки контента.

---

## 🌟 Особенности
- Скачивание видео с TikTok, Instagram, YouTube Shorts, VK  
- Извлечение описания и заголовков  
- Проверка размера файла перед отправкой
- Поддержка прокси и кастомных заголовков  

---

## ⚙️ Технологии
- **Язык:** Python 3.11+
- **Библиотеки:**
  - `python-telegram-bot` (асинхронная версия)
  - `yt-dlp` (загрузка медиа)
  - `loguru` (логирование)
  - `python-dotenv` (конфигурация)
- **Хостинг:** любой VPS/облачный сервер  

## 📄 Лицензия
Этот проект распространяется под лицензией GNU Affero General Public License v3.0 - 
подробности см. в файле [LICENSE](LICENSE).

---

## 📦 Установка и запуск

### 1. Клонируйте репозиторий
`
git clone https://github.com/yourusername/clipsyloader-bot.git
cd clipsyloader-bot`
### 2. Установите зависимости
`pip install -r requirements.txt`
### 3. Настройте конфигурацию (config.py)
`TOKEN = "your_telegram_bot_token"
DOWNLOAD_PATH = "downloads"
MAX_FILE_SIZE_MB = 50
MAX_PHOTO_SIZE_MB = 20`
### 4. Запустите бота
```python bot.py```

---

## 🚀 Использование
## Просто отправьте боту ссылку на контент с поддерживаемой платформы:
- TikTok видео
- Instagram Reels
- YouTube Shorts
- VK видео
## Бот автоматически определит тип контента и отправит вам файл.
