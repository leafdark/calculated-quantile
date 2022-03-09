import requests

BASE = "http://127.0.0.1:5000/"


def test_calculate_quantile_normal():
    data = {
        "poolId": 12346,
        "percentile": 99.0
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 200


def test_calculate_quantile_pool_id_not_exist():
    data = {
        "poolId": 1234644444,
        "percentile": 99.0
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 500


def test_calculate_quantile_percentile_is_100():
    data = {
        "poolId": 12346,
        "percentile": 100
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 200


def test_calculate_quantile_not_params():
    data = {
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 400


def test_calculate_quantile_not_percentile():
    data = {
        "poolId": 12346,
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 400


def test_calculate_quantile_not_pool_id():
    data = {
        "percentile": 99,
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 400


def test_calculate_quantile_percentile_over_100():
    data = {
        "poolId": 12346,
        "percentile": 101
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 400


def test_calculate_quantile_percentile_is_0():
    data = {
        "poolId": 12346,
        "percentile": 0
    }
    response = requests.post(f'{BASE}pool-calculator', data)
    assert response.status_code == 200
