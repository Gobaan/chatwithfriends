import azure.functions as func
from helpers import database
import json
table_client = database.initialize_db()
# Use the HTTP trigger decorator
def main(req: func.HttpRequest, connection: str, res: func.Out[func.HttpResponse]) -> None:
    counter_value = database.increment_counter(table_client)
    connection_json = json.loads(connection)
    connection_json ['userId'] = f'User{counter_value}'
    res.set(database.json_response(connection_json))