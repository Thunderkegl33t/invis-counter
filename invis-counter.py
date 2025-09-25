from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re
import unicodedata

TOKEN = '7333435842:AAH5Kb5jk2QO-ocoTLDR_DFHn1vfk3ZQdNI'  # ← вставь сюда токен от @BotFather

total_sum = 0

def clean_spaces(s):
    return ''.join(ch if not unicodedata.category(ch).startswith('Z') else ' ' for ch in s)

def normalize_amount(raw):
    # Удаляет все пробелы и невидимые символы
    raw = re.sub(r'[\s\u00A0\u202F\u2009\u2007\xa0]', '', raw)

    # Формат: 13.000,00 → 13000.00
    if '.' in raw and ',' in raw and raw.find('.') < raw.find(','):
        raw = raw.replace('.', '').replace(',', '.')

    # Формат: 38,000.00 → 38000.00
    elif ',' in raw and '.' in raw and raw.find(',') < raw.find('.'):
        raw = raw.replace(',', '')

    # Формат: 60 000,00 → 60000.00
    elif ',' in raw and '.' not in raw:
        raw = raw.replace(',', '.')

    try:
        return int(round(float(raw)))
    except:
        return 0

def extract_amount(text):
    text = clean_spaces(text)

    # ❌ Игнорируем отменённые транзакции (Payme и др.)
    if "отмен" in text.lower():   # ловит "Отменён", "Отмена" и т.п.
        return 0

    lines = text.splitlines()

    # ✅ PAYNET: ищем "Tranzaksiya summasi" и вытаскиваем число перед "so`m"
    paynet_match = re.search(r'Tranzaksiya\s+summasi:\s*([\d\s.,]+)', text, re.IGNORECASE)
    if paynet_match:
        return normalize_amount(paynet_match.group(1))

    # ✅ CLICK: строго — если есть +998 и строк минимум 5
    if '+998' in text and len(lines) >= 5:
        match = re.search(r'([\d\s.,]+)', lines[4])
        if match:
            return normalize_amount(match.group(1))

    # 1. CardXabar, Humo — по ➕
    match = re.search(r'[+➕]\s*([\d\s.,]+)', text)
    if match:
        return normalize_amount(match.group(1))

    # 2. Payme — если есть 'сум' и нет номера
    for line in lines:
        if 'сум' in line.lower() and '+998' not in line and '+' not in line:
            match = re.search(r'([\d\s.,]+)', line)
            if match:
                return normalize_amount(match.group(1))

    return 0

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global total_sum
    text = update.message.text
    amount = extract_amount(text)
    if amount > 0:
        total_sum += amount
        await update.message.reply_text(f"{amount:,}".replace(",", " "))
    else:
        await update.message.reply_text("❌ Не удалось извлечь сумму.")

async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global total_sum
    await update.message.reply_text(f"Общая сумма: {total_sum:,}".replace(",", " "))
    total_sum = 0
    await update.message.reply_text("🔄 Счетчик сброшен.")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global total_sum
    total_sum = 0
    await update.message.reply_text("🔄 Сумма сброшена.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Пересылай сюда пополнения от CardXabar, Humo, Payme, Click, Paynet.\n"
        "Суммы будут учтены и отображены.\n\n"
        "📌 Команды:\n"
        "/total — показать и сбросить сумму\n"
        "/reset — сброс вручную"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("total", total))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущен.")
    app.run_polling()
