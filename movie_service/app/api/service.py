import json
import os
import httpx
from typing import Union

CAST_SERVICE_HOST_URL = 'http://127.0.0.1:8001/api/v1/casts/'
url = os.environ.get('CAST_SERVICE_HOST_URL') or CAST_SERVICE_HOST_URL


def is_cast_present(cast: Union[int, str]):
    r = httpx.get(f'{url}{cast}')
    return json.loads(r.text)['id'] if r.status_code == 200 else False


def create_cast(cast: str):
    r = httpx.post(f'{url}', json={"name": cast})
    if r.status_code == 201:
        return json.loads(r.text)['id']
    else:
        raise ConnectionError(f'Can\'t create cast {cast}: cast service response {r.status_code}')
