from azure.messaging.webpubsubservice import WebPubSubServiceClient
from helpers import database
import azure.functions as func
import json
import logging
import os
import json

JSON_MIME_TYPE = 'text/json'
def json_response(json_serialiazable):
    return func.HttpResponse(json.dumps(json_serialiazable), mimetype = JSON_MIME_TYPE)

table_client = database.initialize_db()
app = func.FunctionApp()
# Use the HTTP trigger decorator
@app.function_name(name='getID')
@app.route(route='getId', auth_level=func.AuthLevel.ANONYMOUS)
def counter(req: func.HttpRequest) -> func.HttpResponse:
    # Increment the counter value
    counter_value = database.increment_counter(table_client)
    return json_response({'user_number': counter_value})

@app.function_name(name="index")
@app.route(route="index") # HTTP Trigger
def main(req: func.HttpRequest, context: func.Context):
    with open('index.html', 'r') as file:
        data = file.read()
    return func.HttpResponse(body=data, status_code=200, headers={"Content-Type": "text/html"})

@app.function_name(name="message")
@app.route(route="message") # HTTP Trigger
async def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(request)
    request = json.loads(request)
    user_id = request['connectionContext']['userId']
    message = request['data']
    connection_string = os.environ.get("WebPubSubConnectionString")
    service = WebPubSubServiceClient.from_connection_string(connection_string, hub='simplechat')
    service.send_to_all({'userId': user_id, 'text': message})