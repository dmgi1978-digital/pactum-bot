import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔖 Дать клятву"),
            KeyboardButton(text="🎲 Заключить пари")
        ],
        [
            KeyboardButton(text="💰 Открыть эскроу")
        ],
        [
            KeyboardButton(text="🏅 Моя репутация"),
            KeyboardButton(text="❓ Как это работает?")
        ]
    ],
    resize_keyboard=True
)

start_text = (
    "👋 <b>Привет! Я — Pactum & Escrow.</b>\n\n"
    "Здесь твоё слово = контракт.\n"
    "Дай клятву. Заключи пари. Защити сделку.\n\n"
    "✅ Выполнил — получи репутацию.\n"
    "❌ Не выполнил — потеряешь Stars и доверие.\n\n"
    "Выбери, с чего начнёшь:"
)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(start_text, reply_markup=main_menu, parse_mode="HTML")

@dp.message(lambda msg: msg.text == "❓ Как это работает?")
async def how_it_works(message: types.Message):
    text = (
        "⚖️ <b>Pactum & Escrow</b> — эскроу для Telegram.\n\n"
        "🔹 <b>Клятва</b> — дай обещание перед свидетелями.\n"
        "🔹 <b>Пари</b> — спорь на Stars.\n"
        "🔹 <b>Эскроу</b> — защити сделку. Деньги в блокчейне.\n\n"
        "💎 Комиссия: 5.5% — за устранение риска."
    )
    await message.answer(text, parse_mode="HTML")

@dp.message(lambda msg: msg.text == "🏅 Моя репутация")
async def reputation(message: types.Message):
    await message.answer("🔒 Репутация станет доступна после первой сделки.")

@dp.message(lambda msg: msg.text in ["🔖 Дать клятву", "🎲 Заключить пари", "💰 Открыть эскроу"])
async def feature_soon(message: types.Message):
    await message.answer("🔥 Скоро! Следи за @PactumEscrow.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
