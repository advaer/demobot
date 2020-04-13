import os

import boto3


class BotProcessing:

    @staticmethod
    def respond(user_id, text):
        client = boto3.client('lex-runtime')
        response = client.post_text(
            botName=os.getenv("LEX_BOT_NAME"),
            botAlias=os.getenv("LEX_BOT_ALIAS"),
            userId=str(user_id),
            inputText=text
        )

        return response.get("message")
