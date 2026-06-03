#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎓 Курси Онлайнӣ Телеграм Бот
Забон: Тоҷикӣ
Муаллиф: Барои шумо сохта шуд
"""

import logging
import json
import os
from datetime import datetime
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# ============================================================
# ⚙️ ТАНЗИМОТ — ИНРО ИВАЗ КУНЕД
# ============================================================
BOT_TOKEN = "8925481674:AAFIuB0ugi603_N20KyeBNk2deb-xe6SLLs"
ADMIN_IDS = [5726501926]

# Маълумоти курс
KURS_NOMI = "Diamond company 💎 — Омӯзиши забонҳои хориҷӣ"
KURS_NARX = "150 сомонӣ"
KURS_MUDDAT = "3 моҳ"
MUALLIM = "Diamond company 💎"
ALOQA = "@Diamondcompany_tj"

# ============================================================
# 💾 БАЗАИ МАЪЛУМОТ (JSON файл)
# ============================================================
DB_FILE = "database.json"

def db_load():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": {}, "messages": [], "orders": []}

def db_save(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def user_register(user):
    db = db_load()
    uid = str(user.id)
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": user.id,
            "ism": user.full_name,
            "username": user.username or "—",
            "sana": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "holat": "yangi"  # yangi / xaridor
        }
        db_save(db)
        return True  # нав
    return False  # аллакай бор

def message_log(user, matn):
    db = db_load()
    db["messages"].append({
        "user_id": user.id,
        "ism": user.full_name,
        "matn": matn,
        "vaqt": datetime.now().strftime("%d.%m.%Y %H:%M")
    })
    db_save(db)

def order_add(user):
    db = db_load()
    db["orders"].append({
        "user_id": user.id,
        "ism": user.full_name,
        "username": user.username or "—",
        "kurs": KURS_NOMI,
        "narx": KURS_NARX,
        "vaqt": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "holat": "kutilmoqda"
    })
    db_save(db)

# ============================================================
# 🎹 ТУГМАҲО
# ============================================================
def main_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("📚 Дар бораи курс"), KeyboardButton("💰 Нарх ва харид")],
        [KeyboardButton("📋 Барнома"), KeyboardButton("👨‍🏫 Муаллим")],
        [KeyboardButton("❓ Саволу ҷавоб"), KeyboardButton("📞 Алоқа")]
    ], resize_keyboard=True)

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Бозгашт", callback_data="back_main")]
    ])

def buy_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Харидан мехоҳам!", callback_data="buy_now")],
        [InlineKeyboardButton("❓ Савол дорам", callback_data="ask_question")],
        [InlineKeyboardButton("🔙 Бозгашт", callback_data="back_main")]
    ])

# ============================================================
# 🤖 КОМАНДАҲО
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    is_new = user_register(user)
    message_log(user, "/start")

    # Ба ADMIN хабар дед
    if is_new:
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(
                    admin_id,
                    f"🆕 *Корбари нав!*\n"
                    f"👤 Ном: {user.full_name}\n"
                    f"🔗 Username: @{user.username or '—'}\n"
                    f"🆔 ID: `{user.id}`\n"
                    f"⏰ Вақт: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                    parse_mode="Markdown"
                )
            except:
                pass

    await update.message.reply_text(
        f"🎓 *Хуш омадед ба {KURS_NOMI}!*\n\n"
        f"Ман ботест, ки шуморо бо курс шинос мекунам.\n"
        f"Аз тугмаҳои зер истифода баред 👇",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    message_log(user, text)
    user_register(user)

    # ============ МЕНЮИ АСОСӢ ============
    if text == "📚 Дар бораи курс":
        await update.message.reply_text(
            f"📚 *{KURS_NOMI}*\n\n"
            f"✅ Аз нол то сатҳи миёна\n"
            f"✅ Дарсҳо ба забони тоҷикӣ\n"
            f"✅ Вазифаҳои амалӣ\n"
            f"✅ Тасдиқнома пас аз хатм\n"
            f"✅ Гурӯҳи дастгирӣ дар Telegram\n\n"
            f"⏱ Муддат: {KURS_MUDDAT}\n"
            f"💰 Нарх: {KURS_NARX}",
            parse_mode="Markdown",
            reply_markup=buy_keyboard()
        )

    elif text == "💰 Нарх ва харид":
        await update.message.reply_text(
            f"💰 *Нарх ва тарзи харид*\n\n"
            f"📦 Нарх: *{KURS_NARX}*\n\n"
            f"*Чӣ тавр харидан мумкин аст:*\n"
            f"1️⃣ Тугмаи 'Харидан мехоҳам' зер кунед\n"
            f"2️⃣ Маблағро ба картаи мо интиқол диҳед\n"
            f"3️⃣ Скриншот фиристед — дастрасӣ мегиред!\n\n"
            f"💳 Рақами карта: *1234 5678 9012 3456*\n"
            f"👤 Соҳиб: Алишер Раҳимов",
            parse_mode="Markdown",
            reply_markup=buy_keyboard()
        )

    elif text == "📋 Барнома":
        await update.message.reply_text(
            f"📋 *Барномаи курс*\n\n"
            f"*📅 Ҳафтаи 1:*\n"
            f"  • Асосҳои Python\n"
            f"  • Намудҳои маълумот\n"
            f"  • Шартҳо ва давраҳо\n\n"
            f"*📅 Ҳафтаи 2:*\n"
            f"  • Функсияҳо\n"
            f"  • Рӯйхатҳо ва луғатҳо\n"
            f"  • Кор бо файлҳо\n\n"
            f"*📅 Ҳафтаи 3:*\n"
            f"  • Барномасозии объектӣ\n"
            f"  • Хатогирӣ ва дастгирӣ\n"
            f"  • Модулҳо\n\n"
            f"*📅 Ҳафтаи 4:*\n"
            f"  • Лоиҳаи ниҳоӣ\n"
            f"  • Тасдиқнома\n"
            f"  • Дастгирии минбаъда",
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )

    elif text == "👨‍🏫 Муаллим":
        await update.message.reply_text(
            f"👨‍🏫 *{MUALLIM}*\n\n"
            f"🎓 Таҷриба: 7 сол\n"
            f"💼 Лоиҳаҳо: 50+\n"
            f"👥 Хонандагон: 300+\n\n"
            f"Мутахассиси Python, Django, ва Machine Learning.\n"
            f"Ҳар як хонандаро шахсан дастгирӣ мекунад.",
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )

    elif text == "❓ Саволу ҷавоб":
        await update.message.reply_text(
            f"❓ *Саволҳои зуд-зуд пурсидашаванда*\n\n"
            f"*Оё таҷриба лозим аст?*\n"
            f"➡️ Не, курс барои мубтадиён аст\n\n"
            f"*Дарсҳо чӣ вақт мешаванд?*\n"
            f"➡️ Онлайн, ҳар вақт қулай\n\n"
            f"*Тасдиқнома медиҳед?*\n"
            f"➡️ Бале, пас аз хатм\n\n"
            f"*Агар савол монд чӣ?*\n"
            f"➡️ Дар гурӯҳи Telegram ҷавоб мегирем\n\n"
            f"*Компютер лозим аст?*\n"
            f"➡️ Бале, ё телефон (аммо компютер беҳтар аст)",
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )

    elif text == "📞 Алоқа":
        await update.message.reply_text(
            f"📞 *Бо мо алоқа гиред*\n\n"
            f"👤 Муаллим: {ALOQA}\n"
            f"⏰ Кор мекунад: 9:00 — 21:00\n\n"
            f"Ё саволи худро инҷо нависед — дар ҷараёни 1 соат ҷавоб мегирем! 💬",
            parse_mode="Markdown",
            reply_markup=back_keyboard()
        )

    else:
        # Паёми ихтиёрӣ — ба ADMIN пешниҳод кунед
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(
                    admin_id,
                    f"💬 *Паём аз корбар:*\n"
                    f"👤 {user.full_name} (@{user.username or '—'})\n"
                    f"🆔 ID: `{user.id}`\n"
                    f"📝 Паём: {text}\n\n"
                    f"Ҷавоб барои фиристодан:\n"
                    f"`/reply {user.id} ҷавоби шумо`",
                    parse_mode="Markdown"
                )
            except:
                pass

        await update.message.reply_text(
            "✅ Паёми шумо қабул шуд!\n"
            "Дар ҷараёни 1 соат ҷавоб мегирем. 😊",
            reply_markup=main_keyboard()
        )

# ============================================================
# 🔘 CALLBACK ТУГМАҲО
# ============================================================
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    if query.data == "buy_now":
        order_add(user)
        # Ба ADMIN хабар дед
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(
                    admin_id,
                    f"🛒 *ФАРМОИШИ НАВ!*\n"
                    f"👤 {user.full_name} (@{user.username or '—'})\n"
                    f"🆔 ID: `{user.id}`\n"
                    f"📦 Курс: {KURS_NOMI}\n"
                    f"💰 Нарх: {KURS_NARX}\n"
                    f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                    parse_mode="Markdown"
                )
            except:
                pass

        await query.edit_message_text(
            f"🎉 *Хурсандем!*\n\n"
            f"Шумо мехоҳед курсро харед.\n\n"
            f"*Тарзи пардохт:*\n"
            f"💳 Карта: 1234 5678 9012 3456\n"
            f"💰 Маблағ: {KURS_NARX}\n\n"
            f"Пас аз пардохт скриншот ба {ALOQA} фиристед!\n"
            f"Дарсҳо дарҳол мекушоянд ✅",
            parse_mode="Markdown"
        )

    elif query.data == "ask_question":
        await query.edit_message_text(
            "💬 Саволи худро нависед, мо ҷавоб медиҳем!\n"
            f"Ё мустақиман бо {ALOQA} алоқа гиред.",
            parse_mode="Markdown"
        )

    elif query.data == "back_main":
        await query.edit_message_text(
            "🏠 Менюи асосӣ 👇",
        )

# ============================================================
# 👑 АДМИН КОМАНДАҲО
# ============================================================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return

    db = db_load()
    users = len(db["users"])
    messages = len(db["messages"])
    orders = len(db["orders"])

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"👥 Корбарон ({users})", callback_data="adm_users")],
        [InlineKeyboardButton(f"🛒 Фармоишҳо ({orders})", callback_data="adm_orders")],
        [InlineKeyboardButton(f"💬 Паёмҳо ({messages})", callback_data="adm_messages")],
        [InlineKeyboardButton("📢 Ҳамаро хабар дидан", callback_data="adm_broadcast")]
    ])

    await update.message.reply_text(
        f"👑 *ПАНЕЛИ АДМИН*\n\n"
        f"📊 Омор:\n"
        f"👥 Корбарон: {users}\n"
        f"🛒 Фармоишҳо: {orders}\n"
        f"💬 Паёмҳо: {messages}",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ҷавоб ба корбар: /reply 123456789 матн"""
    if update.effective_user.id not in ADMIN_IDS:
        return
    try:
        parts = update.message.text.split(" ", 2)
        user_id = int(parts[1])
        javob = parts[2]
        await context.bot.send_message(user_id, f"📩 *Ҷавоби муаллим:*\n\n{javob}", parse_mode="Markdown")
        await update.message.reply_text("✅ Ҷавоб фиристода шуд!")
    except:
        await update.message.reply_text("❌ Формат: /reply 123456789 матни ҷавоб")

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/broadcast матн — ба ҳама фиристад"""
    if update.effective_user.id not in ADMIN_IDS:
        return
    try:
        matn = update.message.text.split(" ", 1)[1]
        db = db_load()
        ok = 0
        for uid in db["users"]:
            try:
                await context.bot.send_message(int(uid), matn)
                ok += 1
            except:
                pass
        await update.message.reply_text(f"✅ {ok} нафар хабар гирифт!")
    except:
        await update.message.reply_text("❌ Формат: /broadcast матни хабар")

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.from_user.id not in ADMIN_IDS:
        return
    await query.answer()
    db = db_load()

    if query.data == "adm_users":
        if not db["users"]:
            await query.edit_message_text("Ҳанӯз корбар нест.")
            return
        matn = "👥 *КОРБАРОН:*\n\n"
        for u in list(db["users"].values())[-20:]:
            matn += f"• {u['ism']} (@{u['username']}) — {u['sana']}\n"
        await query.edit_message_text(matn, parse_mode="Markdown")

    elif query.data == "adm_orders":
        if not db["orders"]:
            await query.edit_message_text("Ҳанӯз фармоиш нест.")
            return
        matn = "🛒 *ФАРМОИШҲО:*\n\n"
        for o in db["orders"][-20:]:
            matn += f"• {o['ism']} (@{o['username']})\n  💰 {o['narx']} — {o['vaqt']}\n\n"
        await query.edit_message_text(matn, parse_mode="Markdown")

    elif query.data == "adm_messages":
        if not db["messages"]:
            await query.edit_message_text("Ҳанӯз паём нест.")
            return
        matn = "💬 *ОХИРИН ПАЁМҲО:*\n\n"
        for m in db["messages"][-15:]:
            matn += f"• {m['ism']}: {m['matn']} ({m['vaqt']})\n"
        await query.edit_message_text(matn, parse_mode="Markdown")

    elif query.data == "adm_broadcast":
        await query.edit_message_text(
            "📢 Барои ҳамаро хабар додан нависед:\n\n`/broadcast матни хабари шумо`",
            parse_mode="Markdown"
        )

# ============================================================
# 🚀 БОТРО ОҒОЗ КУНЕД
# ============================================================
logging.basicConfig(level=logging.INFO)

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Командаҳо
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin_panel))
app.add_handler(CommandHandler("reply", admin_reply))
app.add_handler(CommandHandler("broadcast", admin_broadcast))

# Паёмҳо
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Callback тугмаҳо
app.add_handler(CallbackQueryHandler(admin_callback, pattern="^adm_"))
app.add_handler(CallbackQueryHandler(handle_callback))

print("🤖 Бот оғоз ёфт!")
app.run_polling()
