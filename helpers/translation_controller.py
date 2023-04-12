from . import database
import logging
from . import cognitive_services

def data_to_translation(data:database.DataTuple):
    new_message = {
        'userId': f'User {data.source_user}', 
        'original': data.message if not data.blob else cognitive_services.speech_to_text(data.blob, data.source_language),
        'translated': '',
        'translated_blob': '',
        'blob': data.blob,
        'source_language': data.source_language,
        'target_language': data.target_language,
    }

    if data.source_language != data.target_language:
        logging.info(f'Language: {data.source_language} | New_language: {data.target_language} | Message: {new_message["original"]}')
        new_message['translated'] = cognitive_services.translate(new_message['original'], data.source_language, data.target_language)
    logging.info(f'The full message is: {new_message}')
    return new_message

if __name__ == '__main__':
    import load_environment as load_environment
    import json
    load_environment.loadenv()
    test = "{'userId': 'User 2', 'original': 'Lo siento.', 'translated': '', 'translated_blob': '', 'blob': 'https://chatwithfriendsdb.blob.core.windows.net/audio-messages-ogg/80428d42-5d68-4f14-bfd1-62f7c68276c3.ogg?sv=2021-12-02&se=2023-04-13T10%3A47%3A32Z&sr=b&sp=rw&sig=8T0FP7IbrvWHqdzid4Yq3BpWH0bRGm5Y8lDDEwW%2Fk0k%3D', 'source_language': 'es', 'target_language': 'en'}"
    test = test.replace("'", '"')
    data_json = json.loads(test)
    test_data = database.DataTuple(
        source_user=data_json['userId'],
        message=data_json['original'],
        blob=data_json['blob'],
        source_language=data_json['source_language'],
        target_language=data_json['target_language'],
        session_id="test",
        target_user="gobi"
    )
    message = data_to_translation(test_data)
    print (message)
