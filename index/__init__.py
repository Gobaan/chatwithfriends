import logging
import os
import azure.functions as func

def main(req: func.HttpRequest, context: func.Context, res: func.Out[func.HttpResponse]) -> None:
    index = os.path.join(context.function_directory, '..', 'index.html')
    logging.info("index.html path: " + index)
    with open(index, 'r') as file:
        data = file.read()
    res.set(func.HttpResponse(body=data, status_code=200, headers={"Content-Type": "text/html"}))
