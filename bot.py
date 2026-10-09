from aiogram import Bot, Dispatcher, types
from asyncio import run
from aiogram.filters import CommandStart

from dotenv import load_dotenv
import os

from ai import ai

load_dotenv()

bot = Bot(token=os.environ.get('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(m:types.Message):
    await m.reply('Assalomu Aleykum. AI botga hush kelibsiz!')

@dp.message()
async def ai_response(m:types.Message):
    response = ai.models.generate_content(
        model='gemini-3.5-flash',
        contents=m.text
    )
    try:
        # Dastlab Markdown formatida yuborishga urinib ko'radi
        await m.answer(response.text, parse_mode="Markdown")
    except Exception:
        # Agar Telegram parse qila olmasa, parse_mode'siz (oddiy matn) yuboradi
        await m.answer(response.text)

async def main():
    await dp.start_polling(bot)
    print('Bot ishga tushdi')

if __name__=='__main__':
    run(main())