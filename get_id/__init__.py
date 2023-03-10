from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity, AzureException
import azure.functions as func
import os
import logging

# Initialize TableService with your connection string
connection_string = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;'
table_service = TableService(connection_string=connection_string)

# Define the name of your table and entity that stores the counter value
table_name = 'counters'
try:
    table_service.create_table(table_name)
except:
    pass

counter_entity = Entity()
counter_entity.PartitionKey = 'mycounter'
counter_entity.RowKey = 'counter'

def increment_counter():
    # Retrieve the current counter value from the table
    try:
        current_counter = table_service.get_entity(table_name, 'mycounter', 'counter')
        counter_value = current_counter.counter_value
    except:
        counter_entity.counter_value = counter_value = 0
        table_service.insert_entity(table_name, counter_entity)

    # Increment the counter value
    counter_value += 1
    # Update the counter value in the table
    counter_entity.counter_value = counter_value
    table_service.update_entity(table_name, counter_entity)
    return counter_value

increment_counter()


def main(req: func.HttpRequest, res: func.Out[func.HttpResponse]) -> func.HttpResponse:
    # Increment the counter value
    counter_value = increment_counter()

    res.set(func.HttpResponse(f'The counter value is now {counter_value}'))