from azure.functions import HttpResponse, Out
import logging
import json
import os
from azure.messaging.webpubsubservice import WebPubSubServiceClient
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

async def main(request) -> dict:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(request)
    request = json.loads(request)
    user_id = request['connectionContext']['userId']
    message = request['data']
    connection_string = os.environ.get("WebPubSubConnectionString")
    service = WebPubSubServiceClient.from_connection_string(connection_string, hub='simplechat')
    service.send_to_all({'userId': user_id, 'text': message})