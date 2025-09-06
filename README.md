# Telegram Bot

This is a Telegram bot built with Telethon that automates payments and scheduled messages.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt

API_ID=your_api_id
API_HASH=your_api_hash

python bot.py


setp <peer> <msgid> – set the target message

settime HH:MM:SS – schedule the task in Tehran time