import os
import requests
from dotenv import load_dotenv
import time


# Загрузка переменных окружения из .env файла
load_dotenv()


class MailSlurp:
    def __init__(self):
        self.base_api_url = "https://api.mailslurp.com/"
        self.api_key = os.getenv("EMAIL_API_KEY")
        self.headers = {
            "x-api-key": self.api_key,
        }

    @staticmethod
    def get_result_api(response):
        """Обрабатываем полученый результат от API"""
        try:
            result = response.json()
            print(result)
            return result
        except Exception as error:
            print(error)
            return {}

    def create_new_email(self) -> dict:
        """Создаем новый email адрес"""
        url = self.base_api_url + "inboxes"
        response = requests.post(url, headers=self.headers)
        return self.get_result_api(response)

    def get_inboxes(self):
        """Получаем все email адреса"""
        url = self.base_api_url + "inboxes"
        response = requests.get(url, headers=self.headers)
        return self.get_result_api(response)

    def get_inbox_info(self, inbox_id):
        """Получаем информацию по email адресу"""
        url = self.base_api_url + f"inboxes/{inbox_id}"
        response = requests.get(url, headers=self.headers)
        return self.get_result_api(response)

    def get_latest_email(self):
        """Получаем последнее сообщение со всех ящиков"""
        url = self.base_api_url + f"emails/latest"
        response = requests.get(url, headers=self.headers)
        return self.get_result_api(response)

    def get_inbox_email_by_id(self, inbox_id):
        """Получаем сообщения по email адресу"""
        url = self.base_api_url + f"inboxes/{inbox_id}/emails"
        response = requests.get(url, headers=self.headers)
        return self.get_result_api(response)

    def get_code_by_facebook(self, inbox_id):
        """
        Находим сообщение с Facebook и получаем код регистрации
        Пример 'subject': 'FB-20763 — ваш код подтверждения для Facebook'
        """
        time.sleep(5)
        digits = None
        all_messages_inbox = self.get_inbox_email_by_id(inbox_id)
        for message in all_messages_inbox:
            subject = message.get("subject")
            if subject and subject.startswith("FB-") and subject.endswith("Facebook"):
                code = subject.split(" ")[0]
                digits = code.replace("FB-", "")
                return digits

        if not digits:
            return self.get_code_by_facebook(inbox_id)


new_email_ready = {
    'id': '6e388a23-6968-4a6b-8d29-505413ad43d1', 'userId': '02781403-684e-493f-ba0f-13f482182dad',
    'created': '2024-07-27T20:34:52.078Z', 'createdAt': '2024-07-27T20:34:52.078Z', 'name': None,
    'domainId': None, 'description': None,
    'emailAddress': 'd4732209-0b63-4c7c-88da-4d6718133231@mailslurp.net',
    'expiresAt': '2024-07-29T08:34:52.076670Z', 'favourite': False, 'tags': None, 'teamAccess': True,
    'inboxType': 'HTTP_INBOX', 'readOnly': False, 'virtualInbox': False, 'functionsAs': None
}

# last_message_inbox = [
#     {'id': '48cc7a80-ca06-4053-add7-f81744fbe859', 'domainId': None,
#      'subject': 'FB-20763 — ваш код подтверждения для Facebook',
#      'to': ['ddbfd0df-bebb-41a3-abc3-c8b08098a81d@mailslurp.net'], 'from': 'registration@facebookmail.com', 'bcc': [],
#      'cc': [], 'createdAt': '2024-07-29T17:47:22.663Z', 'read': True, 'attachments': [],
#      'threadId': '1d9631ca-78fb-4f7d-ab55-c025a571b09b',
#      'messageId': '93aeedaa-4dd2-11ef-8a6a-a7087e41eac2@facebookmail.com', 'inReplyTo': None,
#      'created': '2024-07-29T17:47:22.663Z'},
#     {'id': '2657fb4a-f53d-4d32-851b-ab27ecb1279b', 'domainId': None, 'subject': 'test-last-message',
#      'to': ['ddbfd0df-bebb-41a3-abc3-c8b08098a81d@mailslurp.net'], 'from': 'kostencko.alexander2012@gmail.com',
#      'bcc': [], 'cc': [], 'createdAt': '2024-07-29T19:21:02.819Z', 'read': False, 'attachments': [],
#      'threadId': '02fb3f61-1acd-4bc1-b741-1e7335e66697',
#      'messageId': 'CAO_aJM-Hf+6yaOnSOpjk=jvz8Nf1FL9PfRe+S8fGCVaN5yK+3w@mail.gmail.com', 'inReplyTo': None,
#      'created': '2024-07-29T19:21:02.819Z'}
# ]
