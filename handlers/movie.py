import logging
import requests

from telegram import Update
from telegram.ext import ContextTypes

from config import TMDB_API_KEY
from database.database import is_favorite
from keyboards.movie_menu import movie_menu


logger = logging.getLogger(__name__)


TMDB_BASE_URL = "https://api.themoviedb.org/3"


def search_movie(movie_name):

    url = f"{TMDB_BASE_URL}/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_name,
        "language": "en-US"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_movie_details(movie_id):

    url = f"{TMDB_BASE_URL}/movie/{movie_id}"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


async def search_movie_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    movie_name = update.message.text.strip()

    logger.debug(
        "Movie search: %s | User: %s",
        movie_name,
        update.effective_user.id
    )

    try:

        data = search_movie(movie_name)

    except requests.RequestException:

        logger.exception("TMDB request failed")

        await update.message.reply_text(
            "❌ خطا در ارتباط با سرویس فیلم.\n"
            "لطفاً دوباره تلاش کنید."
        )

        return

    results = data.get("results", [])

    if not results:

        await update.message.reply_text(
            "❌ فیلمی با این نام پیدا نشد."
        )

        return

    movie = results[0]

    await send_movie(
        update,
        movie["id"]
    )


async def send_movie(
    update,
    movie_id
):

    try:

        movie = get_movie_details(movie_id)

    except requests.RequestException:

        logger.exception("Could not get movie details")

        await update.effective_message.reply_text(
            "❌ دریافت اطلاعات فیلم با مشکل مواجه شد."
        )

        return

    user_id = update.effective_user.id

    saved = is_favorite(
        user_id,
        movie_id
    )

    title = movie.get("title", "Unknown")

    release_date = movie.get(
        "release_date",
        ""
    )

    year = release_date[:4] if release_date else "نامشخص"

    rating = movie.get(
        "vote_average",
        0
    )

    overview = movie.get(
        "overview",
        "خلاصه‌ای موجود نیست."
    )

    genres = movie.get(
        "genres",
        []
    )

    genre_names = ", ".join(
        genre["name"]
        for genre in genres
    )

    poster_path = movie.get("poster_path")

    text = (
        f"🎬 {title}\n\n"
        f"⭐ امتیاز: {rating:.1f}\n"
        f"📅 سال: {year}\n"
        f"🎭 ژانر: {genre_names}\n\n"
        f"📝 خلاصه:\n"
        f"{overview}"
    )

    reply_markup = movie_menu(
        movie_id,
        saved
    )

    if poster_path:

        poster_url = (
            "https://image.tmdb.org/t/p/w500"
            + poster_path
        )

        await update.effective_message.reply_photo(
            photo=poster_url,
            caption=text,
            reply_markup=reply_markup
        )

    else:

        await update.effective_message.reply_text(
            text,
            reply_markup=reply_markup
        )