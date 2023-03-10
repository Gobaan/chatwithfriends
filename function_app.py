import azure.functions as func
from helpers import database

table_client = database.initialize_db()
app = func.FunctionApp()
# Use the HTTP trigger decorator
@app.function_name(name='Counter')
@app.route(route='counter', auth_level=func.AuthLevel.ANONYMOUS)
def counter(req: func.HttpRequest) -> func.HttpResponse:
    # Increment the counter value
    counter_value = database.increment_counter(table_client)
    return func.HttpResponse(f'The counter value is now {counter_value}')

@app.function_name(name="HttpTrigger1")
@app.route(route="hello") # HTTP Trigger
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("HttpTrigger1 function processed a request!!!")