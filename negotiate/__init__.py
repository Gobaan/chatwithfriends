import azure.functions as func
from helpers import database
import os
from azure.messaging.webpubsubservice import WebPubSubServiceClient
import uuid 

table = database.Database()
# Use the HTTP trigger decorator
def main(req: func.HttpRequest, res: func.Out[func.HttpResponse]) -> None:
    if 'sessionId' in req.params and req.params['sessionId'] != 'null':
        session_id = req.params['sessionId']
    else:
        session_id = str(uuid.uuid4())

    if 'userId' in req.params and req.params['userId'] != 'null':
        user_id = req.params['userId']
    else:
        user_id = f'{table.increment_counter(session_id)}'

    if 'language' in req.params and req.params['language'] != 'null':
        language = req.params['language']
    else:
        language = table.get_user_language(user_id, session_id) or 'en'
    
    table.set_preferences(user_id, {'language': language}, session_id)

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
    connection_json ['blobUrl'] = database.get_sas_url(user_id, session_id)

    # TODO: save all the sessionIDs associated with this user
    # Create an end point to get all session ids for a given user
    
    res.set(database.json_response(connection_json))