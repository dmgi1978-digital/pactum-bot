import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# === БЕЗОПАСНОСТЬ ===
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN must be set in environment variables!")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# === ВСЕ 20 ЯЗЫКОВ ===
TEXTS = {
    "en": {
        "start": "👋 <b>Hello! I’m Pactum & Escrow.</b>\n\nYour word is a smart contract on <b>TON</b>.\nMake an oath • Place a bet • Secure a deal\n\n✅ Fulfilled — earn reputation\n❌ Broken — lose <b>Stars, TON, USDT</b> and trust\n\nChoose:",
        "how": "⚖️ <b>Pactum & Escrow</b> — escrow on <b>The Open Network</b>.\n\n🔹 Oath — promise in front of witnesses (stored on TON)\n🔹 Bet — wager <b>Stars, TON, USDT</b>\n🔹 Escrow — funds locked in <b>TON smart contract</b>\n\n💎 Fee: <b>5.5%</b> for blockchain security",
        "oath": "🔖 Oath",
        "bet": "🎲 Bet",
        "escrow": "💰 Escrow",
        "reputation": "🏅 Reputation",
        "how_btn": "❓ How it works",
        "lang_set": "✅ Language: English"
    },
    "ru": {
        "start": "👋 <b>Привет! Я — Pactum & Escrow.</b>\n\nТвоё слово — смарт-контракт в <b>TON</b>.\nДай клятву • Заключи пари • Защити сделку\n\n✅ Выполнил — получи репутацию\n❌ Нарушил — потеряешь <b>Stars, TON, USDT</b> и доверие\n\nВыбери:",
        "how": "⚖️ <b>Pactum & Escrow</b> — эскроу в <b>The Open Network</b>.\n\n🔹 Клятва — обещание перед свидетелями (хранится в TON)\n🔹 Пари — ставка на <b>Stars, TON, USDT</b>\n🔹 Эскроу — средства в <b>смарт-контракте TON</b>\n\n💎 Комиссия: <b>5.5%</b> за безопасность блокчейна",
        "oath": "🔖 Клятва",
        "bet": "🎲 Пари",
        "escrow": "💰 Эскроу",
        "reputation": "🏅 Репутация",
        "how_btn": "❓ Как работает",
        "lang_set": "✅ Язык: Русский"
    },
    "es": {
        "start": "👋 <b>¡Hola! Soy Pactum & Escrow.</b>\n\nTu palabra es un smart contract en <b>TON</b>.\nHaz un juramento • Apuesta • Asegura un trato\n\n✅ Cumplido — gana reputación\n❌ Roto — pierde <b>Stars, TON, USDT</b> y confianza\n\nElige:",
        "how": "⚖️ <b>Pactum & Escrow</b> — depósito en garantía en <b>The Open Network</b>.\n\n🔹 Juramento — promesa ante testigos (en TON)\n🔹 Apuesta — apuesta con <b>Stars, TON, USDT</b>\n🔹 Depósito — fondos en <b>contrato inteligente TON</b>\n\n💎 Comisión: <b>5.5%</b> por seguridad blockchain",
        "oath": "🔖 Juramento",
        "bet": "🎲 Apuesta",
        "escrow": "💰 Depósito",
        "reputation": "🏅 Reputación",
        "how_btn": "❓ ¿Cómo funciona?",
        "lang_set": "✅ Idioma: Español"
    },
    "pt": {
        "start": "👋 <b>Olá! Sou o Pactum & Escrow.</b>\n\nSua palavra é um smart contract na <b>TON</b>.\nFaça um juramento • Aposte • Garanta um negócio\n\n✅ Cumprido — ganhe reputação\n❌ Quebrado — perca <b>Stars, TON, USDT</b> e confiança\n\nEscolha:",
        "how": "⚖️ <b>Pactum & Escrow</b> — garantia na <b>The Open Network</b>.\n\n🔹 Juramento — promessa perante testemunhas (na TON)\n🔹 Aposta — aposte com <b>Stars, TON, USDT</b>\n🔹 Garantia — fundos em <b>contrato inteligente TON</b>\n\n💎 Taxa: <b>5,5%</b> pela segurança blockchain",
        "oath": "🔖 Juramento",
        "bet": "🎲 Aposta",
        "escrow": "💰 Garantia",
        "reputation": "🏅 Reputação",
        "how_btn": "❓ Como funciona?",
        "lang_set": "✅ Idioma: Português"
    },
    "tr": {
        "start": "👋 <b>Merhaba! Ben Pactum & Escrow.</b>\n\nSözün, <b>TON</b> üzerinde bir akıllı kontrattır.\nYemin et • Bahis yap • İşlemi güvenceye al\n\n✅ Yaptın — itibar kazan\n❌ Bozdun — <b>Stars, TON, USDT</b> ve güveni kaybet\n\nSeç:",
        "how": "⚖️ <b>Pactum & Escrow</b> — <b>The Open Network</b> üzerinde güvence.\n\n🔹 Yemin — tanıklar önünde söz (TON'da saklı)\n🔹 Bahis — <b>Stars, TON, USDT</b> ile bahis yap\n🔹 Güvence — fonlar <b>TON akıllı kontratında</b>\n\n💎 Ücret: <b>%5,5</b> blockchain güvenliği için",
        "oath": "🔖 Yemin",
        "bet": "🎲 Bahis",
        "escrow": "💰 Güvence",
        "reputation": "🏅 İtibar",
        "how_btn": "❓ Nasıl çalışır?",
        "lang_set": "✅ Dil: Türkçe"
    },
    "fa": {
        "start": "👋 <b>سلام! من Pactum & Escrow هستم.</b>\n\nکلمه‌ی شما یک قرارداد هوشمند در <b>TON</b> است.\nسوگند بخور • شرط ببند • معامله را تضمین کن\n\n✅ انجام شد — اعتبار کسب کن\n❌ شکسته شد — <b>استارز، TON، USDT</b> و اعتماد را از دست بده\n\nانتخاب کن:",
        "how": "⚖️ <b>Pactum & Escrow</b> — تضمین در <b>The Open Network</b>.\n\n🔹 سوگند — قول در برابر شاهدان (در TON ذخیره شده)\n🔹 شرط — با <b>استارز، TON، USDT</b> شرط ببند\n🔹 تضمین — وجوه در <b>قرارداد هوشمند TON</b>\n\n💎 کارمزد: <b>۵٫۵٪</b> برای امنیت بلاکچین",
        "oath": "🔖 سوگند",
        "bet": "🎲 شرط",
        "escrow": "💰 تضمین",
        "reputation": "🏅 اعتبار",
        "how_btn": "❓ چگونه کار می‌کند؟",
        "lang_set": "✅ زبان: فارسی"
    },
    "ar": {
        "start": "👋 <b>مرحباً! أنا Pactum & Escrow.</b>\n\nكلمتك عقد ذكي على <b>TON</b>.\nأقسم • راهن • أمّن صفقة\n\n✅ أنجزت — اكتسب سمعة\n❌ خالفت — افقد <b>Stars و TON و USDT</b> والثقة\n\nاختر:",
        "how": "⚖️ <b>Pactum & Escrow</b> — ضمان على <b>The Open Network</b>.\n\n🔹 القسم — وعد أمام الشهود (مخزن في TON)\n🔹 الرهان — راهن بـ <b>Stars أو TON أو USDT</b>\n🔹 الضمان — الأموال في <b>عقد ذكي TON</b>\n\n💎 العمولة: <b>5.5%</b> لأمن البلوك تشين",
        "oath": "🔖 قسم",
        "bet": "🎲 رهان",
        "escrow": "💰 ضمان",
        "reputation": "🏅 سمعة",
        "how_btn": "❓ كيف يعمل؟",
        "lang_set": "✅ اللغة: العربية"
    },
    "id": {
        "start": "👋 <b>Halo! Saya Pactum & Escrow.</b>\n\nKata-katamu adalah smart contract di <b>TON</b>.\nBersumpah • Bertaruh • Amankan transaksi\n\n✅ Dipenuhi — dapatkan reputasi\n❌ Dilanggar — kehilangan <b>Stars, TON, USDT</b> dan kepercayaan\n\nPilih:",
        "how": "⚖️ <b>Pactum & Escrow</b> — escrow di <b>The Open Network</b>.\n\n🔹 Sumpah — janji di depan saksi (di TON)\n🔹 Taruhan — pertaruhkan <b>Stars, TON, USDT</b>\n🔹 Escrow — dana di <b>smart contract TON</b>\n\n💎 Biaya: <b>5,5%</b> untuk keamanan blockchain",
        "oath": "🔖 Sumpah",
        "bet": "🎲 Taruhan",
        "escrow": "💰 Escrow",
        "reputation": "🏅 Reputasi",
        "how_btn": "❓ Bagaimana cara kerjanya?",
        "lang_set": "✅ Bahasa: Indonesia"
    },
    "fr": {
        "start": "👋 <b>Bonjour ! Je suis Pactum & Escrow.</b>\n\nVotre parole est un smart contract sur <b>TON</b>.\nFaites un serment • Pariez • Sécurisez une transaction\n\n✅ Accompli — gagnez en réputation\n❌ Rompu — perdez <b>Stars, TON, USDT</b> et la confiance\n\nChoisissez :",
        "how": "⚖️ <b>Pactum & Escrow</b> — dépôt de garantie sur <b>The Open Network</b>.\n\n🔹 Serment — promesse devant témoins (sur TON)\n🔹 Pari — misez en <b>Stars, TON, USDT</b>\n🔹 Dépôt — fonds dans un <b>smart contract TON</b>\n\n💎 Frais : <b>5,5 %</b> pour la sécurité blockchain",
        "oath": "🔖 Serment",
        "bet": "🎲 Pari",
        "escrow": "💰 Dépôt",
        "reputation": "🏅 Réputation",
        "how_btn": "❓ Comment ça marche ?",
        "lang_set": "✅ Langue : Français"
    },
    "de": {
        "start": "👋 <b>Hallo! Ich bin Pactum & Escrow.</b>\n\nDein Wort ist ein Smart Contract auf <b>TON</b>.\nSchwöre einen Eid • Wette • Sichere einen Deal\n\n✅ Erfüllt — erhalte Reputation\n❌ Gebrochen — verliere <b>Stars, TON, USDT</b> und Vertrauen\n\nWähle:",
        "how": "⚖️ <b>Pactum & Escrow</b> — Escrow auf <b>The Open Network</b>.\n\n🔹 Eid — Versprechen vor Zeugen (in TON gespeichert)\n🔹 Wette — setze <b>Stars, TON, USDT</b>\n🔹 Escrow — Gelder im <b>TON Smart Contract</b>\n\n💎 Gebühr: <b>5,5 %</b> für Blockchain-Sicherheit",
        "oath": "🔖 Eid",
        "bet": "🎲 Wette",
        "escrow": "💰 Escrow",
        "reputation": "🏅 Reputation",
        "how_btn": "❓ Wie funktioniert es?",
        "lang_set": "✅ Sprache: Deutsch"
    },
    "zh": {
        "start": "👋 <b>你好！我是 Pactum & Escrow。</b>\n\n你的话是 <b>TON</b> 上的智能合约。\n立下誓言 • 下注 • 保障交易\n\n✅ 完成 — 获得信誉\n❌ 违背 — 失去 <b>Stars、TON、USDT</b> 和信任\n\n选择：",
        "how": "⚖️ <b>Pactum & Escrow</b> — <b>The Open Network</b> 托管服务。\n\n🔹 誓言 — 在见证人面前承诺（存储于 TON）\n🔹 下注 — 使用 <b>Stars、TON、USDT</b> 下注\n🔹 托管 — 资金锁定在 <b>TON 智能合约</b> 中\n\n💎 费用：<b>5.5%</b> 用于区块链安全",
        "oath": "🔖 誓言",
        "bet": "🎲 下注",
        "escrow": "💰 托管",
        "reputation": "🏅 信誉",
        "how_btn": "❓ 如何运作？",
        "lang_set": "✅ 语言：中文"
    },
    "ko": {
        "start": "👋 <b>안녕하세요! 저는 Pactum & Escrow입니다.</b>\n\n당신의 말은 <b>TON</b>의 스마트 계약입니다.\n서약 • 베팅 • 거래 보호\n\n✅ 이행 — 평판 획득\n❌ 위반 — <b>Stars, TON, USDT</b> 및 신뢰 상실\n\n선택하세요:",
        "how": "⚖️ <b>Pactum & Escrow</b> — <b>The Open Network</b> 에스크로 서비스.\n\n🔹 서약 — 증인 앞 약속 (TON에 저장)\n🔹 베팅 — <b>Stars, TON, USDT</b>로 베팅\n🔹 에스크로 — 자금은 <b>TON 스마트 계약</b>에 잠금\n\n💎 수수료: <b>5.5%</b> 블록체인 보안을 위해",
        "oath": "🔖 서약",
        "bet": "🎲 베팅",
        "escrow": "💰 에스크로",
        "reputation": "🏅 평판",
        "how_btn": "❓ 어떻게 작동하나요?",
        "lang_set": "✅ 언어: 한국어"
    },
    "hi": {
        "start": "👋 <b>नमस्ते! मैं Pactum & Escrow हूँ।</b>\n\nआपका वचन <b>TON</b> पर एक स्मार्ट अनुबंध है।\nशपथ लें • दांव लगाएं • लेन-देन सुरक्षित करें\n\n✅ पूर्ण — प्रतिष्ठा अर्जित करें\n❌ टूटा — <b>Stars, TON, USDT</b> और भरोसा खोएं\n\nचुनें:",
        "how": "⚖️ <b>Pactum & Escrow</b> — <b>The Open Network</b> पर एस्क्रो।\n\n🔹 शपथ — गवाहों के सामने वादा (TON में संग्रहीत)\n🔹 दांव — <b>Stars, TON, USDT</b> में दांव लगाएं\n🔹 एस्क्रो — धन <b>TON स्मार्ट अनुबंध</b> में तालाबंद\n\n💎 शुल्क: <b>5.5%</b> ब्लॉकचेन सुरक्षा के लिए",
        "oath": "🔖 शपथ",
        "bet": "🎲 दांव",
        "escrow": "💰 एस्क्रो",
        "reputation": "🏅 प्रतिष्ठा",
        "how_btn": "❓ यह कैसे काम करता है?",
        "lang_set": "✅ भाषा: हिंदी"
    },
    "vi": {
        "start": "👋 <b>Xin chào! Tôi là Pactum & Escrow.</b>\n\nLời bạn nói là hợp đồng thông minh trên <b>TON</b>.\nThề • Đặt cược • Bảo vệ giao dịch\n\n✅ Hoàn thành — nhận uy tín\n❌ Vi phạm — mất <b>Stars, TON, USDT</b> và niềm tin\n\nChọn:",
        "how": "⚖️ <b>Pactum & Escrow</b> — dịch vụ ký quỹ trên <b>The Open Network</b>.\n\n🔹 Lời thề — hứa trước nhân chứng (lưu trên TON)\n🔹 Cược — cược bằng <b>Stars, TON, USDT</b>\n🔹 Ký quỹ — tiền bị khóa trong <b>hợp đồng thông minh TON</b>\n\n💎 Phí: <b>5,5%</b> cho bảo mật blockchain",
        "oath": "🔖 Lời thề",
        "bet": "🎲 Cược",
        "escrow": "💰 Ký quỹ",
        "reputation": "🏅 Uy tín",
        "how_btn": "❓ Cách hoạt động?",
        "lang_set": "✅ Ngôn ngữ: Tiếng Việt"
    },
    "th": {
        "start": "👋 <b>สวัสดี! ฉันคือ Pactum & Escrow</b>\n\nคำพูดของคุณคือสัญญาอัจฉริยะบน <b>TON</b>\nให้คำสาบาน • เดิมพัน • รักษาธุรกรรม\n\n✅ ทำสำเร็จ — ได้ชื่อเสียง\n❌ ผิดคำ — สูญเสีย <b>Stars, TON, USDT</b> และความไว้วางใจ\n\nเลือก:",
        "how": "⚖️ <b>Pactum & Escrow</b> — บริการเอครอว์บน <b>The Open Network</b>\n\n🔹 คำสาบาน — สัญญาต่อหน้าพยาน (เก็บใน TON)\n🔹 เดิมพัน — เดิมพันด้วย <b>Stars, TON, USDT</b>\n🔹 เอครอว์ — เงินถูกล็อกใน <b>สัญญาอัจฉริยะ TON</b>\n\n💎 ค่าธรรมเนียม: <b>5.5%</b> สำหรับความปลอดภัยบล็อกเชน",
        "oath": "🔖 คำสาบาน",
        "bet": "🎲 เดิมพัน",
        "escrow": "💰 เอครอว์",
        "reputation": "🏅 ชื่อเสียง",
        "how_btn": "❓ ทำงานอย่างไร?",
        "lang_set": "✅ ภาษา: ไทย"
    },
    "uk": {
        "start": "👋 <b>Привіт! Я — Pactum & Escrow.</b>\n\nТвоє слово — смарт-контракт у <b>TON</b>.\nДай клятву • Заключи парі • Захисти угоду\n\n✅ Виконано — отримай репутацію\n❌ Порушено — втратиш <b>Stars, TON, USDT</b> і довіру\n\nОбери:",
        "how": "⚖️ <b>Pactum & Escrow</b> — ескроу в <b>The Open Network</b>.\n\n🔹 Клятва — обіцянка перед свідками (зберігається в TON)\n🔹 Парі — ставка на <b>Stars, TON, USDT</b>\n🔹 Ескроу — кошти в <b>смарт-контракті TON</b>\n\n💎 Комісія: <b>5.5%</b> за безпеку блокчейну",
        "oath": "🔖 Клятва",
        "bet": "🎲 Парі",
        "escrow": "💰 Ескроу",
        "reputation": "🏅 Репутація",
        "how_btn": "❓ Як це працює?",
        "lang_set": "✅ Мова: Українська"
    },
    "pl": {
        "start": "👋 <b>Cześć! Jestem Pactum & Escrow.</b>\n\nTwoje słowo to smart contract w <b>TON</b>.\nZłóż przysięgę • Zakład • Zabezpiecz transakcję\n\n✅ Spełnione — zdobyj reputację\n❌ Złamane — strać <b>Stars, TON, USDT</b> i zaufanie\n\nWybierz:",
        "how": "⚖️ <b>Pactum & Escrow</b> — depozyt w <b>The Open Network</b>.\n\n🔹 Przysięga — obietnica przed świadkami (w TON)\n🔹 Zakład — zakład za <b>Stars, TON, USDT</b>\n🔹 Depozyt — środki w <b>smart kontrakcie TON</b>\n\n💎 Prowizja: <b>5,5%</b> za bezpieczeństwo blockchain",
        "oath": "🔖 Przysięga",
        "bet": "🎲 Zakład",
        "escrow": "💰 Depozyt",
        "reputation": "🏅 Reputacja",
        "how_btn": "❓ Jak to działa?",
        "lang_set": "✅ Język: Polski"
    },
    "it": {
        "start": "👋 <b>Ciao! Sono Pactum & Escrow.</b>\n\nLa tua parola è uno smart contract su <b>TON</b>.\nFai un giuramento • Scommetti • Sicurizza un affare\n\n✅ Rispettato — guadagna reputazione\n❌ Violato — perdi <b>Stars, TON, USDT</b> e fiducia\n\nScegli:",
        "how": "⚖️ <b>Pactum & Escrow</b> — escrow su <b>The Open Network</b>.\n\n🔹 Giuramento — promessa davanti a testimoni (su TON)\n🔹 Scommessa — scommetti con <b>Stars, TON, USDT</b>\n🔹 Escrow — fondi bloccati in <b>smart contract TON</b>\n\n💎 Commissione: <b>5,5%</b> per la sicurezza blockchain",
        "oath": "🔖 Giuramento",
        "bet": "🎲 Scommessa",
        "escrow": "💰 Escrow",
        "reputation": "🏅 Reputazione",
        "how_btn": "❓ Come funziona?",
        "lang_set": "✅ Lingua: Italiano"
    },
    "nl": {
        "start": "👋 <b>Hallo! Ik ben Pactum & Escrow.</b>\n\nJe woord is een smart contract op <b>TON</b>.\nZweer een eed • Wed • Beveilig een deal\n\n✅ Nagekomen — verdien reputatie\n❌ Gebroken — verlies <b>Stars, TON, USDT</b> en vertrouwen\n\nKies:",
        "how": "⚖️ <b>Pactum & Escrow</b> — escrow op <b>The Open Network</b>.\n\n🔹 Eed — belofte voor getuigen (opgeslagen op TON)\n🔹 Weddenschap — wed met <b>Stars, TON, USDT</b>\n🔹 Escrow — fondsen vastgezet in <b>TON smart contract</b>\n\n💎 Tarief: <b>5,5%</b> voor blockchain-beveiliging",
        "oath": "🔖 Eed",
        "bet": "🎲 Weddenschap",
        "escrow": "💰 Escrow",
        "reputation": "🏅 Reputatie",
        "how_btn": "❓ Hoe werkt het?",
        "lang_set": "✅ Taal: Nederlands"
    },
    "ja": {
        "start": "👋 <b>こんにちは！Pactum & Escrowです。</b>\n\nあなたの言葉は<b>TON</b>上のスマートコントラクトです。\n誓い • 賭け • 取引を保護\n\n✅ 達成 — 評判を獲得\n❌ 違反 — <b>Stars、TON、USDT</b>と信頼を失う\n\n選択してください:",
        "how": "⚖️ <b>Pactum & Escrow</b> — <b>The Open Network</b>上のエスクロー。\n\n🔹 誓い — 証人への約束（TONに保存）\n🔹 賭け — <b>Stars、TON、USDT</b>で賭ける\n🔹 エスクロー — 資金は<b>TONスマートコントラクト</b>でロック\n\n💎 手数料: <b>5.5%</b> ブロックチェーンセキュリティのため",
        "oath": "🔖 誓い",
        "bet": "🎲 賭け",
        "escrow": "💰 エスクロー",
        "reputation": "🏅 評判",
        "how_btn": "❓ 仕組みは？",
        "lang_set": "✅ 言語: 日本語"
    }
}

# === СОСТОЯНИЕ ===
class UserState(StatesGroup):
    choosing_language = State()

# === КЛАВИАТУРА ЯЗЫКОВ ===
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

# === ГЛАВНОЕ МЕНЮ ===
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
        "🇬🇧 English": "en",
        "🇷🇺 Русский": "ru",
        "🇪🇸 Español": "es",
        "🇵🇹 Português": "pt",
        "🇹🇷 Türkçe": "tr",
        "🇮🇷 فارسی": "fa",
        "🇸🇦 العربية": "ar",
        "🇮🇩 Bahasa": "id",
        "🇫🇷 Français": "fr",
        "🇩🇪 Deutsch": "de",
        "🇨🇳 中文": "zh",
        "🇰🇷 한국어": "ko",
        "🇮🇳 हिंदी": "hi",
        "🇻🇳 Tiếng Việt": "vi",
        "🇹🇭 ไทย": "th",
        "🇺🇦 Українська": "uk",
        "🇵🇱 Polski": "pl",
        "🇮🇹 Italiano": "it",
        "🇳🇱 Nederlands": "nl",
        "🇯🇵 日本語": "ja"
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

    if message.text == t["how_btn"]:
        await message.answer(t["how"], parse_mode="HTML")
    elif message.text == t["reputation"]:
        await message.answer("🔒 Reputation unlocks after your first TON deal.")
    elif message.text in [t["oath"], t["bet"], t["escrow"]]:
        await message.answer("🔥 Coming in 48 hours! Enable notifications: @PactumEscrow")
    else:
        await cmd_start(message, state)

# === ЗАПУСК ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
