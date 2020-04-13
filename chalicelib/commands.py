from chalicelib import lex

def echo(bot, update):
    lx = lex.BotProcessing()
    response_text = lx.respond(user_id=update.message.chat_id, text=update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=response_text)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand")
