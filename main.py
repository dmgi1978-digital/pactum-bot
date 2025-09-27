import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# === БЕЗОПАСНОСТЬ: токен из переменной окружения ===
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN must be set in Render Environment Variables!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# === СОСТОЯНИЯ ПОЛЬЗОВАТЕЛЯ ===
class UserState(StatesGroup):
    choosing_language = State()
    escrow_amount = State()

# === ТЕКСТЫ НА 20 ЯЗЫКАХ ===
TEXTS = {
    "en": {"start": "👋 <b>Hello! I’m Pactum & Escrow.</b>\n\nYour word is a smart contract on <b>TON</b>.\nMake an oath • Place a bet • Secure a deal\n\n✅ Fulfilled — earn reputation\n❌ Broken — lose <b>Stars, TON, USDT</b> and trust\n\nChoose:", "oath": "🔖 Oath", "bet": "🎲 Bet", "escrow": "💰 Escrow", "reputation": "🏅 Reputation", "how_btn": "❓ How it works", "lang_set": "✅ Language: English"},
    "ru": {"start": "👋 <b>Привет! Я — Pactum & Escrow.</b>\n\nТвоё слово — смарт-контракт в <b>TON</b>.\nДай клятву • Заключи пари • Защити сделку\n\n✅ Выполнил — получи репутацию\n❌ Нарушил — потеряешь <b>Stars, TON, USDT</b> и доверие\n\nВыбери:", "oath": "🔖 Клятва", "bet": "🎲 Пари", "escrow": "💰 Эскроу", "reputation": "🏅 Репутация", "how_btn": "❓ Как работает", "lang_set": "✅ Язык: Русский"},
    "es": {"start": "👋 <b>¡Hola! Soy Pactum & Escrow.</b>\n\nTu palabra es un smart contract en <b>TON</b>.\nHaz un juramento • Apuesta • Asegura un trato\n\n✅ Cumplido — gana reputación\n❌ Roto — pierde <b>Stars, TON, USDT</b> y confianza\n\nElige:", "oath": "🔖 Juramento", "bet": "🎲 Apuesta", "escrow": "💰 Depósito", "reputation": "🏅 Reputación", "how_btn": "❓ ¿Cómo funciona?", "lang_set": "✅ Idioma: Español"},
    "pt": {"start": "👋 <b>Olá! Sou o Pactum & Escrow.</b>\n\nSua palavra é um smart contract na <b>TON</b>.\nFaça um juramento • Aposte • Garanta um negócio\n\n✅ Cumprido — ganhe reputação\n❌ Quebrado — perca <b>Stars, TON, USDT</b> e confiança\n\nEscolha:", "oath": "🔖 Juramento", "bet": "🎲 Aposta", "escrow": "💰 Garantia", "reputation": "🏅 Reputação", "how_btn": "❓ Como funciona?", "lang_set": "✅ Idioma: Português"},
    "tr": {"start": "👋 <b>Merhaba! Ben Pactum & Escrow.</b>\n\nSözün, <b>TON</b> üzerinde bir akıllı kontrattır.\nYemin et • Bahis yap • İşlemi güvenceye al\n\n✅ Yaptın — itibar kazan\n❌ Bozdun — <b>Stars, TON, USDT</b> ve güveni kaybet\n\nSeç:", "oath": "🔖 Yemin", "bet": "🎲 Bahis", "escrow": "💰 Güvence", "reputation": "🏅 İtibar", "how_btn": "❓ Nasıl çalışır?", "lang_set": "✅ Dil: Türkçe"},
    "fa": {"start": "👋 <b>سلام! من Pactum & Escrow هستم.</b>\n\nکلمه‌ی شما یک قرارداد هوشمند در <b>TON</b> است.\nسوگند بخور • شرط ببند • معامله را تضمین کن\n\n✅ انجام شد — اعتبار کسب کن\n❌ شکسته شد — <b>استارز، TON، USDT</b> و اعتماد را از دست بده\n\nانتخاب کن:", "oath": "🔖 سوگند", "bet": "🎲 شرط", "escrow": "💰 تضمین", "reputation": "🏅 اعتبار", "how_btn": "❓ چگونه کار می‌کند؟", "lang_set": "✅ زبان: فارسی"},
    "ar": {"start": "👋 <b>مرحباً! أنا Pactum & Escrow.</b>\n\nكلمتك عقد ذكي على <b>TON</b>.\nأقسم • راهن • أمّن صفقة\n\n✅ أنجزت — اكتسب سمعة\n❌ خالفت — افقد <b>Stars و TON و USDT</b> والثقة\n\nاختر:", "oath": "🔖 قسم", "bet": "🎲 رهان", "escrow": "💰 ضمان", "reputation": "🏅 سمعة", "how_btn": "❓ كيف يعمل؟", "lang_set": "✅ اللغة: العربية"},
    "id": {"start": "👋 <b>Halo! Saya Pactum & Escrow.</b>\n\nKata-katamu adalah smart contract di <b>TON</b>.\nBersumpah • Bertaruh • Amankan transaksi\n\n✅ Dipenuhi — dapatkan reputasi\n❌ Dilanggar — kehilangan <b>Stars, TON, USDT</b> dan kepercayaan\n\nPilih:", "oath": "🔖 Sumpah", "bet": "🎲 Taruhan", "escrow": "💰 Escrow", "reputation": "🏅 Reputasi", "how_btn": "❓ Bagaimana cara kerjanya?", "lang_set": "✅ Bahasa: Indonesia"},
    "fr": {"start": "👋 <b>Bonjour ! Je suis Pactum & Escrow.</b>\n\nVotre parole est un smart contract sur <b>TON</b>.\nFaites un serment • Pariez • Sécurisez une transaction\n\n✅ Accompli — gagnez en réputation\n❌ Rompu — perdez <b>Stars, TON, USDT</b> et la confiance\n\nChoisissez :", "oath": "🔖 Serment", "bet": "🎲 Pari", "escrow": "💰 Dépôt", "reputation": "🏅 Réputation", "how_btn": "❓ Comment ça marche ?", "lang_set": "✅ Langue : Français"},
    "de": {"start": "👋 <b>Hallo! Ich bin Pactum & Escrow.</b>\n\nDein Wort ist ein Smart Contract auf <b>TON</b>.\nSchwöre einen Eid • Wette • Sichere einen Deal\n\n✅ Erfüllt — erhalte Reputation\n❌ Gebrochen — verliere <b>Stars, TON, USDT</b> und Vertrauen\n\nWähle:", "oath": "🔖 Eid", "bet": "🎲 Wette", "escrow": "💰 Escrow", "reputation": "🏅 Reputation", "how_btn": "❓ Wie funktioniert es?", "lang_set": "✅ Sprache: Deutsch"},
    "zh": {"start": "👋 <b>你好！我是 Pactum & Escrow。</b>\n\n你的话是 <b>TON</b> 上的智能合约。\n立下誓言 • 下注 • 保障交易\n\n✅ 完成 — 获得信誉\n❌ 违背 — 失去 <b>Stars、TON、USDT</b> 和信任\n\n选择：", "oath": "🔖 誓言", "bet": "🎲 下注", "escrow": "💰 托管", "reputation": "🏅 信誉", "how_btn": "❓ 如何运作？", "lang_set": "✅ 语言：中文"},
    "ko": {"start": "👋 <b>안녕하세요! 저는 Pactum & Escrow입니다.</b>\n\n당신의 말은 <b>TON</b>의 스마트 계약입니다.\n서약 • 베팅 • 거래 보호\n\n✅ 이행 — 평판 획득\n❌ 위반 — <b>Stars, TON, USDT</b> 및 신뢰 상실\n\n선택하세요:", "oath": "🔖 서약", "bet": "🎲 베팅", "escrow": "💰 에스크로", "reputation": "🏅 평판", "how_btn": "❓ 어떻게 작동하나요?", "lang_set": "✅ 언어: 한국어"},
    "hi": {"start": "👋 <b>नमस्ते! मैं Pactum & Escrow हूँ।</b>\n\nआपका वचन <b>TON</b> पर एक स्मार्ट अनुबंध है।\nशपथ लें • दांव लगाएं • लेन-देन सुरक्षित करें\n\n✅ पूर्ण — प्रतिष्ठा अर्जित करें\n❌ टूटा — <b>Stars, TON, USDT</b> और भरोसा खोएं\n\nचुनें:", "oath": "🔖 शपथ", "bet": "🎲 दांव", "escrow": "💰 एस्क्रो", "reputation": "🏅 प्रतिष्ठा", "how_btn": "❓ यह कैसे काम करता है?", "lang_set": "✅ भाषा: हिंदी"},
    "vi": {"start": "👋 <b>Xin chào! Tôi là Pactum & Escrow.</b>\n\nLời bạn nói là hợp đồng thông minh trên <b>TON</b>.\nThề • Đặt cược • Bảo vệ giao dịch\n\n✅ Hoàn thành — nhận uy tín\n❌ Vi phạm — mất <b>Stars, TON, USDT</b> và niềm tin\n\nChọn:", "oath": "🔖 Lời thề", "bet": "🎲 Cược", "escrow": "💰 Ký quỹ", "reputation": "🏅 Uy tín", "how_btn": "❓ Cách hoạt động?", "lang_set": "✅ Ngôn ngữ: Tiếng Việt"},
    "th": {"start": "👋 <b>สวัสดี! ฉันคือ Pactum & Escrow</b>\n\nคำพูดของคุณคือสัญญาอัจฉริยะบน <b>TON</b>\nให้คำสาบาน • เดิมพัน • รักษาธุรกรรม\n\n✅ ทำสำเร็จ — ได้ชื่อเสียง\n❌ ผิดคำ — สูญเสีย <b>Stars, TON, USDT</b> และความไว้วางใจ\n\nเลือก:", "oath": "🔖 คำสาบาน", "bet": "🎲 เดิมพัน", "escrow": "💰 เอครอว์", "reputation": "🏅 ชื่อเสียง", "how_btn": "❓ ทำงานอย่างไร?", "lang_set": "✅ ภาษา: ไทย"},
    "uk": {"start": "👋 <b>Привіт! Я — Pactum & Escrow.</b>\n\nТвоє слово — смарт-контракт у <b>TON</b>.\nДай клятву • Заключи парі • Захисти угоду\n\n✅ Виконано — отримай репутацію\n❌ Порушено — втратиш <b>Stars, TON, USDT</b> і довіру\n\nОбери:", "oath": "🔖 Клятва", "bet": "🎲 Парі", "escrow": "💰 Ескроу", "reputation": "🏅 Репутація", "how_btn": "❓ Як це працює?", "lang_set": "✅ Мова: Українська"},
    "pl": {"start": "👋 <b>Cześć! Jestem Pactum & Escrow.</b>\n\nTwoje słowo to smart contract w <b>TON</b>.\nZłóż przysięgę • Zakład • Zabezpiecz transakcję\n\n✅ Spełnione — zdobyj reputację\n❌ Złamane — strać <b>Stars, TON, USDT</b> i zaufanie\n\nWybierz:", "oath": "🔖 Przysięga", "bet": "🎲 Zakład", "escrow": "💰 Depozyt", "reputation": "🏅 Reputacja", "how_btn": "❓ Jak to działa?", "lang_set": "✅ Język: Polski"},
    "it": {"start": "👋 <b>Ciao! Sono Pactum & Escrow.</b>\n\nLa tua parola è uno smart contract su <b>TON</b>.\nFai un giuramento • Scommetti • Sicurizza un affare\n\n✅ Rispettato — guadagna reputazione\n❌ Violato — perdi <b>Stars, TON, USDT</b> e fiducia\n\nScegli:", "oath": "🔖 Giuramento", "bet": "🎲 Scommessa", "escrow": "💰 Escrow", "reputation": "🏅 Reputazione", "how_btn": "❓ Come funziona?", "lang_set": "✅ Lingua: Italiano"},
    "nl": {"start": "👋 <b>Hallo! Ik ben Pactum & Escrow.</b>\n\nJe woord is een smart contract op <b>TON</b>.\nZweer een eed • Wed • Beveilig een deal\n\n✅ Nagekomen — verdien reputatie\n❌ Gebroken — verlies <b>Stars, TON, USDT</b> en vertrouwen\n\nKies:", "oath": "🔖 Eed", "bet": "🎲 Weddenschap", "escrow": "💰 Escrow", "reputation": "🏅 Reputatie", "how_btn": "❓ Hoe werkt het?", "lang_set": "✅ Taal: Nederlands"},
    "ja": {"start": "👋 <b>こんにちは！Pactum & Escrowです。</b>\n\nあなたの言葉は<b>TON</b>上のスマートコントラクトです。\n誓い • 賭け • 取引を保護\n\n✅ 達成 — 評判を獲得\n❌ 違反 — <b>Stars、TON、USDT</b>と信頼を失う\n\n選択してください:", "oath": "🔖 誓い", "bet": "🎲 賭け", "escrow": "💰 エスクロー", "reputation": "🏅 評判", "how_btn": "❓ 仕組みは？", "lang_set": "✅ 言語: 日本語"}
}

# === КЛАВИАТУРЫ ===
def get_lang_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇬🇧 English"), KeyboardButton(text="🇷🇺 Русский")],
            [KeyboardButton(text="🇪🇸 Español"), KeyboardButton(text="🇵🇹 Português")],
            [KeyboardButton(text="🇹🇷 Türkçe"), KeyboardButton(text="🇮🇷 فارسی")],
            [KeyboardButton(text="🇸🇦 العربية"), KeyboardButton(text="🇮🇩 Bahasa")],
            [KeyboardButton(text="🇫🇷 Français"), KeyboardButton(text="🇩🇪 Deutsch")],
            [KeyboardButton(text="🇨🇳 中文"), KeyboardButton(text="🇰🇷 한국어")],
            [KeyboardButton(text="🇮🇳 हिंदी"), KeyboardButton(text="🇻🇳 Tiếng Việt")],
            [KeyboardButton(text="🇹🇭 ไทย"), KeyboardButton(text="🇺🇦 Українська")],
            [KeyboardButton(text="🇵🇱 Polski"), KeyboardButton(text="🇮🇹 Italiano")],
            [KeyboardButton(text="🇳🇱 Nederlands"), KeyboardButton(text="🇯🇵 日本語")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_main_menu(lang_code):
    t = TEXTS[lang_code]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t["oath"]), KeyboardButton(text=t["bet"])],
            [KeyboardButton(text=t["escrow"])],
            [KeyboardButton(text=t["reputation"]), KeyboardButton(text=t["how_btn"])]
        ],
        resize_keyboard=True
    )
    # === /start ===
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(UserState.choosing_language)
    await message.answer("🌍 Choose language / Выберите язык:", reply_markup=get_lang_keyboard())

# === ВЫБОР ЯЗЫКА ===
@dp.message(UserState.choosing_language)
async def lang_chosen(message: types.Message, state: FSMContext):
    lang_map = {
        "🇬🇧 English": "en", "🇷🇺 Русский": "ru", "🇪🇸 Español": "es", "🇵🇹 Português": "pt",
        "🇹🇷 Türkçe": "tr", "🇮🇷 فارسی": "fa", "🇸🇦 العربية": "ar", "🇮🇩 Bahasa": "id",
        "🇫🇷 Français": "fr", "🇩🇪 Deutsch": "de", "🇨🇳 中文": "zh", "🇰🇷 한국어": "ko",
        "🇮🇳 हिंदी": "hi", "🇻🇳 Tiếng Việt": "vi", "🇹🇭 ไทย": "th", "🇺🇦 Українська": "uk",
        "🇵🇱 Polski": "pl", "🇮🇹 Italiano": "it", "🇳🇱 Nederlands": "nl", "🇯🇵 日本語": "ja"
    }
    lang = lang_map.get(message.text)
    if lang:
        await state.update_data(lang=lang)
        await state.set_state(None)
        t = TEXTS[lang]
        await message.answer(t["lang_set"])
        await message.answer(t["start"], reply_markup=get_main_menu(lang), parse_mode="HTML")
    else:
        await message.answer("🌍 Choose language / Выберите язык:", reply_markup=get_lang_keyboard())

# === ОБРАБОТКА КНОПОК ===
@dp.message(lambda msg: True)
async def handle_buttons(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    if lang not in TEXTS:
        lang = "en"
    t = TEXTS[lang]

    if message.text == t["escrow"]:
        await state.set_state(UserState.escrow_amount)
        await message.answer("💰 Enter amount in Stars (min 10):")
    elif message.text in [t["oath"], t["bet"], t["reputation"], t["how_btn"]]:
        await message.answer("🔥 Coming soon! Follow @PactumEscrow")
    else:
        await cmd_start(message, state)

# === ПРИЁМ СУММЫ И ОТПРАВКА ИНВОЙСА В STARS ===
@dp.message(UserState.escrow_amount)
async def escrow_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text.strip())
        if amount < 10:
            await message.answer("❌ Minimum: 10 Stars")
            return
    except:
        await message.answer("❌ Enter a number (e.g. 100)")
        return

    commission = int(amount * 0.055)
    total = amount + commission

    try:
        await bot.send_invoice(
            chat_id=message.chat.id,
            title="Pactum & Escrow",
            description=f"Deal protection: {amount} ⭐ + fee {commission} ⭐",
            payload="escrow_deal",
            provider_token="",      # ← ОБЯЗАТЕЛЬНО ПУСТОЙ
            currency="XTR",         # ← ОФИЦИАЛЬНЫЙ КОД STARS
            prices=[LabeledPrice(label="Total", amount=total)],
            start_parameter="escrow"
        )
        await state.clear()
    except Exception as e:
        await message.answer(f"❌ Error: {str(e)}")

# === ОБРАБОТКА ОПЛАТЫ ===
@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message(lambda msg: msg.successful_payment)
async def success_payment(message: types.Message):
    total = message.successful_payment.total_amount
    await message.answer(f"✅ Paid {total} Stars! Escrow is active.")

# === ЗАПУСК ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
