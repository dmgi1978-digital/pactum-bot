import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# === ТОКЕН ИЗ RENDER ===
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is required!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# === СОСТОЯНИЕ ===
class UserState(StatesGroup):
    escrow_amount = State()

# === КЛАВИАТУРА ===
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Open Escrow")]
    ],
    resize_keyboard=True
)

# === /start ===
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 <b>Pactum & Escrow</b>\n\nYour word = smart contract on TON.\nOpen escrow to protect your deal.\n\nFee: 5.5% in Stars.",
        reply_markup=main_menu,
        parse_mode="HTML"
    )

# === ОБРАБОТКА КНОПКИ ===
@dp.message(lambda msg: msg.text == "💰 Open Escrow")
async def open_escrow(message: types.Message, state: FSMContext):
    await state.set_state(UserState.escrow_amount)
    await message.answer("💰 Enter amount in Stars (min 10):")

# === ПРИЁМ СУММЫ И ОТПРАВКА ИНВОЙСА ===
@dp.message(UserState.escrow_amount)
async def process_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount < 10:
            await message.answer("❌ Minimum: 10 Stars")
            return
    except ValueError:
        await message.answer("❌ Please enter a number")
        return

    commission = int(amount * 0.055)
    total = amount + commission

    # === ГЛАВНОЕ: ПРАВИЛЬНЫЙ ИНВОЙС ДЛЯ STARS ===
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Pactum & Escrow",
        description=f"Protection for {amount} Stars. Fee: {commission} Stars.",
        payload="escrow_deal",
        provider_token="",      # ← ДОЛЖЕН БЫТЬ ПУСТЫМ!
        currency="XTR",         # ← ТОЛЬКО "XTR"!
        prices=[LabeledPrice(label="Total", amount=total)],
        start_parameter="escrow"
    )
    await state.clear()

# === ОБРАБОТКА ОПЛАТЫ ===
@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(lambda msg: msg.successful_payment)
async def successful_payment(message: types.Message):
    total = message.successful_payment.total_amount
    await message.answer(f"✅ Paid {total} Stars! Escrow is active.")

# === ЗАПУСК ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
