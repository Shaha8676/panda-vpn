import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    BufferedInputFile
)
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
import database as db
import vless_manager as vless

# ================================================
# SOZLAMALAR
# ================================================
BOT_TOKEN        = "8937881795:AAEzekvk1lG3HUn8LOLXWB8IexRbaX3-2Yk"
ADMIN_ID         = 366589255        # Sizning Telegram ID
SUPPORT_USERNAME = "https://t.me/Panda56_support"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(storage=MemoryStorage())

# ================================================
# MATNLAR
# ================================================
TEXTS = {
    "uz": {
        "welcome": (
            "👋 <b>UzVPN ga xush kelibsiz!</b>\n\n"
            "🛡 Xavfsiz va tez internet.\n"
            "Menyudan tanlang:"
        ),
        "choose_lang":  "🌐 Tilni tanlang / Выберите язык:",
        "main_menu":    "📋 Asosiy menyu:",
        "my_sub":       "📦 Mening obunam",
        "buy_sub":      "🛒 Obuna sotib olish",
        "referral":     "🎁 Referal dastur",
        "support":      "💬 Yordam",
        "back":         "⬅️ Orqaga",
        "lang_set":     "✅ Til o'zgartirildi!",
        "choose_plan":  "💎 Tarif rejani tanlang:",
        "plan_1":       "1 oy — 100 ₽",
        "plan_3":       "3 oy — 270 ₽  (-10%)",
        "plan_6":       "6 oy — 480 ₽  (-20%)",
        "plan_12":      "12 oy — 840 ₽  (-30%)",
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
        "referral_info": (
            "🎁 <b>Referal dastur</b>\n\n"
            "Har bir do'st uchun <b>+7 kun</b> bepul!\n\n"
            "Sizning havolangiz:\n"
            "<code>{link}</code>\n\n"
            "👥 Taklif qilganlar: <b>{count} ta</b>"
        ),
        "support_text": (
            "💬 <b>Yordam</b>\n\n"
            "Muammolar uchun:\n"
            f"👉 {https://t.me/Panda56_support}"
        ),
        "pay_choose": (
            "💎 <b>{months} oylik obuna</b>\n\n"
            "💰 Narx: <b>{price} ₽</b>\n"
            "📅 Muddat: <b>{days} kun</b>\n\n"
            "To'lov uchun tugmani bosing:"
        ),
        "pay_pending": "⏳ To'lov tekshirilmoqda...",
        "pay_success": (
            "✅ <b>To'lov qabul qilindi!</b>\n\n"
            "🎉 Obunangiz faollashtirilmoqda...\n"
            "Bir daqiqa kuting."
        ),
        "config_ready": (
            "🚀 <b>VPN tayyor!</b>\n\n"
            "Quyidagi link orqali ulanishingiz mumkin.\n"
            "Linkni nusxa olib <b>v2rayN / v2rayNG / Happ</b> ilovasiga qo'shing:\n\n"
            "<code>{link}</code>\n\n"
            "Yoki QR kodni skanerlang 👇"
        ),
        "config_error": "❌ Config yaratishda xatolik. Admin bilan bog'laning.",
        "extend_info": "📅 Obunangiz <b>{days} kun</b> ga uzaytirildi!",
        "bonus_received": "🎁 Do'stingiz qo'shildi! Sizga <b>+7 kun</b> berildi!",
        "install_hint": (
            "📱 <b>Ilovani yuklab oling:</b>\n\n"
            "🍎 iOS: <a href='https://apps.apple.com/app/id6446814690'>Happ</a> yoki "
            "<a href='https://apps.apple.com/app/id1591822138'>v2Box</a>\n"
            "🤖 Android: <a href='https://play.google.com/store/apps/details?id=com.v2ray.ang'>v2rayNG</a>\n"
            "💻 Windows/Mac: <a href='https://github.com/2dust/v2rayN/releases'>v2rayN</a>"
        ),
    },
    "ru": {
        "welcome": (
            "👋 <b>Добро пожаловать в UzVPN!</b>\n\n"
            "🛡 Безопасный и быстрый интернет.\n"
            "Выберите из меню:"
        ),
        "choose_lang":  "🌐 Tilni tanlang / Выберите язык:","main_menu":    "📋 Главное меню:",
        "my_sub":       "📦 Моя подписка",
        "buy_sub":      "🛒 Купить подписку",
        "referral":     "🎁 Реферальная программа",
        "support":      "💬 Поддержка",
        "back":         "⬅️ Назад",
        "lang_set":     "✅ Язык изменён!",
        "choose_plan":  "💎 Выберите тарифный план:",
        "plan_1":       "1 месяц — 100 ₽",
        "plan_3":       "3 месяца — 270 ₽  (-10%)",
        "plan_6":       "6 месяцев — 480 ₽  (-20%)",
        "plan_12":      "12 месяцев — 840 ₽  (-30%)",
        "no_sub": (
            "❌ <b>Нет активной подписки</b>\n\n"
            "Нажмите кнопку ниже чтобы купить:"
        ),
        "sub_info": (
            "✅ <b>Активная подписка:</b>\n\n"
            "📅 Срок: <b>осталось {days} дней</b>\n"
            "📱 Устройства: <b>{devices}</b>\n"
            "🌐 Сервер: <b>{server}</b>\n"
            "📊 Трафик: <b>{traffic} ГБ</b>"
        ),
        "referral_info": (
            "🎁 <b>Реферальная программа</b>\n\n"
            "За каждого друга <b>+7 дней</b> бесплатно!\n\n"
            "Ваша ссылка:\n"
            "<code>{link}</code>\n\n"
            "👥 Приглашено: <b>{count}</b>"
        ),
        "support_text": (
            "💬 <b>Поддержка</b>\n\n"
            "По вопросам:\n"
            f"👉 {https://t.me/Panda56_support}"
        ),
        "pay_choose": (
            "💎 <b>Подписка на {months} мес.</b>\n\n"
            "💰 Цена: <b>{price} ₽</b>\n"
            "📅 Срок: <b>{days} дней</b>\n\n"
            "Нажмите для оплаты:"
        ),
        "pay_pending": "⏳ Проверяем оплату...",
        "pay_success": (
            "✅ <b>Оплата принята!</b>\n\n"
            "🎉 Активируем подписку...\n"
            "Подождите минуту."
        ),
        "config_ready": (
            "🚀 <b>VPN готов!</b>\n\n"
            "Скопируйте ссылку и добавьте в <b>v2rayN / v2rayNG / Happ</b>:\n\n"
            "<code>{link}</code>\n\n"
            "Или отсканируйте QR-код 👇"
        ),
        "config_error": "❌ Ошибка создания конфига. Обратитесь к администратору.",
        "extend_info": "📅 Ваша подписка продлена на <b>{days} дней</b>!",
        "bonus_received": "🎁 Ваш друг присоединился! Вам начислено <b>+7 дней</b>!",
        "install_hint": (
            "📱 <b>Скачайте приложение:</b>\n\n"
            "🍎 iOS: <a href='https://apps.apple.com/app/id6446814690'>Happ</a> или "
            "<a href='https://apps.apple.com/app/id1591822138'>v2Box</a>\n"
            "🤖 Android: <a href='https://play.google.com/store/apps/details?id=com.v2ray.ang'>v2rayNG</a>\n"
            "💻 Windows/Mac: <a href='https://github.com/2dust/v2rayN/releases'>v2rayN</a>"
        ),
    }
}

PLANS = {
    "1":  {"months": 1,  "price": 100, "days": 30},
    "3":  {"months": 3,  "price": 270, "days": 90},
    "6":  {"months": 6,  "price": 480, "days": 180},
    "12": {"months": 12, "price": 840, "days": 365},
}

def t(user_id: int, key: str) -> str:
    lang = db.get_user_lang(user_id) or "uz"
    return TEXTS[lang].get(key, "")

# ================================================
# KLAVIATURALAR
# ================================================
def kb_lang() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🇺🇿 O'zbek",   callback_data="lang_uz"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
    ]])

def kb_main(uid: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid,"my_sub"),  callback_data="my_sub")],
        [InlineKeyboardButton(text=t(uid,"buy_sub"), callback_data="buy_sub")],
        [InlineKeyboardButton(text="📱 " + ("Ilovani yuklab olish" if (db.get_user_lang(uid) or "uz") == "uz" else "Скачать приложение"),
                              callback_data="install")],
        [
            InlineKeyboardButton(text=t(uid,"referral"), callback_data="referral"),
            InlineKeyboardButton(text=t(uid,"support"),  callback_data="support"),
        ],[InlineKeyboardButton(text="🌐 Til / Язык", callback_data="change_lang")],
    ])

def kb_plans(uid: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid,"plan_1"),  callback_data="plan_1")],
        [InlineKeyboardButton(text=t(uid,"plan_3"),  callback_data="plan_3")],
        [InlineKeyboardButton(text=t(uid,"plan_6"),  callback_data="plan_6")],
        [InlineKeyboardButton(text=t(uid,"plan_12"), callback_data="plan_12")],
        [InlineKeyboardButton(text=t(uid,"back"),    callback_data="main_menu")],
    ])

def kb_pay(uid: int, plan_id: str) -> InlineKeyboardMarkup:
    plan = PLANS[plan_id]
    pay_text = f"💳 {'To\'lash' if (db.get_user_lang(uid) or 'uz') == 'uz' else 'Оплатить'} — {plan['price']} ₽"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=pay_text, callback_data=f"pay_{plan_id}")],
        [InlineKeyboardButton(text=t(uid,"back"), callback_data="buy_sub")],
    ])

def kb_back(uid: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid,"back"), callback_data="main_menu")]
    ])

# ================================================
# YORDAMCHI FUNKSIYA — menyu ko'rsatish
# ================================================
async def show_menu(chat_id: int, uid: int, msg_id: int = None):
    text = t(uid, "welcome")
    kb   = kb_main(uid)
    if msg_id:
        await bot.edit_message_text(text, chat_id, msg_id, parse_mode="HTML", reply_markup=kb)
    else:
        await bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=kb)

# ================================================
# HANDLERLAR
# ================================================
@dp.message(CommandStart())
async def cmd_start(message: Message):
    uid  = message.from_user.id
    ref  = message.text.split()[1] if len(message.text.split()) > 1 else None

    is_new = db.add_user(
        user_id=uid,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name,
        ref_code=ref
    )

    # Referal bonus
    if is_new and ref:
        referrer = db.get_user_by_ref(ref)
        if referrer and referrer != uid:
            db.add_bonus_days(referrer, 7)
            await bot.send_message(referrer,
                TEXTS[db.get_user_lang(referrer) or "uz"]["bonus_received"],
                parse_mode="HTML")

    # Birinchi marta → til tanlash
    if is_new or not db.get_user_lang(uid):
        await message.answer(
            TEXTS["uz"]["choose_lang"],
            parse_mode="HTML",
            reply_markup=kb_lang()
        )
    else:
        await show_menu(message.chat.id, uid)


@dp.callback_query(F.data.in_(["lang_uz", "lang_ru"]))
async def cb_lang(call: CallbackQuery):
    lang = call.data.split("_")[1]
    db.set_user_lang(call.from_user.id, lang)
    await call.answer(TEXTS[lang]["lang_set"])
    await show_menu(call.message.chat.id, call.from_user.id, call.message.message_id)


@dp.callback_query(F.data == "main_menu")
async def cb_main(call: CallbackQuery):
    await show_menu(call.message.chat.id, call.from_user.id, call.message.message_id)


@dp.callback_query(F.data == "change_lang")
async def cb_change_lang(call: CallbackQuery):
    await call.message.edit_text(
        t(call.from_user.id, "choose_lang"),
        parse_mode="HTML", reply_markup=kb_lang()
    )


@dp.callback_query(F.data == "my_sub")
async def cb_my_sub(call: CallbackQuery):
    uid = call.from_user.id
    sub = db.get_active_subscription(uid)

    if not sub:
        await call.message.edit_text(
            t(uid, "no_sub"), parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=t(uid,"buy_sub"), callback_data="buy_sub")],
                [InlineKeyboardButton(text=t(uid,"back"),    callback_data="main_menu")],
            ])
        )
        return

    # Traffic olish
    traffic_info = await vless.get_user_traffic(uid)

    text = t(uid, "sub_info").format(days    = sub["days_left"],
        devices = sub["devices"],
        server  = sub["server"],
        traffic = traffic_info.get("traffic_gb", 0)
    )
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=kb_back(uid))


@dp.callback_query(F.data == "buy_sub")
async def cb_buy(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.edit_text(
        t(uid, "choose_plan"), parse_mode="HTML", reply_markup=kb_plans(uid)
    )


@dp.callback_query(F.data.startswith("plan_"))
async def cb_plan(call: CallbackQuery):
    uid     = call.from_user.id
    plan_id = call.data.split("_")[1]
    plan    = PLANS[plan_id]
    text    = t(uid, "pay_choose").format(
        months=plan["months"], price=plan["price"], days=plan["days"]
    )
    await call.message.edit_text(
        text, parse_mode="HTML", reply_markup=kb_pay(uid, plan_id)
    )


@dp.callback_query(F.data.startswith("pay_"))
async def cb_pay(call: CallbackQuery):
    uid     = call.from_user.id
    plan_id = call.data.split("_")[1]
    plan    = PLANS[plan_id]

    # To'lov bazaga yozish
    db.create_payment(uid, plan_id, plan["price"])

    # ⚠️ HOZIRCHA: to'lovni avtomatik tasdiqlash (test rejimi)
    # Keyinroq Telegram Stars ulanganda bu qism o'zgaradi
    await call.answer(t(uid, "pay_pending"), show_alert=False)
    await call.message.edit_text(t(uid, "pay_success"), parse_mode="HTML")

    # VLESS config yaratish
    await activate_subscription(uid, plan_id, call.message.chat.id)


async def activate_subscription(uid: int, plan_id: str, chat_id: int):
    """To'lov tasdiqlangandan keyin obunani faollashtirish"""
    plan = PLANS[plan_id]

    # Bazaga obuna qo'shish
    sub_id = db.create_subscription(uid, plan["months"], plan["price"], plan["days"])

    # VLESS config yaratish
    config = await vless.create_vless_config(uid, plan["days"])

    if not config:
        await bot.send_message(chat_id, t(uid, "config_error"), parse_mode="HTML")
        return

    # UUID ni bazaga saqlash
    db.save_vless_uuid(sub_id, config["uuid"])

    # VLESS link yuborish
    await bot.send_message(
        chat_id,
        t(uid, "config_ready").format(link=config["vless_link"]),
        parse_mode="HTML",
        disable_web_page_preview=True
    )

    # QR kod yuborish
    await bot.send_photo(
        chat_id,
        photo=BufferedInputFile(config["qr_bytes"], filename="uzvpn_qr.png"),
        caption="📱 QR kod — skanerlang va ulanasiz!",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="📥 Ilovani yuklab olish" if (db.get_user_lang(uid) or "uz") == "uz"
                     else "📥 Скачать приложение",
                callback_data="install"
            )],
            [InlineKeyboardButton(text=t(uid,"back"), callback_data="main_menu")],
        ])
    )


@dp.callback_query(F.data == "install")
async def cb_install(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.edit_text(
        t(uid, "install_hint"),
        parse_mode="HTML",
        disable_web_page_preview=False,
        reply_markup=kb_back(uid)
    )


@dp.callback_query(F.data == "referral")
async def cb_referral(call: CallbackQuery):
    uid      = call.from_user.id
    bot_info = await bot.get_me()
    link     = f"https://t.me/{bot_info.username}?start={uid}"
    count    = db.get_referral_count(uid)
    await call.message.edit_text(
        t(uid, "referral_info").format(link=link, count=count),
        parse_mode="HTML", reply_markup=kb_back(uid)
    )


@dp.callback_query(F.data == "support")
async def cb_support(call: CallbackQuery):
    uid = call.from_user.id
    await call.message.edit_text(
        t(uid, "support_text"), parse_mode="HTML", reply_markup=kb_back(uid)
    )


# ================================================
# ISHGA TUSHURISH
# ================================================
async def main():
    print("✅ UzVPN Bot ishga tushdi!")
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
