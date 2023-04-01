import azure.functions as func
from helpers import database
import os
from azure.messaging.webpubsubservice import WebPubSubServiceClient
import uuid 

# Use the HTTP trigger decorator
def main(req: func.HttpRequest, res: func.Out[func.HttpResponse]) -> None:
    if req.params['sessionId'] != 'null':
        session_id = req.params['sessionId']
    else:
        session_id = str(uuid.uuid4())

    if req.params['userId'] != 'null':
        user_id = req.params['userId']
        language = database.get_user_language(database.table_client, user_id, session_id)
    else:
        user_id = f'{database.increment_counter(database.table_client, session_id)}'
        language = 'en'
        database.set_preferences(database.table_client, user_id, {'language': 'en'}, session_id)

    client: WebPubSubServiceClient = WebPubSubServiceClient.from_connection_string(os.environ['WebPubSubConnectionString'], os.environ['AzureWebJobsWebPubSubHub'])
    # Connect to the WebPubSub service with the user ID query parameter
    access_token = client.get_client_access_token(user_id = database.get_webosocket_id(user_id, session_id))
    padding = os.environ['CheckSumKey']
    connection_json = {}
    connection_json ['url'] = access_token['url']
    connection_json ['userId'] = user_id
    connection_json ['sessionId'] = session_id
    connection_json ['checksum'] = hash(f'{padding}{user_id}{session_id}')
    connection_json ['language'] = language
    # TODO: save all the sessionIDs associated with this user
    # Create an end point to get all session ids for a given user
    
    res.set(database.json_response(connection_json))