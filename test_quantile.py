import requests

BASE = "http://127.0.0.1:5000/"


def test_calculate_quantile_001():
    data = {
        "poolId": 12346,
        "percentile": 99.0
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 200


def test_calculate_quantile_002():
    data = {
        "poolId": 1234644444,
        "percentile": 99.0
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 404


def test_calculate_quantile_003():
    data = {
        "poolId": 12346,
        "percentile": 100
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 200


def test_calculate_quantile_004():
    data = {
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 400


def test_calculate_quantile_005():
    data = {
        "poolId": 12346,
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 400


def test_calculate_quantile_006():
    data = {
        "percentile": 99,
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 400


def test_calculate_quantile_007():
    data = {
        "poolId": 12346,
        "percentile": 101
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 400


def test_calculate_quantile_008():
    data = {
        "poolId": 12346,
        "percentile": 0
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 200
