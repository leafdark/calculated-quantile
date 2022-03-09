import requests


BASE = "http://127.0.0.1:5000/"


def test_add_pool_data_normal_success():
    data = {
        "poolId": 12346,
        "poolValues": [2, 3, 4, 5, 9, 7]
    }
    response = requests.post(f'{BASE}pool', data)
    assert response.status_code == 200


def test_update_pool_data_normal_success():
    data = {
        "poolId": 12346,
        "poolValues": [2, 3, 4, 5, 9, 7, 10]
    }
    response = requests.post(f'{BASE}pool', data)
    assert response.status_code == 200


def test_add_pool_pool_values_empty():
    data = {
        "poolId": 12346,
        "poolValues": []
    }
    response = requests.post(f'{BASE}pool', data)
    assert response.status_code == 400


def test_add_pool_not_pool_values():
    data = {
        "poolId": 12346,
    }
    response = requests.post(f'{BASE}pool', data)
    assert response.status_code == 400


def test_add_pool_not_pool_id():
    data = {
        "poolValues": [2, 3]
    }
    response = requests.post(f'{BASE}pool', data)
    print(response)
    assert response.status_code == 400


def test_add_pool_pool_id_is_string():
    data = {
        "poolId": 'abc',
        "poolValues": [2, 3, 5]
    }
    response = requests.post(f'{BASE}pool', data)
    assert response.status_code == 400


def test_add_pool_values_have_string():
    data = {
        "poolId": 123456,
        "poolValues": [2, 3, 5, 'a']
    }
    response = requests.post(f'{BASE}pool', data)
    assert response.status_code == 400
