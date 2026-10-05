from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def movie_menu(movie_id, is_saved=False):

    save_text = "❌ حذف از علاقه‌مندی" if is_saved else "⭐ ذخیره"

    keyboard = [
        [
            InlineKeyboardButton(
                "🎞 تریلر",
                callback_data=f"trailer_{movie_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🎬 فیلم‌های مشابه",
                callback_data=f"similar_{movie_id}"
            )
        ],
        [
            InlineKeyboardButton(
                save_text,
                callback_data=f"favorite_{movie_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="back_main"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)