import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

import keyboards
import keyboards
import data_manager
from activity_logger import logger

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    # LOGGING
    await logger.log_action(message.bot, message.from_user, "🏁 <b>Нажал START</b>")
    
    catalog = data_manager.load_data()
    await message.answer(
        "💎 <b>VIP Catalog Store</b> 💎\n\n"
        "Здесь собраны лучшие платные игры и PRO приложения, которые ты можешь получить <b>бесплатно</b>.\n\n"
        "📱 <b>Совместимость:</b> iPhone X и новее\n"
        "⚡️ <b>Без джейлбрека</b>\n\n"
        "⬇️ <b>Выбери категорию:</b>",
        reply_markup=keyboards.get_main_menu_kb(catalog),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery):
    # LOGGING
    await logger.log_action(callback.message.bot, callback.from_user, "🔙 <b>Вернулся в меню</b>")

    catalog = data_manager.load_data()
    try:
        await callback.message.edit_text(
            "💎 <b>Главное Меню</b>\n\n"
            "⬇️ <b>Выбери категорию:</b>",
            reply_markup=keyboards.get_main_menu_kb(catalog),
            parse_mode="HTML"
        )
    except Exception:
        await callback.message.answer(
            "💎 <b>Главное Меню</b>\n\n"
            "⬇️ <b>Выбери категорию:</b>",
            reply_markup=keyboards.get_main_menu_kb(catalog),
            parse_mode="HTML"
        )

@router.callback_query(F.data.startswith("cat_"))
async def cb_category(callback: CallbackQuery):
    cat_key = callback.data.split("_")[1]
    cat_data = data_manager.get_category(cat_key)
    
    # LOGGING
    if cat_data:
        await logger.log_action(callback.message.bot, callback.from_user, f"📂 Открыл категорию: <b>{cat_data['title']}</b>")
    
    if not cat_data:
        await callback.answer("⚠️ Раздел пуст или не найден", show_alert=True)
        return

    items = cat_data.get("items", [])
    if not items:
         await callback.answer("📭 Здесь пока пусто", show_alert=True)
         return

    await callback.message.edit_text(
        f"📂 <b>Раздел: {cat_data['title']}</b>\n\n"
        "🔥 <b>Выбери то, что тебе нравится:</b>",
        reply_markup=keyboards.get_category_items_kb(items, cat_key),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("item_"))
async def cb_item(callback: CallbackQuery):
    item_id = callback.data.split("_")[1]
    item = data_manager.get_item(item_id)
    
    if not item:
        await callback.answer("⚠️ Контент не найден", show_alert=True)
        return

    text = (
        f"⭐️ <b>{item['title']}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📱 <b>Тип:</b> {item['type']}\n"
        f"✅ <b>Совместимость:</b> {item['compat']}\n\n"
        f"{item['desc']}\n"
        f"━━━━━━━━━━━━━━━━━━"
    )

    await callback.message.edit_text(
        text,
        reply_markup=keyboards.get_item_kb(item['category'], item['id']),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("get_"))
async def cb_get(callback: CallbackQuery):
    item_id = callback.data.split("_")[1]
    item = data_manager.get_item(item_id)
    
    if not item:
        await callback.answer("⚠️ Ошибка: Товар не найден. Начни заново /start", show_alert=True)
        return

    # LOGGING
    await logger.log_action(callback.message.bot, callback.from_user, f"🚨 <b>Нажал ПОЛУЧИТЬ:</b> {item['title']}")

    owner = os.getenv("OWNER_USERNAME", "admin").replace("@", "").strip()
    
    await callback.answer("💎 Отличный выбор!")
    
    text = (
        f"🎁 <b>Вы выбрали:</b> {item['title']}\n\n"
        "Чтобы получить это приложение, напиши нашему менеджеру. Он всё выдаст и поможет!\n\n"
        "📢 <b>В сообщении ОБЯЗАТЕЛЬНО укажи:</b>\n"
        "• Свою модель айфона (нужен iPhone X или новее)\n"
        f"• Название: <b>{item['title']}</b>\n\n"
        f"👉 Аккаунт для связи: <b>@{owner}</b>"
    )
    
    builder = InlineKeyboardBuilder()
    builder.button(text="📩 ОТПРАВИТЬ ЗАЯВКУ", url=f"https://t.me/{owner}")
    
    await callback.message.answer(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
