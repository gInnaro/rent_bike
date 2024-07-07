from main import *

# def test_registr():
#     assert registr()['success'] == 'Пользователь успешно зарегистрирован.'

def test_token():
    token_dict = token()
    assert 'detail' not in token_dict

def test_token_check():
    data = token()
    assert token_check(data) == {}

def test_bike_list():
    data = token()
    answer = bike_list(data)
    assert 'detail' not in answer

def test_bike_rent():
    data = token()
    assert bike_rent(data)['status'] == 'rented'

def test_return_bike():
    data = token()
    answer = return_bike(data)
    assert 'error' not in answer

def test_history():
    data = token()
    answer = history(data)
    assert 'detail' not in answer
