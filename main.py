from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN, ADMIN_ID, LOG_CHANNEL_ID
from pymongo import MongoClient
import openai
import logging

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Logging setup
logging.basicConfig(level=logging.INFO)

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.ananya

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@dp.message_handler(commands=["start"])
async def start_cmd(msg: types.Message):
    await bot.send_message(msg.chat.id, f"Hey {msg.from_user.first_name}! 💖 I'm Ananya, your new bestie!")
    await bot.send_message(LOG_CHANNEL_ID, f"#START by {msg.from_user.id} ({msg.from_user.full_name})")

@dp.message_handler(commands=["mood"])
async def mood_checkin(msg: types.Message):
    await msg.reply("Tell me how you're feeling today 📝")
    db.moods.insert_one({"user_id": msg.from_user.id, "name": msg.from_user.full_name})

@dp.message_handler()
async def chat(msg: types.Message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": msg.text}]
    )
    await msg.reply(response["choices"][0]["message"]["content"])
    await bot.send_message(LOG_CHANNEL_ID, f"#CHAT from {msg.from_user.id}: {msg.text}")

if __name__ == "__main__":
    executor.start_polling(dp)
