import azure.functions as func
from helpers import database

table_client = database.initialize_db()
# Use the HTTP trigger decorator
def main(req: func.HttpRequest) -> func.HttpResponse:
    # Increment the counter value
    preferences = {'language': req.params['language']}
    user_id = req.params['userId']
    session_id = req.params['sessionId']
    database.set_preferences(table_client, user_id, preferences, session_id = session_id)
    return database.json_response(preferences)