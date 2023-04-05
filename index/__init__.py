import logging
import os
import azure.functions as func

def main(req: func.HttpRequest, context: func.Context, res: func.Out[func.HttpResponse]) -> None:
    index = os.path.join(context.function_directory, '..', 'index.html')
    logging.info("index.html path: " + index)
    with open(index, 'r') as file:
        data = file.read()
    if 'sessionId' in req.params:
        unknown_session = "let sessionId = localStorage.getItem('sessionId');"
        known_session = f"let sessionId = '{req.params['sessionId']}';"
        data = data.replace(unknown_session, known_session)

    res.set(func.HttpResponse(body=data, status_code=200, headers={"Content-Type": "text/html"}))
