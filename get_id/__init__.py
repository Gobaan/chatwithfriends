import logging

import azure.functions as func
import os
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # Initialize the Azure Table storage client
    account_name = os.environ['AzureStorageAccountName']
    account_key = os.environ['AzureStorageAccountKey']
    table_service = TableService(account_name=account_name, account_key=account_key)

    # Create a new user entity with a unique ID
    user_data = req.get_json()
    table_name = 'users'
    user_id = table_service.query_entities(table_name, select='PartitionKey,RowKey', top=1, order_by='RowKey desc')[0].RowKey + 1
    user_entity = Entity()
    user_entity.PartitionKey = table_name
    user_entity.RowKey = str(user_id)
    for key, value in user_data.items():
        setattr(user_entity, key, value)
    table_service.insert_entity(table_name, user_entity)

    # Return the new user ID to the client
    return func.HttpResponse(f"New user ID: {user_id}")