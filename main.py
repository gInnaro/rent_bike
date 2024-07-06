import requests

def registr():
    url = 'http://127.0.0.1:8000/api/registr/'

    data = {
        'username': 'innaro',
        'password': 'qwerty',
        'email': 'ilnaz.gan@gmail.com'
    }

    r = requests.post(url, json=data)
    return r.json()


def token():
    url = 'http://127.0.0.1:8000/api/token/'
    data = {
        'username': 'innaro',
        'password': 'qwerty'
    }

    r = requests.post(url, json=data)
    return r.json()

def token_check(data):
    url = 'http://127.0.0.1:8000/api/token/verify/'
    headers = {
        "token": data['refresh']}
    r = requests.post(url, json=headers)

    return r.json()


def bike_list(data):
    url = 'http://127.0.0.1:8000/bicycles/list/'
    headers = {
        "Authorization": f"Bearer {data['access']}"}
    r = requests.get(url, headers=headers)

    return r.json()

def bike_rent(data):
    url = 'http://127.0.0.1:8000/bicycles/rent/'
    headers = {
        "Authorization": f"Bearer {data['access']}"
    }
    r = requests.post(url, headers=headers, json={"bicycle_id": "1"})
    return r.json()

def return_bike(data):
    url = 'http://127.0.0.1:8000/bicycles/return/'
    headers = {
        "Authorization": f"Bearer {data['access']}"
    }
    r = requests.post(url, headers=headers, json={"bicycle_id": "1"})

    return r.json()


def history(data):
    url = 'http://127.0.0.1:8000/bicycles/rental_history/'
    headers = {
        "Authorization": f"Bearer {data['access']}"
    }
    r = requests.get(url, headers=headers, json={"bicycle_id": "1"})

    return r.json()

if __name__ == "__main__":
    data = token()
    token_check(data)
    # # bike_rent(data)
    # # time.sleep(45)
    # history(data)
