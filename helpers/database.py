from azure.data.tables import TableServiceClient, TableClient
from azure.data.tables import UpdateMode
from azure.core.exceptions import ResourceNotFoundError
import logging
import json
import azure.functions as func
import os
from collections import namedtuple
from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions

DataTuple = namedtuple('DataTuple', ['session_id', 'source_user', 'target_user', 'source_language', 'target_language', 'message', 'blob'])


# TODO: Move this to a test case so it can just be mocked
JSON_MIME_TYPE = 'text/json'
def json_response(json_serialiazable):
    return func.HttpResponse(json.dumps(json_serialiazable), mimetype = JSON_MIME_TYPE)

class Database:
    # TODO make this a static instance
    def __init__(self):
        # Initialize TableService with your connection string
        connection_string = os.environ["AzureStorageConnectionString"]
        self.table_service_client: TableServiceClient = TableServiceClient.from_connection_string(connection_string)
        # Define the name of your table and entity that stores the counter value
        table_name = 'counters'
        self.table_client : TableClient = self.table_service_client.create_table_if_not_exists(table_name)

    def increment_counter(self, session_id = 'mycounter'):
        logging.info ("Incrementing counter")
        # Retrieve the current counter value from the table
        try:
            entity = self.table_client.get_entity(partition_key=session_id, row_key='counter')
        except ResourceNotFoundError:
            entity = {'PartitionKey': session_id,
                    'RowKey': 'counter',
                    'counter': 0
                    }
            self.table_client.create_entity(entity=entity)

        entity['counter'] += 1
        logging.info("Updating entity")
        self.table_client.update_entity(mode=UpdateMode.REPLACE, entity=entity)
        logging.info("Updated entity")
        return entity['counter']

    def set_preferences(self,  user_id, preferences = None, session_id = 'mycounter'):
        if preferences == None:
            preferences = {}
        logging.info ("Set_Preferences")
        user_id = str(user_id)

        # Retrieve the current counter value from the table
        try:
            entity = self.table_client.get_entity(partition_key=session_id, row_key=user_id)
        except ResourceNotFoundError:
            entity = {'PartitionKey': session_id,
                    'RowKey': user_id,
                    'language': 'en',
                    }
            self.table_client.create_entity(entity=entity)

        entity.update(preferences)
        logging.info("Updating entity")
        self.table_client.update_entity(mode=UpdateMode.REPLACE, entity=entity)
        return entity

    # TODO: fix this so users languages are not session specific?
    def get_all_user_languages(self, session_id = 'mycounter'):
        entities = self.table_client.query_entities(f"PartitionKey eq '{session_id}' and not (RowKey eq 'counter')")
        for entity in entities:
            yield (entity['RowKey'], entity['language'])

    def get_user_language(self, user_id, session_id = 'mycounter'):
        entities = self.table_client.query_entities(f"PartitionKey eq '{session_id}' and RowKey eq '{user_id}'")
        for entity in entities:
            return entity['language']

def get_webosocket_id(user_id:str, session_id:str):
    return user_id + session_id
                                
def get_sas_url(user_id:str, session_id:str):
    # Set your Azure Blob Storage account connection string and container name
    container_name = 'audio-messages'
    account_name = os.environ['AzureStorageAccountName']
    account_key = os.environ['AzureStorageAccountKey'] 
    filetype = 'webm'
    blob_name = f'{user_id}-{session_id}-{datetime.now().strftime("%Y%m%d%H%M%S%f")}.{filetype}'
    blob_sas = generate_blob_sas(
        account_name=account_name, 
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True, create=True, write=True),
        expiry=datetime.utcnow() + timedelta(hours=24))
    return f'https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{blob_sas}'


if __name__ == '__main__':
    os.environ['AzureStorageAccountName'] = 'chatwithfriendsdb'
    os.environ['AzureStorageAccountKey'] = 'bwzFahW172zCTJmOQDXS9TXMVIim4Hbc9rZenJvefyvZEBqXxDisd5lNio6CrE3wzPZH+fzwQH4q+AStW3IV1g=='
    print (get_sas_url('gobi', '123'))
    database = Database()
    for user, language in database.get_all_user_languages():
       print (user, language)