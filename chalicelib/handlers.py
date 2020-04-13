from telegram.ext import CommandHandler, MessageHandler, Filters

from . import commands

echo_handler = MessageHandler(Filters.text, commands.echo)
unknown_handler = MessageHandler(Filters.command, commands.unknown)
