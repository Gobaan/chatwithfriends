import logging
import json
import azure.functions as func

def main(req: func.HttpRequest, connection, res: func.Out[func.HttpResponse]) -> None:
    logging.info('Python HTTP trigger function processed a request.')
    res.set(func.HttpResponse(connection, mimetype='text/json'))