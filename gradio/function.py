
import requests
import os
import mimetypes

import os
host = os.environ.get('FASTAPI_HOST', 'localhost')
port = os.environ.get('FASTAPI_PORT', '5000')


def send_file_to_backend(file, lang_choice):
    try:
        lang = "false" if lang_choice == "English" else "true"
        
        file_content = open(file.name, "rb")
        file_name = os.path.basename(file.name)
        content_type = mimetypes.guess_type(file.name)[0]
        
        files = {"file": (file_name, file_content, content_type or "application/octet-stream")}
        data = {"lang": lang}
        
        response = requests.post(f'http://{host}:{port}/api/v1/mobi-test/image/create-description', files=files, data=data)
        
        if response.status_code == 200:
            result = response.json().get("description", "Ответ от сервера не содержит данных")
            return f'Файл {file_name}:\n\n{result}'
        else:
            return f"Файл {file_name}:\n\nОшибка: {response.status_code}, {response.text}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"
    finally:
        file_content.close()


def get_table_data():

    response = requests.get(f'http://{host}:{port}/api/v1/mobi-test/image/all')
    json_response = response.json()
    if json_response:
        table_data = [
            [item["id"], item["file_name"], item["timestamp"], item["description"], item["status"]] for item in json_response
        ]
        return table_data
    else:
        return []
