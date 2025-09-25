import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ТВОЙ ТОКЕН ОТ @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаём клавиатуру
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔖 Дать клятву")],
        [KeyboardButton(text="🎲 Заключить пари")],
        [KeyboardButton(text="💰 Открыть эскроу")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "👋 Привет! Я — Pactum & Escrow.\n\n"
        "Выбери, что хочешь сделать:",
        reply_markup=main_menu
    )

# Заглушки для кнопок
@dp.message(lambda message: message.text in ["🔖 Дать клятву", "🎲 Заключить пари", "💰 Открыть эскроу"])
async def button_handler(message: types.Message):
    if message.text == "🔖 Дать клятву":
        await message.answer("Скоро: дай клятву, которую нельзя отрицать.")
    elif message.text == "🎲 Заключить пари":
        await message.answer("Скоро: спорь на Stars с гарантией выплаты.")
    elif message.text == "💰 Открыть эскроу":
        await message.answer("Скоро: защити сделку через блокчейн.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
