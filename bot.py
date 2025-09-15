import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, handle_link
from config import TOKEN, REQUEST_TIMEOUT

async def main():
    app = ApplicationBuilder()\
        .token(TOKEN)\
        .read_timeout(REQUEST_TIMEOUT)\
        .write_timeout(REQUEST_TIMEOUT)\
        .build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    print("Бот запущен и готов к работе!")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())