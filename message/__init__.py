from azure.functions import HttpResponse, Out
import logging
import json
import os
from azure.messaging.webpubsubservice import WebPubSubServiceClient

async def main(request) -> dict:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(request)
    request = json.loads(json.loads(request)['data'])
    user_id = request['userId']
    message = request['text']
    connection_string = os.environ.get("WebPubSubConnectionString")
    service = WebPubSubServiceClient.from_connection_string(connection_string, hub='simplechat')
    service.send_to_all({'userId': user_id, 'text': message})