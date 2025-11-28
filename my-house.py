import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

logging.basicConfig(level=logging.INFO)

TOKEN = "8003812615:AAG1F0j3sSzTG_eqAMoyqA4eUifqEHMCjsU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

URL_RENT = "https://t.me/maklerzemli5"
URL_HOUSE = "https://t.me/maklerzemli4"
URL_DACHA = "https://t.me/maklerzemli1"
URL_LAND = "https://t.me/maklerzemli3"
URL_FLATS = "https://t.me/maklerzemli2"

# -------------------------------------------------------------
# КОНТАКТЫ
# -------------------------------------------------------------
CONTACT_TEXT_RU = "📞 Контакты:\n\nTelegram: @dedok221\nТелефон: +998 99 666 67 74"
CONTACT_TEXT_UZ = "📞 Kontaktlar:\n\nTelegram: @dedok221\nTelefon: +998 99 666 67 74"

# -------------------------------------------------------------
# ЯЗЫКИ
# -------------------------------------------------------------
def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O‘zbekcha", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        ]
    ])

# -------------------------------------------------------------
# ГЛАВНОЕ МЕНЮ
# -------------------------------------------------------------
def main_keyboard_ru():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Аренды", callback_data="cat_rent:ru")],
        [InlineKeyboardButton(text="🏡 Дома", callback_data="cat_house:ru")],
        [InlineKeyboardButton(text="🌴 Дачи", callback_data="cat_dacha:ru")],
        [InlineKeyboardButton(text="🌍 Земли", callback_data="cat_land:ru")],
        [InlineKeyboardButton(text="🏢 Квартиры", callback_data="cat_flats:ru")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts:ru")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_lang")]
    ])

def main_keyboard_uz():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Ijarar", callback_data="cat_rent:uz")],
        [InlineKeyboardButton(text="🏡 Uylar", callback_data="cat_house:uz")],
        [InlineKeyboardButton(text="🌴 Dachalar", callback_data="cat_dacha:uz")],
        [InlineKeyboardButton(text="🌍 Yerlar", callback_data="cat_land:uz")],
        [InlineKeyboardButton(text="🏢 Kvartiralar", callback_data="cat_flats:uz")],
        [InlineKeyboardButton(text="📞 Kontaktlar", callback_data="contacts:uz")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_lang")]
    ])

# -------------------------------------------------------------
# НАЗАД
# -------------------------------------------------------------
def back_button_ru():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_menu:ru")]
    ])

def back_button_uz():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_menu:uz")]
    ])

# -------------------------------------------------------------
# START
# -------------------------------------------------------------
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Выберите язык / Tilni tanlang:",
        reply_markup=language_keyboard()
    )

# -------------------------------------------------------------
# ВЫБОР ЯЗЫКА
# -------------------------------------------------------------
@dp.callback_query(F.data.in_({"lang_ru", "lang_uz"}))
async def on_language_selected(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]

    if lang == "ru":
        await callback.message.edit_text(
            "Добро пожаловать! Выберите категорию:",
            reply_markup=main_keyboard_ru()
        )
    else:
        await callback.message.edit_text(
            "Xush kelibsiz! Bo‘limni tanlang:",
            reply_markup=main_keyboard_uz()
        )

    await callback.answer()

# -------------------------------------------------------------
# НАЗАД К ВЫБОРУ ЯЗЫКА
# -------------------------------------------------------------
@dp.callback_query(F.data == "back_lang")
async def back_to_language(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите язык / Tilni tanlang:",
        reply_markup=language_keyboard()
    )
    await callback.answer()

# -------------------------------------------------------------
# КОНТАКТЫ
# -------------------------------------------------------------
@dp.callback_query(F.data.startswith("contacts"))
async def show_contacts(callback: types.CallbackQuery):
    _, lang = callback.data.split(":")

    if lang == "ru":
        await callback.message.edit_text(
            CONTACT_TEXT_RU,
            reply_markup=back_button_ru()
        )
    else:
        await callback.message.edit_text(
            CONTACT_TEXT_UZ,
            reply_markup=back_button_uz()
        )

    await callback.answer()

# -------------------------------------------------------------
# ВЫБОР КАТЕГОРИИ — ССЫЛКА БЕЗ КНОПКИ
# -------------------------------------------------------------
@dp.callback_query(F.data.startswith("cat_"))
async def on_category_selected(callback: types.CallbackQuery):
    payload = callback.data

    try:
        cat_part, lang = payload.split(":")
    except ValueError:
        await callback.message.edit_text(
            "Выберите язык / Tilni tanlang:",
            reply_markup=language_keyboard()
        )
        return

    # Категории
    if cat_part == "cat_rent":
        url = URL_RENT
        title_ru = "🏠 Аренды"
        title_uz = "🏠 Ijaralar"
    elif cat_part == "cat_house":
        url = URL_HOUSE
        title_ru = "🏡 Дома"
        title_uz = "🏡 Uylar"
    elif cat_part == "cat_dacha":
        url = URL_DACHA
        title_ru = "🌴 Дачи"
        title_uz = "🌴 Dachalar"
    elif cat_part == "cat_land":
        url = URL_LAND
        title_ru = "🌍 Земли"
        title_uz = "🌍 Yerlar"
    elif cat_part == "cat_flats":
        url = URL_FLATS
        title_ru = "🏢 Квартиры"
        title_uz = "🏢 Kvartiralar"

    # Выводим текст + ссылку + кнопку Назад
    if lang == "ru":
        text = f"{title_ru}\n\n➡️ {url}"
        markup = back_button_ru()
    else:
        text = f"{title_uz}\n\n➡️ {url}"
        markup = back_button_uz()

    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()

# -------------------------------------------------------------
# НАЗАД К КАТЕГОРИЯМ
# -------------------------------------------------------------
@dp.callback_query(F.data.startswith("back_menu"))
async def on_back(callback: types.CallbackQuery):
    try:
        _, lang = callback.data.split(":")
    except ValueError:
        lang = "ru"

    if lang == "ru":
        await callback.message.edit_text(
            "Выберите категорию:",
            reply_markup=main_keyboard_ru()
        )
    else:
        await callback.message.edit_text(
            "Bo‘limni tanlang:",
            reply_markup=main_keyboard_uz()
        )

    await callback.answer()

# -------------------------------------------------------------
# ЗАПУСК
# -------------------------------------------------------------
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("Ошибка при запуске:", e)
    input("Нажмите Enter чтобы закрыть окно...")