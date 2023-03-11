import logging

import azure.functions as func
from helpers import database

table_client = database.initialize_db()
# Use the HTTP trigger decorator
def main(req: func.HttpRequest) -> func.HttpResponse:
    # Increment the counter value
    counter_value = database.increment_counter(table_client)
    return database.json_response({'user_number': counter_value})