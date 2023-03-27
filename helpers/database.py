from azure.data.tables import TableServiceClient
from azure.data.tables import UpdateMode
from azure.core.exceptions import ResourceNotFoundError
import logging
import json
import azure.functions as func
import os
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['session_id', 'source_user', 'target_user', 'original_language', 'language', 'message', 'blob'])


# TODO: Move this to a test case so it can just be mocked
if __name__ == '__main__':
    os.environ['AzureStorageAccountKey'] = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;'

JSON_MIME_TYPE = 'text/json'
def json_response(json_serialiazable):
    return func.HttpResponse(json.dumps(json_serialiazable), mimetype = JSON_MIME_TYPE)

def initialize_db():
    # Initialize TableService with your connection string
    connection_string = os.environ["AzureStorageAccountKey"]
    table_service_client: TableServiceClient = TableServiceClient.from_connection_string(connection_string)
    # Define the name of your table and entity that stores the counter value
    table_name = 'counters'
    return table_service_client.create_table_if_not_exists(table_name)

table_client = initialize_db()
def increment_counter(table_client: TableServiceClient, session_id = 'mycounter'):
    logging.info ("Incrementing counter")
    # Retrieve the current counter value from the table
    try:
        entity = table_client.get_entity(partition_key=session_id, row_key='counter')
    except ResourceNotFoundError:
        entity = {'PartitionKey': session_id,
                  'RowKey': 'counter',
                  'counter': 0
                 }
        table_client.create_entity(entity=entity)

    entity['counter'] += 1
    logging.info("Updating entity")
    table_client.update_entity(mode=UpdateMode.REPLACE, entity=entity)
    logging.info("Updated entity")
    return entity['counter']

def set_preferences(table_client: TableServiceClient, user_id, preferences = None, session_id = 'mycounter'):
    if preferences == None:
        preferences = {}
    logging.info ("Set_Preferences")
    user_id = str(user_id)

    # Retrieve the current counter value from the table
    try:
        entity = table_client.get_entity(partition_key=session_id, row_key=user_id)
    except ResourceNotFoundError:
        entity = {'PartitionKey': session_id,
                  'RowKey': user_id,
                  'language': 'en-us',
                 }
        table_client.create_entity(entity=entity)

    entity.update(preferences)
    logging.info("Updating entity")
    table_client.update_entity(mode=UpdateMode.REPLACE, entity=entity)
    return entity

def get_all_user_languages(table_client: TableServiceClient, session_id = 'mycounter'):
    entities = table_client.query_entities(f"PartitionKey eq '{session_id}' and not (RowKey eq 'counter')")
    for entity in entities:
        yield (entity['RowKey'], entity['language'])

                            
if __name__ == '__main__':
    for user, language in get_all_user_languages(table_client):
        print (user, language)