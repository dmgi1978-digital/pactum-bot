import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# === НАСТРОЙКИ ===
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN must be set in Render Environment Variables!")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# === СОСТОЯНИЯ ===
class UserState(StatesGroup):
    choosing_language = State()
    escrow_amount = State()

# === ТЕКСТЫ НА 20 ЯЗЫКАХ ===
LANG_DATA = {
    "en": {"btn": "💰 Open Escrow", "start": "👋 <b>Pactum & Escrow</b>\n\nYour word = smart contract on <b>TON</b>.\nOpen escrow to protect your deal.\n\nFee: 5.5% in Stars.", "prompt": "💰 Enter amount in Stars (min 10):", "min_err": "❌ Minimum: 10 Stars", "num_err": "❌ Enter a number", "paid": "✅ Paid {total} Stars! Escrow is active."},
    "ru": {"btn": "💰 Открыть эскроу", "start": "👋 <b>Pactum & Escrow</b>\n\nТвоё слово = смарт-контракт в <b>TON</b>.\nОткрой эскроу для защиты сделки.\n\nКомиссия: 5.5% в Stars.", "prompt": "💰 Введите сумму в Stars (минимум 10):", "min_err": "❌ Минимум: 10 Stars", "num_err": "❌ Введите число", "paid": "✅ Оплачено {total} Stars! Эскроу активен."},
    "es": {"btn": "💰 Abrir depósito", "start": "👋 <b>Pactum & Escrow</b>\n\nTu palabra = contrato inteligente en <b>TON</b>.\nAbre un depósito para proteger tu trato.\n\nComisión: 5.5% en Stars.", "prompt": "💰 Ingresa monto en Stars (mínimo 10):", "min_err": "❌ Mínimo: 10 Stars", "num_err": "❌ Ingresa un número", "paid": "✅ Pagado {total} Stars! Depósito activo."},
    "pt": {"btn": "💰 Abrir garantia", "start": "👋 <b>Pactum & Escrow</b>\n\nSua palavra = contrato inteligente na <b>TON</b>.\nAbra uma garantia para proteger seu negócio.\n\nTaxa: 5,5% em Stars.", "prompt": "💰 Digite valor em Stars (mínimo 10):", "min_err": "❌ Mínimo: 10 Stars", "num_err": "❌ Digite um número", "paid": "✅ Pago {total} Stars! Garantia ativa."},
    "tr": {"btn": "💰 Güvence aç", "start": "👋 <b>Pactum & Escrow</b>\n\nSözün = <b>TON</b> üzerinde akıllı kontrat.\nİşlemini korumak için güvence aç.\n\nÜcret: Stars'ta %5,5.", "prompt": "💰 Stars cinsinden tutar girin (en az 10):", "min_err": "❌ Minimum: 10 Stars", "num_err": "❌ Bir sayı girin", "paid": "✅ {total} Stars ödendi! Güvence aktif."},
    "fa": {"btn": "💰 باز کردن تضمین", "start": "👋 <b>Pactum & Escrow</b>\n\nکلمه‌ی شما = قرارداد هوشمند در <b>TON</b>.\nبرای محافظت از معامله، تضمین باز کنید.\n\nکارمزد: ۵٫۵٪ به استارز.", "prompt": "💰 مبلغ را به استارز وارد کنید (حداقل ۱۰):", "min_err": "❌ حداقل: ۱۰ استارز", "num_err": "❌ یک عدد وارد کنید", "paid": "✅ {total} استارز پرداخت شد! تضمین فعال است."},
    "ar": {"btn": "💰 فتح الضمان", "start": "👋 <b>Pactum & Escrow</b>\n\nكلمتك = عقد ذكي على <b>TON</b>.\nافتح ضمانًا لحماية صفقاتك.\n\nالعمولة: 5.5% بالـ Stars.", "prompt": "💰 أدخل المبلغ بالـ Stars (الحد الأدنى 10):", "min_err": "❌ الحد الأدنى: 10 Stars", "num_err": "❌ أدخل رقماً", "paid": "✅ دُفع {total} Stars! الضمان نشط."},
    "id": {"btn": "💰 Buka escrow", "start": "👋 <b>Pactum & Escrow</b>\n\nKata-katamu = kontrak pintar di <b>TON</b>.\nBuka escrow untuk lindungi transaksimu.\n\nBiaya: 5,5% dalam Stars.", "prompt": "💰 Masukkan jumlah dalam Stars (min 10):", "min_err": "❌ Minimum: 10 Stars", "num_err": "❌ Masukkan angka", "paid": "✅ Dibayar {total} Stars! Escrow aktif."},
    "fr": {"btn": "💰 Ouvrir un dépôt", "start": "👋 <b>Pactum & Escrow</b>\n\nVotre parole = contrat intelligent sur <b>TON</b>.\nOuvrez un dépôt pour sécuriser votre transaction.\n\nFrais : 5,5 % en Stars.", "prompt": "💰 Entrez le montant en Stars (min 10) :", "min_err": "❌ Minimum : 10 Stars", "num_err": "❌ Entrez un nombre", "paid": "✅ Payé {total} Stars ! Dépôt actif."},
    "de": {"btn": "💰 Escrow öffnen", "start": "👋 <b>Pactum & Escrow</b>\n\nDein Wort = Smart Contract auf <b>TON</b>.\nÖffne Escrow, um deinen Deal zu schützen.\n\nGebühr: 5,5 % in Stars.", "prompt": "💰 Betrag in Stars eingeben (mind. 10):", "min_err": "❌ Mindestens: 10 Stars", "num_err": "❌ Gib eine Zahl ein", "paid": "✅ {total} Stars bezahlt! Escrow aktiv."},
    "zh": {"btn": "💰 开启托管", "start": "👋 <b>Pactum & Escrow</b>\n\n你的话 = <b>TON</b> 上的智能合约。\n开启托管以保护你的交易。\n\n费用：5.5% Stars。", "prompt": "💰 输入 Stars 数量（最少 10）：", "min_err": "❌ 最少：10 Stars", "num_err": "❌ 输入数字", "paid": "✅ 已支付 {total} Stars！托管已激活。"},
    "ko": {"btn": "💰 에스크로 열기", "start": "👋 <b>Pactum & Escrow</b>\n\n당신의 말 = <b>TON</b>의 스마트 계약입니다.\n거래를 보호하려면 에스크로를 여세요.\n\n수수료: Stars 5.5%.", "prompt": "💰 Stars 금액 입력 (최소 10):", "min_err": "❌ 최소: 10 Stars", "num_err": "❌ 숫자를 입력하세요", "paid": "✅ {total} Stars 지불됨! 에스크로 활성화."},
    "hi": {"btn": "💰 एस्क्रो खोलें", "start": "👋 <b>Pactum & Escrow</b>\n\nआपका वचन = <b>TON</b> पर स्मार्ट अनुबंध।\nअपने लेन-देन की सुरक्षा के लिए एस्क्रो खोलें।\n\nशुल्क: Stars में 5.5%।", "prompt": "💰 Stars में राशि दर्ज करें (न्यूनतम 10):", "min_err": "❌ न्यूनतम: 10 Stars", "num_err": "❌ एक संख्या दर्ज करें", "paid": "✅ {total} Stars का भुगतान किया गया! एस्क्रो सक्रिय है।"},
    "vi": {"btn": "💰 Mở ký quỹ", "start": "👋 <b>Pactum & Escrow</b>\n\nLời bạn = hợp đồng thông minh trên <b>TON</b>.\nMở ký quỹ để bảo vệ giao dịch.\n\nPhí: 5,5% bằng Stars.", "prompt": "💰 Nhập số Stars (tối thiểu 10):", "min_err": "❌ Tối thiểu: 10 Stars", "num_err": "❌ Nhập một số", "paid": "✅ Đã thanh toán {total} Stars! Ký quỹ đang hoạt động."},
    "th": {"btn": "💰 เปิดเอครอว์", "start": "👋 <b>Pactum & Escrow</b>\n\nคำพูดคุณ = สัญญาอัจฉริยะบน <b>TON</b>\nเปิดเอครอว์เพื่อป้องกันธุรกรรม\n\nค่าธรรมเนียม: 5.5% ใน Stars", "prompt": "💰 ใส่จำนวน Stars (ขั้นต่ำ 10):", "min_err": "❌ ขั้นต่ำ: 10 Stars", "num_err": "❌ ใส่ตัวเลข", "paid": "✅ ชำระแล้ว {total} Stars! เอครอว์เปิดใช้งาน"},
    "uk": {"btn": "💰 Відкрити ескроу", "start": "👋 <b>Pactum & Escrow</b>\n\nТвоє слово = смарт-контракт у <b>TON</b>.\nВідкрий ескроу для захисту угоди.\n\nКомісія: 5.5% у Stars.", "prompt": "💰 Введіть суму в Stars (мінімум 10):", "min_err": "❌ Мінімум: 10 Stars", "num_err": "❌ Введіть число", "paid": "✅ Сплачено {total} Stars! Ескроу активний."},
    "pl": {"btn": "💰 Otwórz depozyt", "start": "👋 <b>Pactum & Escrow</b>\n\nTwoje słowo = smart contract w <b>TON</b>.\nOtwórz depozyt, aby zabezpieczyć transakcję.\n\nProwizja: 5,5% w Stars.", "prompt": "💰 Wprowadź kwotę w Stars (min 10):", "min_err": "❌ Minimum: 10 Stars", "num_err": "❌ Wprowadź liczbę", "paid": "✅ Zapłacono {total} Stars! Depozyt aktywny."},
    "it": {"btn": "💰 Apri escrow", "start": "👋 <b>Pactum & Escrow</b>\n\nLa tua parola = smart contract su <b>TON</b>.\nApri escrow per proteggere il tuo affare.\n\nCommissione: 5,5% in Stars.", "prompt": "💰 Inserisci importo in Stars (min 10):", "min_err": "❌ Minimo: 10 Stars", "num_err": "❌ Inserisci un numero", "paid": "✅ Pagato {total} Stars! Escrow attivo."},
    "nl": {"btn": "💰 Open escrow", "start": "👋 <b>Pactum & Escrow</b>\n\nJouw woord = smart contract op <b>TON</b>.\nOpen escrow om je deal te beschermen.\n\nVergoeding: 5,5% in Stars.", "prompt": "💰 Voer bedrag in Stars in (min 10):", "min_err": "❌ Minimum: 10 Stars", "num_err": "❌ Voer een getal in", "paid": "✅ Betaald {total} Stars! Escrow actief."},
    "ja": {"btn": "💰 エスクローを開く", "start": "👋 <b>Pactum & Escrow</b>\n\nあなたの言葉 = <b>TON</b>上のスマートコントラクト。\n取引を保護するにはエスクローを開いてください。\n\n手数料: Starsで5.5%。", "prompt": "💰 Starsの金額を入力してください（最低10）:", "min_err": "❌ 最低: 10 Stars", "num_err": "❌ 数字を入力してください", "paid": "✅ {total} Starsを支払いました！エスクローが有効です。"}
}

# === КЛАВИАТУРА ВЫБОРА ЯЗЫКА ===
def get_lang_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇬🇧 EN"), KeyboardButton(text="🇷🇺 RU")],
            [KeyboardButton(text="🇪🇸 ES"), KeyboardButton(text="🇵🇹 PT")],
            [KeyboardButton(text="🇹🇷 TR"), KeyboardButton(text="🇮🇷 FA")],
            [KeyboardButton(text="🇸🇦 AR"), KeyboardButton(text="🇮🇩 ID")],
            [KeyboardButton(text="🇫🇷 FR"), KeyboardButton(text="🇩🇪 DE")],
            [KeyboardButton(text="🇨🇳 ZH"), KeyboardButton(text="🇰🇷 KO")],
            [KeyboardButton(text="🇮🇳 HI"), KeyboardButton(text="🇻🇳 VI")],
            [KeyboardButton(text="🇹🇭 TH"), KeyboardButton(text="🇺🇦 UA")],
            [KeyboardButton(text="🇵🇱 PL"), KeyboardButton(text="🇮🇹 IT")],
            [KeyboardButton(text="🇳🇱 NL"), KeyboardButton(text="🇯🇵 JA")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

# === СООТВЕТСТВИЕ КНОПОК ЯЗЫКАМ ===
LANG_MAP = {
    "🇬🇧 EN": "en", "🇷🇺 RU": "ru", "🇪🇸 ES": "es", "🇵🇹 PT": "pt",
    "🇹🇷 TR": "tr", "🇮🇷 FA": "fa", "🇸🇦 AR": "ar", "🇮🇩 ID": "id",
    "🇫🇷 FR": "fr", "🇩🇪 DE": "de", "🇨🇳 ZH": "zh", "🇰🇷 KO": "ko",
    "🇮🇳 HI": "hi", "🇻🇳 VI": "vi", "🇹🇭 TH": "th", "🇺🇦 UA": "uk",
    "🇵🇱 PL": "pl", "🇮🇹 IT": "it", "🇳🇱 NL": "nl", "🇯🇵 JA": "ja"
}

# === /start ===
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(UserState.choosing_language)
    await message.answer("🌍 Choose language:", reply_markup=get_lang_keyboard())

# === ВЫБОР ЯЗЫКА ===
@dp.message(UserState.choosing_language)
async def choose_lang(message: types.Message, state: FSMContext):
    lang_code = LANG_MAP.get(message.text)
    if lang_code:
        await state.update_data(lang=lang_code)
        await state.set_state(None)
        data = LANG_DATA[lang_code]
        menu = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=data["btn"])]],
            resize_keyboard=True
        )
        await message.answer(data["start"], reply_markup=menu, parse_mode="HTML")
    else:
        await message.answer("🌍 Choose language:", reply_markup=get_lang_keyboard())

# === ОБРАБОТКА КНОПКИ ЭСКРОУ ===
@dp.message(lambda msg: any(msg.text == LANG_DATA[lang]["btn"] for lang in LANG_DATA))
async def escrow_button(message: types.Message, state: FSMContext):
    # Определяем язык по тексту кнопки
    lang_code = None
    for lang, data in LANG_DATA.items():
        if message.text == data["btn"]:
            lang_code = lang
            break
    if not lang_code:
        lang_code = "en"
    
    await state.update_data(lang=lang_code)
    await state.set_state(UserState.escrow_amount)
    await message.answer(LANG_DATA[lang_code]["prompt"])

# === ПРИЁМ СУММЫ И ОТПРАВКА ИНВОЙСА ===
@dp.message(UserState.escrow_amount)
async def process_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang_code = data.get("lang", "en")
    texts = LANG_DATA[lang_code]

    try:
        amount = int(message.text)
        if amount < 10:
            await message.answer(texts["min_err"])
            return
    except ValueError:
        await message.answer(texts["num_err"])
        return

    commission = int(amount * 0.055)
    total = amount + commission

    try:
        await bot.send_invoice(
            chat_id=message.chat.id,
            title="Pactum & Escrow",
            description=f"Deal protection. Fee: {commission} Stars.",
            payload="escrow_deal",
            provider_token="",      # ← ОБЯЗАТЕЛЬНО ПУСТОЙ
            currency="XTR",         # ← ТОЛЬКО "XTR"
            prices=[LabeledPrice(label="Total", amount=total)],
            start_parameter="escrow"
        )
        await state.clear()
    except Exception as e:
        await message.answer(f"❌ Error: {str(e)}")

# === ОБРАБОТКА ОПЛАТЫ ===
@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(lambda msg: msg.successful_payment)
async def on_successful_payment(message: types.Message):
    total = message.successful_payment.total_amount
    # Определяем язык (можно улучшить через payload, но для MVP — EN)
    await message.answer(f"✅ Paid {total} Stars! Escrow is active.")

# === ЗАПУСК ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
