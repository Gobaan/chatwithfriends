from azure.messaging.webpubsubservice import WebPubSubServiceClient
import azure.functions as func
import logging
import os
from helpers import database
from helpers import translation_controller

def send_message(connection_string, data:database.DataTuple): 
    service: WebPubSubServiceClient = WebPubSubServiceClient.from_connection_string(connection_string, hub='simplechat')
    new_message = translation_controller.data_to_translation(data)
    service.send_to_user(
        database.get_webosocket_id(data.target_user, data.session_id), 
        new_message
    )

def main(event: func.EventGridEvent):
    logging.info('Python EventGrid trigger processed an event: %s', event.get_json())
    data: database.DataTuple = database.DataTuple(*event.get_json())
    connection_string = os.environ.get("WebPubSubConnectionString")
    send_message(connection_string, data)

