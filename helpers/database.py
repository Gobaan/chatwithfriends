from azure.data.tables import TableServiceClient
from azure.data.tables import UpdateMode
from azure.core.exceptions import ResourceNotFoundError
import logging

def initialize_db():
    # Initialize TableService with your connection string
    connection_string = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
    table_service_client: TableServiceClient = TableServiceClient.from_connection_string(connection_string)
    # Define the name of your table and entity that stores the counter value
    table_name = 'counters'
    return table_service_client.create_table_if_not_exists(table_name)

def increment_counter(table_client: TableServiceClient):
    logging.info ("Incrementing counter")
    # Retrieve the current counter value from the table
    try:
        entity = table_client.get_entity(partition_key='mycounter', row_key='counter')
    except ResourceNotFoundError:
        entity = {'PartitionKey': 'mycounter',
                  'RowKey': 'counter',
                  'counter': 0
                  }
        table_client.create_entity(entity=entity)

    entity['counter'] += 1
    logging.info("Updating entity")
    table_client.update_entity(mode=UpdateMode.REPLACE, entity=entity)
    logging.info("Updated entity")
    return entity['counter']

if __name__ == '__main__':
    table_client = initialize_db()
    print(increment_counter(table_client))