from telegram import Update
from telegram.ext import ContextTypes
from downloader import download_media
from telegram.constants import ParseMode
import mimetypes
import os
import time
from loguru import logger
import yt_dlp
from utils import is_supported_url

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
🎬 Добро пожаловать в <b>ClipsyLoader</b> | powered by <a href="https://t.me/oksyol">oksyoldev</a>

<b> Что я умею: </b>
• Скачивать видео с TikTok
• Скачивать видео и фото с Instagram
• Скачивать YouTube Shorts
• Скачивать видео из VK
• Скачивать фото из TikTok каруселей

❓ <u>Как использовать:</u>
<i>Просто отправьте мне ссылку на видео или пост с любой из этих платформ, и я мгновенно скачаю его для вас!</i>

⚡ Быстро и удобно
📦 Максимальный размер видео: 50MB
📷 Максимальный размер фото: 20MB
    """
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if not is_supported_url(url):
        await update.message.reply_text("*Неподдерживаемая платформа или неверная ссылка*", parse_mode='Markdown')
        return

    if 'instagram.com' in url.lower():
        msg_text = "⏳ *Скачиваем контент с Instagram...*"
    elif 'tiktok.com' in url.lower():
        msg_text = "⏳ *Скачиваем контент с TikTok...*"
    else:
        msg_text = "⏳ *Скачиваем контент...*"
    
    msg = await update.message.reply_text(msg_text, parse_mode='Markdown')

    file_path = None
    try:
        file_path, description, is_video = download_media(url)
        
        await msg.edit_text("✅ *Контент скачан! Отправляем...*", parse_mode='Markdown')

        mime_type, _ = mimetypes.guess_type(file_path)
        is_video = mime_type and mime_type.startswith('video')
        is_photo = mime_type and mime_type.startswith('image')

        time.sleep(1)
        
        try:
            if is_video:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=open(file_path, "rb"),
                    caption=f"🎬 *Скачано с помощью @fastlinksaver_bot*",
                    parse_mode='Markdown',
                    read_timeout=120,
                    write_timeout=120,
                    connect_timeout=120
                )
            elif is_photo:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=open(file_path, "rb"),
                    caption=f"📷 *Скачано с помощью @fastlinksaver_bot*",
                    parse_mode='Markdown',
                    read_timeout=60,
                    write_timeout=60,
                    connect_timeout=60
                )
            else:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id, 
                    document=open(file_path, "rb"),
                    caption=f"📄 *Скачано с помощью @fastlinksaver_bot*",
                    parse_mode='Markdown',
                    read_timeout=60,
                    write_timeout=60,
                    connect_timeout=60
                )
        except Exception as send_error:
            logger.error(f"Ошибка отправки: {send_error}")
            time.sleep(2)
            await context.bot.send_document(
                chat_id=update.effective_chat.id, 
                document=open(file_path, "rb"),
                caption=f"📄 *Скачано с помощью @fastlinksaver_bot*",
                parse_mode='Markdown',
                read_timeout=120,
                write_timeout=120,
                connect_timeout=120
            )

        if description and description != "Описание недоступно" and description.strip():
            if len(description) > 1000:
                description = description[:1000] + "..."
            
            content_type = "видео" if is_video else "фото"
            description_text = f"""
📝 Описание {content_type}:

{description}

{'🎬' if is_video else '📷'} Скачано с помощью @fastlinksaver_bot
            """
            await update.message.reply_text(description_text)
            
    except ValueError as ve:
        await msg.edit_text(f"*Ошибка:* {str(ve)}", parse_mode='Markdown')
    except yt_dlp.utils.DownloadError as de:
        if "blocked" in str(de).lower() or "ip address" in str(de).lower():
            await msg.edit_text("*Ошибка: Ваш IP заблокирован* 😢\n\nПопробуйте позже или используйте VPN", parse_mode='Markdown')
        elif "Unsupported URL" in str(de):
            await msg.edit_text("*Ошибка: Неподдерживаемый тип контента*\n\nПопробуйте другую ссылку", parse_mode='Markdown')
        else:
            await msg.edit_text("*Не удалось скачать контент.*\n\nВозможные причины:\n• Сервис заблокирован\n• Контент приватный\n• Неподдерживаемая платформа", parse_mode='Markdown')
        logger.error(f"Ошибка скачивания: {de}")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        try:
            await msg.edit_text("*Не удалось скачать контент.*\n\nВозможные причины:\n• Сервис заблокирован\n• Контент приватный\n• Неподдерживаемая платформа\n• Превышен лимит размера", parse_mode='Markdown')
        except:
            await update.message.reply_text("*Не удалось скачать контент.*\n\nВозможные причины:\n• Сервис заблокирован\n• Контент приватный\n• Неподдерживаемая платформа\n• Превышен лимит размера", parse_mode='Markdown')
    finally:
        # Удаляем файл
        if file_path and os.path.exists(file_path):
            try:
                time.sleep(1)
                os.remove(file_path)
                base_name = os.path.splitext(file_path)[0]
                for ext in ['.info.json', '.description']:
                    meta_path = base_name + ext
                    if os.path.exists(meta_path):
                        os.remove(meta_path)
            except Exception as delete_error:
                logger.error(f"Ошибка удаления файла {file_path}: {delete_error}")