import uuid
import json
import requests
from requests.auth import HTTPBasicAuth
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLIENT_ID = '71b92890-bf91-4b6b-9645-6561b93e3d7d'
SECRET = '3278c7e4-6c0c-4b7b-a8b7-9baadb679504'

SYSTEM_PROMPT = """
Ты - эксперт по SQL и SQLite3. 
Твоя задача - создавать ТОЧНЫЕ SQL-запросы на основе описания пользователя.

КРИТИЧЕСКИ ВАЖНО:
- Используй ТОЧНО ТЕ ЖЕ названия таблиц и полей, которые указал пользователь
- Если пользователь сказал "таблица car" - создавай таблицу car
- Если пользователь сказал "таблица menu" - создавай таблицу menu
- Если пользователь указал поля "id, title" - используй именно эти названия
- or придумывай свои названия таблиц и полей

Правила форматирования:
1. Генерируй только SQL-запрос, БЕЗ любых объяснений до или после
2. НЕ добавляй слова "SQL-запрос:", "Вот запрос:" и подобное
3. Используй синтаксис SQLite3
4. Используй IF NOT EXISTS для CREATE TABLE
5. Комментарии НЕ добавляй

Запрос ID: {request_id}
Время запроса: {timestamp}

Запрос пользователя: {user_input}

Сгенерируй SQL-запрос строго по описанию пользователя:
"""


def get_access_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4())
    }
    payload = {"scope": "GIGACHAT_API_PERS"}

    try:
        res = requests.post(url, headers=headers, auth=HTTPBasicAuth(CLIENT_ID, SECRET), data=payload, verify=False)
        res.raise_for_status()
        access_token = res.json().get("access_token")
        if not access_token:
            raise ValueError("Токен доступа не был получен.")
        return access_token
    except requests.RequestException as e:
        print("Ошибка при получении access token:", e)
        return None


def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat",
        "temperature": 0.3,  # Немного повысил для разнообразия
        "messages": [{"role": "user", "content": msg}],
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        print("Ошибка при отправке запроса к GigaChat API:", e)
        return "Ошибка при получении ответа от GigaChat."


class SQLAI:
    def __init__(self):
        self.request_count = 0

    def generate_sql(self, user_input: str) -> str:
        self.request_count += 1
        access_token = get_access_token()
        if not access_token:
            return "Не удалось получить access token."

        full_prompt = SYSTEM_PROMPT.format(
            user_input=user_input,
            request_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat()
        )

        return send_prompt(full_prompt, access_token)