import asyncio
from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument
import nest_asyncio
import os
from datetime import datetime, timezone

# Ідентифікатори API
api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'

# Ключові слова для пошуку
keywords = ["zala", "supercam", "orlan", "ланцет", "коптер"]

# Директорія для збереження відео
DOWNLOAD_DIR = "videos"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Фільтрація повідомлень
def filter_message(message, keywords, max_age_days=180):
    if not isinstance(message.media, MessageMediaDocument):
        return False  # Пропускаємо повідомлення без медіа

    if not any(doc in message.message.lower() for doc in keywords):
        return False  # Пропускаємо, якщо відсутні ключові слова

    # Поточна дата з часовою зоною
    now = datetime.now(timezone.utc)
    if (now - message.date).days > max_age_days:
        return False  # Пропускаємо старіші за 6 місяців

    return True

# Завантаження відеофайлів
async def download_videos(client, channel_username):
    print(f"Connecting to channel: {channel_username}")
    async for message in client.iter_messages(channel_username):
        if filter_message(message, keywords):
            file_name = f"{DOWNLOAD_DIR}/{message.id}.mp4"
            print(f"Downloading video: {file_name}")
            await client.download_media(message, file_name)

# Основна функція
async def main():
    channel_username = "ssternenko"
    async with TelegramClient('dronedtctn', api_id, api_hash) as client:
        await download_videos(client, channel_username)

# Запуск програми
if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
