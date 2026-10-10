from aiogram import Bot, Dispatcher, types, F
from asyncio import run
from aiogram.filters import CommandStart

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from dotenv import load_dotenv
import os

from database import init_db, create_user, get_user, create_messages, set_user_topic, get_messages, get_user_topic
from ai import ai

load_dotenv()

bot = Bot(token=os.environ.get('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()


AI_TOPICS = {
    'Maslahatchi': "Siz O'zbekistonlik biron bir insonning shaxsiy maslahatchisiz. Bunda siz biron nima so'ralganda faqat to'g'risini aytishingiz kerak. Kimnidir yonini olmasdan!",
    "Do'stona": "Siz Do'stona AI maslahatchisiz. Savollarga turli xil smiliklar bilan va do'stona ohangda javob bering!",
    "Ko'd yordamchisi": "Siz professional dasturchisiz. Har qanday dasturlash tiliada har qanday dasturni yarata olasiz.",
}


def create_buttons():
    buttons = [[KeyboardButton(text=text)] for text in AI_TOPICS.keys()]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, persistent=True)

@dp.message(CommandStart())
async def start_handler(m:types.Message):
    user = get_user(m.from_user.id)
    if user:
        await m.reply(f'Assalomu Aleykum {m.from_user.first_name}. AI botga qaytganingizdan hursandmiz!', reply_markup=create_buttons())
    else:
        user = create_user(m.from_user.id, m.from_user.first_name)
        await m.reply(f'Assalomu Aleykum {m.from_user.first_name}. AI botga hush kelibsiz', reply_markup=create_buttons())


@dp.message(F.text.in_(AI_TOPICS.keys()))
async def change_topic_handler(m:types.Message):
    set_user_topic(m.from_user.id, m.text)
    await m.reply(f'Mavzu {m.text}ga o\'zgardi!')

@dp.message()
async def ai_response(m:types.Message):
    topic = get_user_topic(m.from_user.id)

    create_messages(m.from_user.id, m.text, 'user')

    last_messages = get_messages(m.from_user.id, 10)
    
    if topic:
        response = ai.models.generate_content(
            model='gemini-3.5-flash',
            contents=last_messages,
            config={
                'inroductions': AI_TOPICS[topic]
            }
        )
    else:
        response = ai.models.generate_content(
            model='gemini-3.5-flash',
            contents=m.text,
        )
    try:
        # Dastlab Markdown formatida yuborishga urinib ko'radi
        await m.answer(response.text, parse_mode="Markdown")

        create_messages(m.from_user.id, response.text, role='ai')
    except Exception:
        # Agar Telegram parse qila olmasa, parse_mode'siz (oddiy matn) yuboradi
        await m.answer(response.text)

async def main():
    init_db()
    print('Bot ishga tushdi')
    await dp.start_polling(bot)

if __name__=='__main__':
    run(main())