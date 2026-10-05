from telegram import Update
from telegram.ext import ContextTypes

from database.database import add_user
from keyboards.main_menu import main_menu


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    add_user(
        user.id,
        user.username
    )

    await update.message.reply_text(
        "🎬 به ربات معرفی فیلم و سریال خوش آمدید!\n\n"
        "یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=main_menu()
    )