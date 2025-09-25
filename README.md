# INVIS Counter Telegram Bot

Телеграм-бот для подсчета переводов из CardXabar, Humo, Click, Payme и т.д.

## 🚀 Запуск 

1. Подключи GitHub репозиторий.
2. Добавь переменную окружения:
   ```
   BOT_TOKEN=ваш_токен_бота
   ```
3. Railway сам выполнит `start.sh` и запустит бота 24/7.

## 📂 Локальный запуск

```bash
pip install -r requirements.txt
echo BOT_TOKEN=ваш_токен > .env
python invis-counter.py
```

## 🔐 Безопасность

Не коммить `.env`, используй `.env.example` как шаблон.
