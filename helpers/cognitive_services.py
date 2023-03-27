import os
import requests

#TODO: Make this do multiple translation 
def translate(text, source_language, target_language):
    key = os.environ['AzureCognitiveServiceKey']
    region = os.environ['AzureCognitiveServiceRegion']
    endpoint = os.environ['AzureTranslationEndpoint']
    # Use the Translator translate function
    url = endpoint + '/translate'
    # Build the request
    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': target_language
    }
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json'
    }
    body = [{
        'text': text
    }]
    # Send the request and get response
    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()
    # Get translation    
    translation = response[0]["translations"][0]["text"]
    # Return the translation
    return translation

if __name__ == '__main__':
    print(translate('Hello world!', 'en', 'fr'))
