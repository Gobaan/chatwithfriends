import azure.functions as func
from helpers import database
import os
from azure.messaging.webpubsubservice import WebPubSubServiceClient

# Use the HTTP trigger decorator
def main(req: func.HttpRequest, res: func.Out[func.HttpResponse]) -> None:
    counter_value = database.increment_counter(database.table_client)
    client: WebPubSubServiceClient = WebPubSubServiceClient.from_connection_string(os.environ['WebPubSubConnectionString'], os.environ['AzureWebJobsWebPubSubHub'])
    database.set_preferences(database.table_client, counter_value)
    # Connect to the WebPubSub service with the user ID query parameter
    access_token = client.get_client_access_token(user_id = counter_value)
    connection_json = {}
    connection_json['url'] = access_token['url']
    connection_json ['userId'] = f'{counter_value}'
    res.set(database.json_response(connection_json))