from azure.messaging.webpubsubservice import WebPubSubServiceClient
from helpers import database
import azure.functions as func
import json
import logging
import os
from helpers import cognitive_services

def send_message(connection_string, data:database.DataTuple): 
    service: WebPubSubServiceClient = WebPubSubServiceClient.from_connection_string(connection_string, hub='simplechat')
    new_message = {
        'userId': f'User {data.source_user}', 
        'original': data.message,
        'translated': '',
    }
    if data.original_language != data.language:
        new_message['translated'] = cognitive_services.translate(data.message, data.original_language, data.language),
    logging.info(f'The full message is: {new_message}')
    service.send_to_user(data.target_user, new_message)

def main(event: func.EventGridEvent):

    logging.info('Python EventGrid trigger processed an event: %s', event.get_json())
    data: database.DataTuple = database.DataTuple(*event.get_json())
    connection_string = os.environ.get("WebPubSubConnectionString")
    send_message(connection_string, data)

