import requests

def registr(): #регистрация нового юзера
    url = 'http://127.0.0.1:8000/api/registr/'

    data = {
        'username': 'innaro',
        'password': 'qwerty',
        'email': 'ilnaz.gan@gmail.com'
    }

    r = requests.post(url, json=data)
    return r.json()


def token(): #получения токена
    url = 'http://127.0.0.1:8000/api/token/'
    data = {
        'username': 'innaro',
        'password': 'qwerty'
    }

    r = requests.post(url, json=data)
    return r.json()

def token_check(data): #проверка работоспособности токена
    url = 'http://127.0.0.1:8000/api/token/verify/'
    headers = {
        "token": data['refresh']}
    r = requests.post(url, json=headers)

    return r.json()


def bike_list(data): #список свободных велосипедов
    url = 'http://127.0.0.1:8000/bicycles/list/'
    headers = {
        "Authorization": f"Bearer {data['access']}"}
    r = requests.get(url, headers=headers)
    return r.json()

def bike_rent(data): #аренда велосипеда
    url = 'http://127.0.0.1:8000/bicycles/rent/'
    headers = {
        "Authorization": f"Bearer {data['access']}"
    }
    r = requests.post(url, headers=headers, json={"bicycle_id": "1"})
    return r.json()

def return_bike(data): #вернуть велосипед
    url = 'http://127.0.0.1:8000/bicycles/return/'
    headers = {
        "Authorization": f"Bearer {data['access']}"
    }
    r = requests.post(url, headers=headers, json={"bicycle_id": "1"})

    return r.json()


def history(data): #история аренды велосипедов пользователем
    url = 'http://127.0.0.1:8000/bicycles/rental_history/'
    headers = {
        "Authorization": f"Bearer {data['access']}"
    }
    r = requests.get(url, headers=headers, json={"bicycle_id": "1"})

    return r.json()

if __name__ == "__main__":
    pass
