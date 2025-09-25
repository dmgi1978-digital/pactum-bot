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

# === 11 ЯЗЫКОВ ===
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
        "how_text": "⚖️ <b>Pactum & Escrow</b> — depósito en garantía para Telegram.\n\n🔹 <b>Juramento</b> — promete ante testigos.\n🔹 <b>Apuesta</b> — apuesta Stars.\n🔹 <b>Depósito</b> — asegura tu trato. Fondos bloqueados en blockchain.\n\n💎 Comisión: 5.5% — por eliminación de riesgo.",
        "reputation_text": "🔒 La reputación estará disponible tras tu primer trato.",
        "soon": "🔥 ¡Próximamente! Sigue @PactumEscrow."
    },
    "pt": {
        "start": "👋 <b>Olá! Sou o Pactum & Escrow.</b>\n\nAqui, sua palavra = contrato.\nFaça um juramento. Aposte. Garanta um negócio.\n\n✅ Cumprido — ganhe reputação.\n❌ Falhou — perca Stars e confiança.\n\nEscolha por onde começar:",
        "choose_lang": "🌍 Escolha o idioma:",
        "lang_set": "✅ Idioma definido",
        "oath": "🔖 Fazer um juramento",
        "bet": "🎲 Fazer uma aposta",
        "escrow": "💰 Abrir garantia",
        "reputation": "🏅 Minha reputação",
        "how_it_works": "❓ Como funciona?",
        "how_text": "⚖️ <b>Pactum & Escrow</b> — garantia para Telegram.\n\n🔹 <b>Juramento</b> — prometa perante testemunhas.\n🔹 <b>Aposta</b> — aposte Stars.\n🔹 <b>Garantia</b> — proteja seu negócio. Fundos travados na blockchain.\n\n💎 Taxa: 5.5% — pela eliminação de risco.",
        "reputation_text": "🔒 A reputação estará disponível após seu primeiro negócio.",
        "soon": "🔥 Em breve! Siga @PactumEscrow."
    },
    "tr": {
        "start": "👋 <b>Merhaba! Ben Pactum & Escrow.</b>\n\nBurada, sözün = sözleşme.\nYemin et. Bahis yap. İşlemi güvenceye al.\n\n✅ Yaptın — itibar kazan.\n❌ Yapmadın — Stars ve güveni kaybet.\n\nNereden başlayacağını seç:",
        "choose_lang": "🌍 Dil seçin:",
        "lang_set": "✅ Dil ayarlandı",
        "oath": "🔖 Yemin et",
        "bet": "🎲 Bahis yap",
        "escrow": "💰 Güvence aç",
        "reputation": "🏅 İtibarım",
        "how_it_works": "❓ Nasıl çalışır?",
        "how_text": "⚖️ <b>Pactum & Escrow</b> — Telegram için güvence.\n\n🔹 <b>Yemin</b> — tanıklar önünde söz ver.\n🔹 <b>Bahis</b> — Stars ile bahis yap.\n🔹 <b>Güvence</b> — işlemini koru. Fonlar blockchain'de kilitli.\n\n💎 Ücret: %5.5 — riski ortadan kaldırmak için.",
        "reputation_text": "🔒 İtibar, ilk işleminizden sonra açılacak.",
        "soon": "🔥 Yakında! @PactumEscrow'u takip et."
    },
    "fa": {
        "start": "👋 <b>سلام! من Pactum & Escrow هستم.</b>\n\nاینجا، کلمه‌ی شما = قرارداد.\nسوگند بخورید. شرط ببندید. معامله را تضمین کنید.\n\n✅ انجام شد — اعتبار کسب کنید.\n❌ انجام نشد — استارز و اعتماد را از دست بدهید.\n\nانتخاب کنید از کجا شروع کنید:",
        "choose_lang": "🌍 زبان را انتخاب کنید:",
        "lang_set": "✅ زبان تنظیم شد",
        "oath": "🔖 سوگند یاد کردن",
        "bet": "🎲 شرط بندی",
        "escrow": "💰 باز کردن تضمین",
        "reputation": "🏅 اعتبار من",
        "how_it_works": "❓ چگونه کار می‌کند؟",
        "how_text": "⚖️ <b>Pactum & Escrow</b> — تضمین برای تلگرام.\n\n🔹 <b>سوگند</b> — در برابر شاهدان قول بدهید.\n🔹 <b>شرط</b> — با استارز شرط ببندید.\n🔹 <b>تضمین</b> — معامله خود را محافظت کنید. وجوه در بلاکچین قفل شده‌اند.\n\n💎 کارمزد: ۵٫۵٪ — برای حذف ریسک.",
        "reputation_text": "🔒 اعتبار پس از اولین معامله فعال می‌شود.",
        "soon": "🔥 به زودی! @PactumEscrow را دنبال کنید."
    },
    "ar": {
        "start": "👋 <b>مرحباً! أنا Pactum & Escrow.</b>\n\nهنا، كلمتك = عقد.\nأقسم. راهن. أمّن صفقة.\n\n✅ أنجزت — اكتسب سمعة.\n❌ فشلت — افقد Stars والثقة.\n\nاختر من أين تبدأ:",
        "choose_lang": "🌍 اختر اللغة:",
        "lang_set": "✅ تم تعيين اللغة",
        "oath": "🔖 أقسم",
        "bet": "🎲 راهن",
        "escrow": "💰 افتح ضماناً",
        "reputation": "🏅 سمعتي",
        "how_it_works": "❓ كيف يعمل؟",
        "how_text": "⚖️ <b>Pactum & Escrow</b> — ضمان لـ Telegram.\n\n🔹 <b>القسم</b> — وعد أمام الشهود.\n🔹 <b>الرهان</b> — راهن بـ Stars.\n🔹 <b>الضمان</b> — أمّن صفقاتك. الأموال مقفلة في البلوك تشين.\n\n💎 العمولة: 5.5% — لإزالة المخاطر.",
        "reputation_text": "🔒 السمعة ستكون متاحة بعد أول صفقة.",
        "soon": "🔥 قريباً! تابع @PactumEscrow."
    },
    "id": {
        "start": "👋 <b>Halo! Saya Pactum & Escrow.</b>\n\nDi sini, kata-katamu = kontrak.\nBersumpah. Bertaruh. Amankan transaksi.\n\n✅ Terpenuhi — dapatkan reputasi.\n❌ Gagal — kehilangan Stars dan kepercayaan.\n\nPilih mulai dari mana:",
        "choose_lang": "🌍 Pilih bahasa:",
        "lang_set": "✅ Bahasa diatur",
        "oath": "🔖 Bersumpah",
        "bet": "🎲 Bertaruh",
        "escrow": "💰 Buka escrow",
        "reputation": "🏅 Reputasiku",
        "how_it_works": "❓ Bagaimana cara kerjanya?",
        "how_text": "⚖️ <b>Pactum & Escrow</b> — escrow untuk Telegram.\n\n🔹 <b>Sumpah</b> — berjanji di depan saksi.\n🔹 <b>Taruhan</b> — pertaruhkan Stars.\n🔹 <b>Escrow</b> — amankan transaksimu. Dana dikunci di blockchain.\n\n💎 Biaya: 5,5% — untuk menghilangkan risiko.",
        "reputation_text": "🔒 Reputasi akan tersedia setelah transaksi pertamamu.",
        "soon": "🔥 Segera hadir! Ikuti @PactumEscrow."
    },
    "fr": {
        "start": "👋 <b>Bonjour ! Je suis Pactum & Escrow.</b>\n\nIci, votre parole = contrat.\nFaites un serment. Pariez. Sécurisez une transaction.\n\n✅ Accompli — gagnez en réputation.\n❌ Échoué — perdez des Stars et la confiance.\n\nChoisissez par où commencer :",
        "choose_lang": "🌍 Choisissez la langue :",
        "lang_set": "✅ Langue définie",
        "oath": "🔖 Faire un serment",
        "bet": "🎲 Parier",
        "escrow": "💰 Ouvrir un dépôt de garantie",
        "reputation": "🏅 Ma réputation",
        "how_it_works": "❓ Comment ça marche ?",
        "how_text": "⚖️ <b>Pactum & Escrow</b> — dépôt de garantie pour Telegram.\n\n🔹 <b>Serment</b> — promettez devant témoins.\n🔹 <b>Pari</b> — misez des Stars.\n🔹 <b>Dépôt</b> — sécurisez votre transaction. Fonds bloqués sur la blockchain.\n\n💎 Frais : 5,5 % — pour éliminer les risques.",
        "reputation_text": "🔒 La réputation sera disponible après votre première transaction.",
        "soon": "🔥 Bientôt ! Suivez @PactumEscrow."
    },
    "de": {
        "start": "👋 <b>Hallo! Ich bin Pactum & Escrow.</b>\n\nHier gilt: Dein Wort = Vertrag.\nSchwöre einen Eid. Wette. Sichere einen Deal.\n\n✅ Erfüllt — erhalte Reputation.\n❌ Verfehlt — verliere Stars und Vertrauen.\n\nWähle, wo du beginnen möchtest:",
        "choose_lang": "🌍 Wähle Sprache:",
        "lang_set": "✅ Sprache eingestellt",
        "oath": "🔖 Einen Eid schwören",
        "bet": "🎲 Wetten",
        "escrow": "💰 Escrow eröffnen",
        "reputation": "🏅 Meine Reputation",
        "how_it_works": "❓ Wie funktioniert es?",
        "how_text": "⚖️ <b>Pactum & Escrow</b> — Escrow für Telegram.\n\n🔹 <b>Eid</b> — verspreche vor Zeugen.\n🔹 <b>Wette</b> — setze Stars.\n🔹 <b>Escrow</b> — sichere deinen Deal. Gelder sind in der Blockchain gesperrt.\n\n💎 Gebühr: 5,5 % — zur Risikobeseitigung.",
        "reputation_text": "🔒 Reputation wird nach deinem ersten Deal freigeschaltet.",
        "soon": "🔥 Bald verfügbar! Folge @PactumEscrow."
    },
    "zh": {
        "start": "👋 <b>你好！我是 Pactum & Escrow。</b>\n\n在这里，你的话 = 合同。\n立下誓言。下注。保障交易。\n\n✅ 完成 — 获得信誉。\n❌ 失败 — 失去 Stars 和信任。\n\n选择从哪里开始：",
        "choose_lang": "🌍 选择语言：",
        "lang_set": "✅ 语言已设置",
        "oath": "🔖 立下誓言",
        "bet": "🎲 下注",
        "escrow": "💰 开启托管",
        "reputation": "🏅 我的信誉",
        "how_it_works": "❓ 如何运作？",
        "how_text": "⚖️ <b>Pactum & Escrow</b> — Telegram 托管服务。\n\n🔹 <b>誓言</b> — 在见证人面前承诺。\n🔹 <b>下注</b> — 用 Stars 下注。\n🔹 <b>托管</b> — 保障你的交易。资金锁定在区块链中。\n\n💎 费用：5.5% — 用于消除风险。",
        "reputation_text": "🔒 首次交易后即可查看信誉。",
        "soon": "🔥 即将推出！关注 @PactumEscrow。"
    }
}

# === СОСТОЯНИЕ ===
class UserState(StatesGroup):
    choosing_language = State()

# === КЛАВИАТУРА ЯЗЫКОВ ===
def get_lang_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")],
            [KeyboardButton(text="🇪🇸 Español"), KeyboardButton(text="🇵🇹 Português")],
            [KeyboardButton(text="🇹🇷 Türkçe"), KeyboardButton(text="🇮🇷 فارسی")],
            [KeyboardButton(text="🇸🇦 العربية"), KeyboardButton(text="🇮🇩 Bahasa")],
            [KeyboardButton(text="🇫🇷 Français"), KeyboardButton(text="🇩🇪 Deutsch")],
            [KeyboardButton(text="🇨🇳 中文")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

# === ГЛАВНОЕ МЕНЮ ===
def get_main_menu(lang: str):
    t = TEXTS.get(lang, TEXTS["en"])
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t["oath"]),
                KeyboardButton(text=t["bet"])
            ],
            [
                KeyboardButton(text=t["escrow"])
            ],
            [
                KeyboardButton(text=t["reputation"]),
                KeyboardButton(text=t["how_it_works"])
            ]
        ],
        resize_keyboard=True
    )

# === /start ===
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(UserState.choosing_language)
    # Используем английский как fallback для выбора
    await message.answer("🌍 Choose language / Выберите язык:", reply_markup=get_lang_keyboard())

# === ВЫБОР ЯЗЫКА ===
@dp.message(UserState.choosing_language)
async def lang_chosen(message: types.Message, state: FSMContext):
    text = message.text
    lang_map = {
        "🇷🇺 Русский": "ru",
        "🇬🇧 English": "en",
        "🇪🇸 Español": "es",
        "🇵🇹 Português": "pt",
        "🇹🇷 Türkçe": "tr",
        "🇮🇷 فارسی": "fa",
        "🇸🇦 العربية": "ar",
        "🇮🇩 Bahasa": "id",
        "🇫🇷 Français": "fr",
        "🇩🇪 Deutsch": "de",
        "🇨🇳 中文": "zh"
    }
    
    lang = lang_map.get(text)
    if lang:
        await state.update_data(lang=lang)
        await state.set_state(None)
        t = TEXTS[lang]
        await message.answer(f"{t['lang_set']} ({text})")
        await message.answer(t["start"], reply_markup=get_main_menu(lang), parse_mode="HTML")
    else:
        await message.answer("🌍 Choose language / Выберите язык:", reply_markup=get_lang_keyboard())

# === ОБРАБОТКА КНОПОК ===
@dp.message(lambda msg: True)
async def handle_buttons(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "en")
    t = TEXTS.get(lang, TEXTS["en"])

    if message.text == t["how_it_works"]:
        await message.answer(t["how_text"], parse_mode="HTML")
    elif message.text == t["reputation"]:
        await message.answer(t["reputation_text"])
    elif message.text in [t["oath"], t["bet"], t["escrow"]]:
        await message.answer(t["soon"])
    else:
        await cmd_start(message, state)

# === ЗАПУСК ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
