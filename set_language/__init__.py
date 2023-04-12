import azure.functions as func
from helpers import database

table = database.Database()
# Use the HTTP trigger decorator
def main(req: func.HttpRequest) -> func.HttpResponse:
    # Increment the counter value
    preferences = {'language': req.params['language']}
    user_id = req.params['userId']
    session_id = req.params['sessionId']
    table.set_preferences(user_id, preferences, session_id = session_id)
    return database.json_response(preferences)