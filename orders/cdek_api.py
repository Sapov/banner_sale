import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class CDEKService:
    def __init__(self, login, secret):
        self.login = login
        self.secret = secret
        self.base_url = 'https://api.edu.cdek.ru/v2'
        self.deliverypoints = f'{self.base_url}/deliverypoints'

        self.auth_token = None

    def get_auth_token(self):

        auth_url = f"{self.base_url}/oauth/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.login,
            'client_secret': self.secret
        }

        response = requests.post(auth_url, data=payload, headers={
            'Accept': 'application/json',
            'X-App-Name': 'widget_pvz',
            'X-App-Version': '3.11.1'
        })
        print(response.status_code)

        if response.status_code != 200 or 'access_token' not in response.json():
            raise RuntimeError('Server not authorized to CDEK API')

        self.auth_token = response.json()['access_token']

    def get_deliverypoints(self):

        headers = {
            'Authorization': f'Bearer {self.auth_token}'
        }
        params = {}

        response = requests.get(self.deliverypoints, headers=headers, params=params)
        if response.status_code == 200:
            with open('points.txt', 'w', encoding='utf-8') as file:
                json.dump(response.json(), file, ensure_ascii=False, indent=4)
            return response.json()
        else:
            # Если токен просрочен, можно попробовать обновить и повторить запрос
            # Для простоты просто выбросим исключение
            raise Exception('Не удалось получить список ПВЗ')


if __name__ == '__main__':
    service = CDEKService(
        login=os.getenv('LOGIN'),  # Замените на ваш логин
        secret=os.getenv('SECRET')  # Замените на ваш пароль
    )

    service.get_auth_token()
    service.get_deliverypoints()
