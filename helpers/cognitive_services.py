import os
import requests
import logging

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
    # Return a response indicating whether the event was successfully added
    if request.status_code != 200:
        logging.error(f"Error adding event: {request.text}")
    else:
        logging.info(f"Translation successful: {request.json()}")
    response = request.json()
    # Get translation    
    translation = response[0]["translations"][0]["text"]
    # Return the translation
    return translation

def speech_to_text(audio_blob_url, source_language, format='ogg'):
    logging.info(f"Converting speech to text: {audio_blob_url} from {source_language}")
    key = os.environ['AzureCognitiveServiceKey']
    region = os.environ['AzureCognitiveServiceRegion']
    print (key)
    if source_language == 'en':
        source_language = 'en-US'
    elif source_language == 'es':
        source_language = 'es-AR'
    # Set the request headers for the Speech-to-Text API
    speech_headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': f'audio/{format};'
    }

    # Make a POST request to the Speech-to-Text API to transcribe the audio from the blob URL
    speech_url = f'https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language={source_language}'
    audio = requests.get(audio_blob_url).content

    speech_response = requests.post(speech_url, headers=speech_headers, data=audio)

    transcription_json = speech_response.json()
    # Get the transcription from the Speech-to-Text API response
    transcription = transcription_json['DisplayText']

    return transcription


if __name__ == '__main__':
    import loadenv
    loadenv.loadenv()

    urls = {
        'ogg': 'https://chatwithfriendsdb.blob.core.windows.net/audio-messages-ogg/a5933c65-3300-4108-bc72-b4e4f8c6a0bb.ogg?sv=2021-12-02&se=2023-04-13T03%3A55%3A27Z&sr=b&sp=rw&sig=OVzuSzerMXxd%2FMc1J3A3hhQEnOJzGqkxSe%2Fs9BMXLVM%3D',
        'webm': 'https://chatwithfriendsdb.blob.core.windows.net/audio-messages/1-9cf78e1f-0fe0-4e34-bbb3-2fc6e6d0f83d-20230408055515689974.wav?se=2023-04-08T06%3A55%3A15Z&sp=rcw&sv=2021-12-02&sr=b&sig=8OE9%2BeKzTtmm3B7sWTl1bfbKyyur9Z5pc25OS6wAKks%3D',
        'mp4':'https://chatwithfriendsdb.blob.core.windows.net/audio-messages/test.mp4?sp=r&st=2023-04-09T01:14:15Z&se=2023-04-09T09:14:15Z&spr=https&sv=2021-12-02&sr=b&sig=8qYbNI22WvWC5BiXFvYW9QCMQZQgWRwvY7g5vmCjV2M%3D',
        'mp3': 'https://chatwithfriendsdb.blob.core.windows.net/audio-messages/test.mp3?sp=r&st=2023-04-09T01:22:36Z&se=2023-04-09T09:22:36Z&spr=https&sv=2021-12-02&sr=b&sig=Lo8v54odki3iTtewHzcW6pr4PpF5evIrez%2FJDTyRdog%3D',
    }
    frmat = 'ogg'
    text = speech_to_text(urls[frmat],'en-US', frmat)
    print (text)
    print (translate(text, 'es', 'en'))