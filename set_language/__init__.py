import logging

import azure.functions as func
from helpers import database

table_client = database.initialize_db()
# Use the HTTP trigger decorator
def main(req: func.HttpRequest) -> func.HttpResponse:
    # Increment the counter value
    preferences = {'language': req.params['language']}
    user_id = req.params['user_id']
    database.set_preferences(table_client, user_id, preferences)
    return database.json_response({'new_language': preferences})