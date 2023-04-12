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
        logging.info(f'Language: {data.source_language} | New_language: {data.target_language} | Message: {data.message}')
        new_message['translated'] = cognitive_services.translate(data.message, data.source_language, data.target_language)
    logging.info(f'The full message is: {new_message}')
    return new_message

if __name__ == '__main__':
    import loadenv
    import json
    loadenv.loadenv()
    test = "{'userId': 'User 2', 'original': 'Hola amigo hablo español.', 'translated': '', 'translated_blob': '', 'blob': 'https://chatwithfriendsdb.blob.core.windows.net/audio-messages-ogg/a5933c65-3300-4108-bc72-b4e4f8c6a0bb.ogg?sv=2021-12-02&se=2023-04-13T03%3A55%3A27Z&sr=b&sp=rw&sig=OVzuSzerMXxd%2FMc1J3A3hhQEnOJzGqkxSe%2Fs9BMXLVM%3D', 'source_language': 'es', 'target_language': 'en'}"
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
