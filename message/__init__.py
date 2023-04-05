import logging
import json
import os
import azure.functions as func
from helpers import database
import requests
import datetime

#TODO load keys from azure
def create_event(data):
    topic_endpoint = os.environ['AzureEventGridTopicEndpoint']
    topic_key = os.environ['AzureEventGridTopicKey']

    # Create a new event to add to the topic
    event = {
        'id': '1',
        'subject': "The message",
        'eventType': 'MessageRecieved',
        "eventTime": str(datetime.datetime.now()),
        'data': data,
    }

    # Send the event to the Event Grid topic using the REST API
    response = requests.post(
        topic_endpoint,
        headers={
            'aeg-sas-key': topic_key,
            'Content-Type': 'application/json'
        },
        json=[event]
    )

    # Return a response indicating whether the event was successfully added
    if response.status_code == 200:
        logging.info(f"Event added: {json.dumps(event)}")
    else:
        logging.error(f"Error adding event: {response.text}")

table_client = database.initialize_db()
# Use the HTTP trigger decorator
async def main(request:str) -> func.HttpResponse:
    logging.info(f'Python webpubsub request: {request}')
    params = json.loads(json.loads(request)['data'])
    session_id = params['sessionId']
    user_id = params['userId']
    message = params['text']
    source_language = params['language']

    # TODO: Investigate how to store chat state between sessions
    for user, language in database.get_all_user_languages(table_client, session_id=session_id):
        data = database.DataTuple(
            session_id = session_id,
            source_user = user_id,
            target_user = user,
            original_language = source_language,
            language = language,
            message = message,
            blob = '',
        )
        create_event(data)