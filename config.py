import os

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN پیدا نشد.")

if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY پیدا نشد.")