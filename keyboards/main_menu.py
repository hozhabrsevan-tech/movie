from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "🔎 جستجو",
                callback_data="search"
            ),
            InlineKeyboardButton(
                "🎭 ژانر",
                callback_data="genres"
            )
        ],
        [
            InlineKeyboardButton(
                "⭐ محبوب‌ترین‌ها",
                callback_data="popular"
            )
        ],
        [
            InlineKeyboardButton(
                "❤️ علاقه‌مندی‌ها",
                callback_data="favorites"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)