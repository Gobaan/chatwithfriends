import os
import json

def loadenv():
    with open('local.settings.json') as fp:
        variables = json.load(fp)

    for key, value in variables['Values'].items():
        os.environ[key] = value

