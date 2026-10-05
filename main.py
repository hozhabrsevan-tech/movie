import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN

from database.database import create_tables

from handlers.start import start
from handlers.buttons import button_handler
from handlers.movie import search_movie_handler

from utils.logger import setup_logging


logger = setup_logging()


async def error_handler(
    update,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.exception(
        "Exception while handling update:",
        exc_info=context.error
    )


def main():

    logger.info("Starting Movie Bot...")

    create_tables()

    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    # /start
    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # Inline Buttons
    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    # Movie Search
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            search_movie_handler
        )
    )

    # Error Handler
    application.add_error_handler(
        error_handler
    )

    logger.info(
        "Movie Bot is running..."
    )

    application.run_polling()


if __name__ == "__main__":
    main()