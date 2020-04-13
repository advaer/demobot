import os

from telegram import Bot
from telegram.ext import Dispatcher

from . import handlers


def setup():
    # Create bot, update queue and dispatcher instances
    bot = Bot(os.getenv("TELEGRAM_TOKEN"))

    dispatcher = Dispatcher(bot, None, workers=0)

    # Register handlers here
    dispatcher.add_handler(handlers.echo_handler)
    dispatcher.add_handler(handlers.unknown_handler)

    return dispatcher
