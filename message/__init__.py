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

table = database.Database()
# Use the HTTP trigger decorator
async def main(request:str) -> func.HttpResponse:
    logging.info(f'Python webpubsub request: {request}')
    params = json.loads(json.loads(request)['data'])
    session_id = params['sessionId']
    user_id = params['userId']
    message = params['text']
    source_language = params['language']
    blob = ''
    if 'uri' in params:
        blob = params['uri'] if 'uri' in params else ''
        url = 'https://chatwithfriendsffmpeg.azurewebsites.net/api/ConvertFFMPeg'
        # Define the file paths of the WebM input file anurl = ''d Ogg output file
        stream = requests.get(params['uri']).content
        response = requests.post(url, files={"file": stream})
        blob = response.json()['value']['blobName']
        logging.info(f'Output blob name {blob}')

    # TODO: Investigate how to store chat state between sessions
    for target_user, target_language in table.get_all_user_languages(session_id=session_id):
        data = database.DataTuple(
            session_id = session_id,
            source_user = user_id,
            target_user = target_user,
            source_language = source_language,
            target_language = target_language,
            message = message,
            blob = blob,
        )
        create_event(data)