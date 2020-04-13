import json
import logging
import os
from pathlib import Path

import boto3
from chalice import Chalice, Response
from dotenv import load_dotenv
from telegram import Bot, Update

from chalicelib.config import setup

app = Chalice(app_name='demobot')
app.log.setLevel(logging.DEBUG)

env_path = Path('.') / 'chalicelib/.env'
load_dotenv(dotenv_path=env_path)

bot = Bot(os.getenv("TELEGRAM_TOKEN"))


@app.lambda_function()
def book_hotel_fulfillment(event, context):
    slots = event.get('currentIntent').get('slots')

    city = slots.get("destinationCity")
    check_in_date = slots.get("checkInDate")
    room_type = slots.get("roomType")

    # Implement any business logic here

    return {
        "sessionAttributes": {
            "city": city,
            "check_in_date": check_in_date,
            "room_type": room_type
        },
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": f"Fulfillment is done! {room_type} hotel room in {city} "
                           f"for {check_in_date} has been booked for you!"
            }
        }
    }


@app.lambda_function()
def weather_fulfillment(event, context):
    session = event.get('sessionAttributes')

    city = session.get("city")
    check_in_date = session.get("check_in_date")

    # Implement any business logic here

    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": f"The weather in {city} on {check_in_date} will be awesome!"
            }
        }
    }


@app.route('/telegram/{api_key}', methods=['POST'], content_types=['application/json'])
def telegram(api_key):
    app.log.debug(f"Validating API Key")
    if api_key != os.getenv('API_KEY'):
        app.log.debug(f"API Key is invalid")
        return Response(
            {"message": "Unauthorized"},
            status_code=401
        )
    app.log.debug(f"API Key is valid")

    app.log.debug(f"Pushing request to SQS")
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl=f"{os.getenv('SQS_URL')}/{os.getenv('REQUEST_QUEUE')}",
        MessageBody=app.current_request.raw_body.decode()
    )
    app.log.debug(f"Response 200 OK to Telegram")
    return Response(
        {"message": "Request received"},
        status_code=200
    )


@app.on_sqs_message(queue=os.getenv("REQUEST_QUEUE"), batch_size=1)
def handle_sqs_message(event):
    dispatcher = setup()

    for record in event:
        app.log.debug(f"Received message. Type: {type(record.body)}. Content: {record.body}")
        json_body = json.loads(record.body)
        update = Update.de_json(json_body, dispatcher.bot)
        dispatcher.process_update(update)
        app.log.debug(f"Message sent to Telegram")

    return {"status": "Messages sent"}

