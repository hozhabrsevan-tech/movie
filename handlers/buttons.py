import logging

from telegram import Update
from telegram.ext import ContextTypes

from database.database import (
    add_favorite,
    remove_favorite,
    get_favorites,
    is_favorite
)

from keyboards.main_menu import main_menu
from keyboards.movie_menu import movie_menu
from handlers.movie import send_movie


logger = logging.getLogger(__name__)


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    data = query.data

    logger.debug(
        "Button clicked: %s | User: %s",
        data,
        query.from_user.id
    )

    # =========================
    # Main Menu
    # =========================

    if data == "search":

        await query.message.reply_text(
            "🔎 نام فیلم یا سریال را ارسال کنید:"
        )

    elif data == "genres":

        await query.message.reply_text(
            "🎭 بخش ژانر به‌زودی اضافه می‌شود."
        )

    elif data == "popular":

        await query.message.reply_text(
            "⭐ بخش محبوب‌ترین‌ها به‌زودی اضافه می‌شود."
        )

    elif data == "favorites":

        await show_favorites(query)

    # =========================
    # Favorite
    # =========================

    elif data.startswith("favorite_"):

        movie_id = int(
            data.split("_")[1]
        )

        user_id = query.from_user.id

        if is_favorite(user_id, movie_id):

            remove_favorite(
                user_id,
                movie_id
            )

            await query.answer(
                "❌ از علاقه‌مندی‌ها حذف شد"
            )

        else:

            # فعلاً عنوان را از caption می‌گیریم
            movie_title = query.message.caption.split("\n")[0]

            add_favorite(
                user_id,
                movie_id,
                movie_title
            )

            await query.answer(
                "⭐ به علاقه‌مندی‌ها اضافه شد"
            )

        saved = is_favorite(
            user_id,
            movie_id
        )

        await query.edit_message_reply_markup(
            reply_markup=movie_menu(
                movie_id,
                saved
            )
        )

    # =========================
    # Similar
    # =========================

    elif data.startswith("similar_"):

        await query.message.reply_text(
            "🎬 بخش فیلم‌های مشابه به‌زودی اضافه می‌شود."
        )

    # =========================
    # Trailer
    # =========================

    elif data.startswith("trailer_"):

        await query.message.reply_text(
            "🎞 بخش تریلر به‌زودی اضافه می‌شود."
        )

    # =========================
    # Back
    # =========================

    elif data == "back_main":

        await query.message.reply_text(
            "🎬 منوی اصلی:",
            reply_markup=main_menu()
        )


async def show_favorites(query):

    user_id = query.from_user.id

    favorites = get_favorites(user_id)

    if not favorites:

        await query.message.reply_text(
            "❤️ هنوز فیلمی ذخیره نکرده‌اید."
        )

        return

    text = "❤️ علاقه‌مندی‌های شما:\n\n"

    for movie_id, movie_title in favorites:

        text += f"🎬 {movie_title}\n"

    await query.message.reply_text(text)