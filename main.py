import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен!")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# === 15 ЯЗЫКОВ ===
TEXTS = {
    "ru": {
        "start": "👋 <b>Привет! Я — Pactum & Escrow.</b>\n\nЗдесь твоё слово = контракт.\nДай клятву. Заключи пари. Защити сделку.\n\n✅ Выполнил — получи репутацию.\n❌ Не выполнил — потеряешь Stars и доверие.\n\nВыбери, с чего начнёшь:",
        "choose_lang": "🌍 Выберите язык:",
        "lang_set": "✅ Язык установлен",
        "oath": "🔖 Дать клятву",
        "bet": "🎲 Заключить пари",
        "escrow": "💰 Открыть эскроу",
        "reputation": "🏅 Моя репутация",
        "how_it_works": "❓ Как это работает?",
        "how_text": "⚖️ <b>Pactum & Escrow</b> — эскроу для Telegram.\n\n🔹 <b>Клятва</b> — дай обещание перед свидетелями.\n🔹 <b>Пари</b> — спорь на Stars.\n🔹 <b>Эскроу</b> — защити сделку. Деньги в блокчейне.\n\n💎 Комиссия: 5.5% — за устранение риска.",
        "reputation_text": "🔒 Репутация станет доступна после первой сделки.",
        "soon": "🔥 Скоро! Следи за @PactumEscrow."
    },
    "en": {
        "start": "👋 <b>Hello! I’m Pactum & Escrow.</b>\n\nHere, your word = contract.\nMake an oath. Place a bet. Secure a deal.\n\n✅ Fulfilled — earn reputation.\n❌ Failed — lose Stars and trust.\n\nChoose where to start:",
        "choose_lang": "🌍 Choose language:",
        "lang_set": "✅ Language set",
        "oath": "🔖 Make an oath",
        "bet": "🎲 Place a bet",
        "escrow": "💰 Open escrow",
        "reputation": "🏅 My reputation",
        "how_it_works": "❓ How it works?",
        "how_text": "⚖️ <b>Pactum & Escrow</b> — escrow for Telegram.\n\n🔹 <b>Oath</b> — promise in front of witnesses.\n🔹 <b>Bet</b> — wager Stars.\n🔹 <b>Escrow</b> — secure your deal. Funds locked in blockchain.\n\n💎 Fee: 5.5% — for risk elimination.",
        "reputation_text": "🔒 Reputation will be available after your first deal.",
        "soon": "🔥 Coming soon! Follow @PactumEscrow."
    },
    "es": {
        "start": "👋 <b>¡Hola! Soy Pactum & Escrow.</b>\n\nAquí, tu palabra = contrato.\nHaz un juramento. Apuesta. Asegura un trato.\n\n✅ Cumplido — gana reputación.\n❌ Fallado — pierde Stars y confianza.\n\nElige por dónde empezar:",
        "choose_lang": "🌍 Elige idioma:",
        "lang_set": "✅ Idioma establecido",
        "oath": "🔖 Hacer un juramento",
        "bet": "🎲 Hacer una apuesta",
        "escrow": "💰 Abrir depósito en garantía",
        "reputation": "🏅 Mi reputación",
        "how_it_works": "❓ ¿Cómo funciona?",
        "how_text": "⚖️ <b>Pactum & Escrow</b> — depósito en garantía para Telegram.\n\n🔹 <b>Juramento</b> — promete ante testigos.\n🔹 <b>Apuesta</b> — apuesta Stars.\n🔹 <b>Depósito</b> —
