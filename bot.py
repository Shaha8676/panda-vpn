import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, LabeledPrice, PreCheckoutQuery
)
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
import database as db
import os
import json

# =====================
# SOZLAMALAR
# =====================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8937881795:AAEzekvk1lG3HUn8LOLXWB8IexRbaX3-2Yk")
MINI_APP_URL = os.environ.get("MINI_APP_URL", "https://shaha8676.github.io/vpn-app/vpn-app.html")
ADMIN_ID = 366589255
SUPPORT_USERNAME = "@Panda56_support"
HAPP_LINK = "https://g.ultm.in/s/E9GPTMr_hN2CfzVw"

logging.basicConfig(level=logging.INFO)

bot: Bot = None
dp = Dispatcher(storage=MemoryStorage())

# =====================
# TILLAR
# =====================
TEXTS = {
    "uz": {
        "welcome": (
            "👋 <b>PandaVPN ga xush kelibsiz!</b>\n\n"
            "🛡 Xavfsiz va tez internet uchun eng yaxshi tanlov.\n\n"
            "Quyidagi menyudan foydalaning:"
        ),
        "choose_lang": "🌐 Tilni tanlang / Выберите язык:",
        "main_menu": "📋 Asosiy menyu:",
        "my_sub": "📦 Mening obunam",
        "buy_sub": "🛒 Obuna sotib olish",
        "install": "📱 O'rnatish va sozlash",
        "referral": "🎁 Referal dastur",
        "support": "💬 Qo'llab-quvvatlash",
        "open_app": "🚀 Ilovani ochish",
        "no_sub": (
            "❌ <b>Faol obuna yo'q</b>\n\n"
            "Obuna sotib olish uchun quyidagi tugmani bosing:"
        ),
        "sub_info": (
            "✅ <b>Faol obuna:</b>\n\n"
            "📅 Muddat: <b>{days} kun qoldi</b>\n"
            "📱 Qurilmalar: <b>{devices} ta</b>\n"
            "🌐 Server: <b>{server}</b>\n"
            "📊 Traffic: <b>{traffic} GB</b>"
        ),
        "choose_plan": "💎 Tarif rejani tanlang:",
        "referral_info": (
            "🎁 <b>Referal dastur</b>\n\n"
            "Har bir do'st uchun <b>+7 kun</b> bepul!\n\n"
            "Sizning havolangiz:\n"
            "<code>{link}</code>\n\n"
            "👥 Taklif qilganlar: <b>{count} ta</b>"
        ),
        "plan_1": "1 oy — 100 ⭐",
        "plan_3": "3 oy — 270 ⭐ (-10%)",
        "plan_6": "6 oy — 480 ⭐ (-20%)",
        "plan_12": "12 oy — 840 ⭐ (-30%)",
        "pay_btn": "⭐ To'lash",
        "back": "⬅️ Orqaga",
        "lang_set": "✅ Til o'zgartirildi!",
        "support_text": (
            "💬 <b>Qo'llab-quvvatlash</b>\n\n"
            "Muammolar yoki savollar bo'lsa:\n"
            f"👉 {https://t.me/Panda56_support}"
        ),
        "pay_success": (
            "✅ <b>To'lov qabul qilindi!</b>\n\n"
            "🎉 VPN linkingiz tayyor!\n\n"
            "📱 Happ ilovasiga qo'shish uchun:\n"
            "1. Happ ilovasini oching\n"
            "2. <b>+</b> tugmasini bosing\n"
            "3. Quyidagi linkni joylashtiring:\n\n"
            f"<code>{https://g.ultm.in/s/E9GPTMr_hN2CfzVw }</code>"
        ),
        "install_hint": (
            "📱 <b>Ilovani yuklab oling:</b>\n\n"
            "🍎 iOS: <a href='https://apps.apple.com/app/id6446814690'>Happ</a>\n"
            "🤖 Android: <a href='https://play.google.com/store/apps/details?id=com.v2ray.ang'>v2rayNG</a>\n"
            "💻 Windows/Mac: <a href='https://github.com/2dust/v2rayN/releases'>v2rayN</a>"
        ),
    },
    "ru": {
        "welcome": (
            "👋 <b>Добро пожаловать в PandaVPN!</b>\n\n"
            "🛡 Лучший выбор для безопасного и быстрого интернета.\n\n"
            "Воспользуйтесь меню ниже:"
        ),
        "choose_lang": "🌐 Tilni tanlang / Выберите язык:",
        "main_menu": "📋 Главное меню:",
        "my_sub": "📦 Моя подписка",
        "buy_sub": "🛒 Купить подписку",
        "install": "📱 Установка и настройка",
        "referral": "🎁 Реферальная программа",
        "support": "💬 Поддержка",
        "open_app": "🚀 Открыть приложение",
        "no_sub": (
            "❌ <b>Активная подписка отсутствует</b>\n\n"
            "Нажмите кнопку ниже чтобы купить подписку:"
        ),
        "sub_info": (
            "✅ <b>Активная подписка:</b>\n\n"
            "📅 Срок: <b>осталось {days} дней</b>\n"
            "📱 Устройства: <b>{devices}</b>\n"
            "🌐 Сервер: <b>{server}</b>\n"
            "📊 Трафик: <b>{traffic} ГБ</b>"
        ),
        "choose_plan": "💎 Выберите тарифный план:",
        "referral_info": (
            "🎁 <b>Реферальная программа</b>\n\n"
            "За каждого друга <b>+7 дней</b> бесплатно!\n\n"
            "Ваша ссылка:\n"
            "<code>{link}</code>\n\n"
            "👥 Приглашено: <b>{count}</b>"
        ),
        "plan_1": "1 месяц — 100 ⭐",
        "plan_3": "3 месяца — 270 ⭐ (-10%)",
        "plan_6": "6 месяцев — 480 ⭐ (-20%)",
        "plan_12": "12 месяцев — 840 ⭐ (-30%)",
        "pay_btn": "⭐ Оплатить",
        "back": "⬅️ Назад",
        "lang_set": "✅ Язык изменён!",
        "support_text": (
            "💬 <b>Поддержка</b>\n\n"
            "По вопросам и проблемам:\n"
            f"👉 {https://t.me/Panda56_support}"
        ),
        "pay_success": (
            "✅ <b>Оплата принята!</b>\n\n"
            "🎉 Ваш VPN готов!\n\n"
            "📱 Добавьте в приложение Happ:\n"
            "1. Откройте приложение Happ\n"
            "2. Нажмите <b>+</b>\n"
            "3. Вставьте ссылку:\n\n"
            f"<code>{https://g.ultm.in/s/E9GPTMr_hN2CfzVw }</code>"
        ),
        "install_hint": (
            "📱 <b>Скачайте приложение:</b>\n\n"
            "🍎 iOS: <a href='https://apps.apple.com/app/id6446814690'>Happ</a>\n"
            "🤖 Android: <a href='https://play.google.com/store/apps/details?id=com.v2ray.ang'>v2rayNG</a>\n"
            "💻 Windows/Mac: <a href='https://github.com/2dust/v2rayN/releases'>v2rayN</a>"
        ),
    }
}

PLANS = {
    "1":  {"months": 1,  "price": 100,  "days": 30},
    "3":  {"months": 3,  "price": 270,  "days": 90},
    "6":  {"months": 6,  "price": 480,  "days": 180},
    "12": {"months": 12, "price": 840,  "days": 365},
}

def txt(user_id: int, key: str) -> str:
    lang = db.get_user_lang(user_id) or "uz"
    return TEXTS[lang].get(key, "")

# =====================
# KLAVIATURALAR
# =====================
def lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
    ]])

def main_keyboard(user_id: int) -> InlineKeyboardMarkup:
    t = lambda k: txt(user_id, k)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("my_sub"),  callback_data="my_sub")],
        [InlineKeyboardButton(text=t("buy_sub"), callback_data="buy_sub")],
        [InlineKeyboardButton(text=t("open_app"), web_app=WebAppInfo(url=MINI_APP_URL))],
        [
            InlineKeyboardButton(text=t("referral"), callback_data="referral"),
            InlineKeyboardButton(text=t("support"),  callback_data="support"),
        ],
        [InlineKeyboardButton(text="🌐 Til / Язык", callback_data="change_lang")],
    ])

def plans_keyboard(user_id: int) -> InlineKeyboardMarkup:
    t = lambda k: txt(user_id, k)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("plan_1"),  callback_data="plan_1")],
        [InlineKeyboardButton(text=t("plan_3"),  callback_data="plan_3")],
        [InlineKeyboardButton(text=t("plan_6"),  callback_data="plan_6")],
        [InlineKeyboardButton(text=t("plan_12"), callback_data="plan_12")],
        [InlineKeyboardButton(text=t("back"),    callback_data="main_menu")],
    ])

def pay_keyboard(user_id: int, plan_id: str) -> InlineKeyboardMarkup:
    t = lambda k: txt(user_id, k)
    plan = PLANS[plan_id]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{t('pay_btn')} {plan['price']}",
            callback_data=f"pay_{plan_id}"
        )],
        [InlineKeyboardButton(text=t("back"), callback_data="buy_sub")],
    ])

def kb_back(uid: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=txt(uid, "back"), callback_data="main_menu")]
    ])

# =====================
# HANDLERLAR
# =====================
@dp.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    ref_code = message.text.split()[1] if len(message.text.split()) > 1 else None

    is_new = db.add_user(
        user_id=user.id,
        username=user.username or "",
        full_name=user.full_name,
        ref_code=ref_code
    )

    if is_new and ref_code:
        referrer_id = db.get_user_by_ref(ref_code)
        if referrer_id:
            db.add_bonus_days(referrer_id, 7)
            await bot.send_message(
                referrer_id,
                "🎁 Do'stingiz qo'shildi! Sizga +7 kun berildi!"
            )

    if is_new or not db.get_user_lang(user.id):
        await message.answer(
            "🌐 <b>Tilni tanlang / Выберите язык:</b>",
            parse_mode="HTML",
            reply_markup=lang_keyboard()
        )
    else:
        await show_main_menu(message.chat.id, user.id)


async def show_main_menu(chat_id: int, user_id: int, message_id: int = None):
    text = txt(user_id, "welcome")
    kb = main_keyboard(user_id)
    if message_id:
        await bot.edit_message_text(
            text, chat_id, message_id, parse_mode="HTML", reply_markup=kb
        )
    else:
        await bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=kb)


@dp.callback_query(F.data.in_(["lang_uz", "lang_ru"]))
async def cb_lang(call: CallbackQuery):
    lang = call.data.split("_")[1]
    db.set_user_lang(call.from_user.id, lang)
    await call.answer(TEXTS[lang]["lang_set"])
    await show_main_menu(call.message.chat.id, call.from_user.id, call.message.message_id)


@dp.callback_query(F.data == "main_menu")
async def cb_main_menu(call: CallbackQuery):
    await show_main_menu(call.message.chat.id, call.from_user.id, call.message.message_id)


@dp.callback_query(F.data == "my_sub")
async def cb_my_sub(call: CallbackQuery):
    uid = call.from_user.id
    sub = db.get_active_subscription(uid)
    if not sub:
        text = txt(uid, "no_sub")
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=txt(uid, "buy_sub"), callback_data="buy_sub")],
            [InlineKeyboardButton(text=txt(uid, "back"),    callback_data="main_menu")],
        ])
    else:
        text = txt(uid, "sub_info").format(
            days=sub["days_left"],
            devices=sub["devices"],
            server=sub["server"],
            traffic=sub["traffic_gb"]
        )
        kb = kb_back(uid)
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=kb)


@dp.callback_query(F.data == "buy_sub")
async def cb_buy_sub(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.edit_text(
        txt(uid, "choose_plan"),
        parse_mode="HTML",
        reply_markup=plans_keyboard(uid)
    )


@dp.callback_query(F.data.startswith("plan_"))
async def cb_plan(call: CallbackQuery):
    uid = call.from_user.id
    plan_id = call.data.split("_")[1]
    plan = PLANS[plan_id]
    lang = db.get_user_lang(uid) or "uz"

    if lang == "uz":
        text = (
            f"💎 <b>{plan['months']} oylik obuna</b>\n\n"
            f"⭐ Narx: <b>{plan['price']} Stars</b>\n"
            f"📅 Muddat: <b>{plan['days']} kun</b>\n"
            f"📱 Qurilmalar: <b>Cheksiz</b>\n\n"
            "To'lash uchun tugmani bosing:"
        )
    else:
        text = (
            f"💎 <b>Подписка на {plan['months']} мес.</b>\n\n"
            f"⭐ Цена: <b>{plan['price']} Stars</b>\n"
            f"📅 Срок: <b>{plan['days']} дней</b>\n"
            f"📱 Устройства: <b>Без ограничений</b>\n\n"
            "Нажмите кнопку для оплаты:"
        )
    await call.message.edit_text(
        text, parse_mode="HTML",
        reply_markup=pay_keyboard(uid, plan_id)
    )


@dp.callback_query(F.data.startswith("pay_"))
async def cb_pay(call: CallbackQuery):
    uid = call.from_user.id
    plan_id = call.data.split("_")[1]
    plan = PLANS[plan_id]
    lang = db.get_user_lang(uid) or "uz"

    title = f"UzVPN — {plan['months']} oy" if lang == "uz" else f"UzVPN — {plan['months']} мес."
    description = (
        f"VPN obuna {plan['days']} kun | Cheksiz qurilmalar"
        if lang == "uz" else
        f"VPN подписка {plan['days']} дней | Без ограничений"
    )

    await call.message.delete()
    await bot.send_invoice(
        chat_id=uid,
        title=title,
        description=description,
        payload=f"vpn_{plan_id}_{uid}",
        currency="XTR",
        prices=[LabeledPrice(label=title, amount=plan["price"])],
    )


# =====================
# TO'LOV TASDIQLASH
# =====================
@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)


@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    uid = message.from_user.id
    payload = message.successful_payment.invoice_payload
    plan_id = payload.split("_")[1]
    plan = PLANS.get(plan_id)

    if plan:
        db.create_subscription(uid, plan["months"], plan["price"], plan["days"])
        db.create_payment(uid, plan_id, plan["price"])

    await message.answer(
        txt(uid, "pay_success"),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📱 Ilovani yuklab olish", callback_data="install")],
            [InlineKeyboardButton(text=txt(uid, "back"), callback_data="main_menu")],
        ])
    )


@dp.callback_query(F.data == "install")
async def cb_install(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.edit_text(
        txt(uid, "install_hint"),
        parse_mode="HTML",
        disable_web_page_preview=False,
        reply_markup=kb_back(uid)
    )


@dp.callback_query(F.data == "referral")
async def cb_referral(call: CallbackQuery):
    uid = call.from_user.id
    bot_info = await bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={uid}"
    count = db.get_referral_count(uid)
    text = txt(uid, "referral_info").format(link=ref_link, count=count)
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=kb_back(uid))


@dp.callback_query(F.data == "support")
async def cb_support(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.edit_text(
        txt(uid, "support_text"),
        parse_mode="HTML",
        reply_markup=kb_back(uid)
    )


@dp.callback_query(F.data == "change_lang")
async def cb_change_lang(call: CallbackQuery):
    await call.message.edit_text(
        txt(call.from_user.id, "choose_lang"),
        parse_mode="HTML",
        reply_markup=lang_keyboard()
    )


# =====================
# MINI-APP SIGNALLARI
# =====================
@dp.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    uid = message.from_user.id
    lang = db.get_user_lang(uid) or "uz"

    try:
        data = json.loads(message.web_app_data.data)
    except Exception:
        return

    action = data.get("action")

    if action == "support":
        await message.answer(txt(uid, "support_text"), parse_mode="HTML")

    elif action == "referral":
        bot_info = await bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={uid}"
        count = db.get_referral_count(uid)
        text = txt(uid, "referral_info").format(link=ref_link, count=count)
        await message.answer(text, parse_mode="HTML")

    elif action == "my_sub":
        sub = db.get_active_subscription(uid)
        if not sub:
            await message.answer(txt(uid, "no_sub"), parse_mode="HTML")
        else:
            text = txt(uid, "sub_info").format(
                days=sub["days_left"],
                devices=sub["devices"],
                server=sub["server"],
                traffic=sub["traffic_gb"]
            )
            await message.answer(text, parse_mode="HTML")

    elif action == "buy_plan":
        plan_id = str(data.get("plan_id"))
        plan = PLANS.get(plan_id)
        if not plan:
            return
        title = f"UzVPN — {plan['months']} oy" if lang == "uz" else f"UzVPN — {plan['months']} мес."
        description = (
            f"VPN obuna {plan['days']} kun"
            if lang == "uz" else
            f"VPN подписка {plan['days']} дней"
        )
        await bot.send_invoice(
            chat_id=uid,
            title=title,
            description=description,
            payload=f"vpn_{plan_id}_{uid}",
            currency="XTR",
            prices=[LabeledPrice(label=title, amount=plan["price"])],
        )


# =====================
# ISHGA TUSHURISH
# =====================
async def main():
    global bot
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot, handle_signals=False)

if __name__ == "__main__":
    asyncio.run(main())
