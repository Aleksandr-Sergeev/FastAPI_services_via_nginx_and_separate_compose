import json
import os
import httpx
from typing import Union

CAST_SERVICE_HOST_URL = 'http://localhost:8002/api/v1/casts/'
url = os.environ.get('CAST_SERVICE_HOST_URL') or CAST_SERVICE_HOST_URL


def is_cast_present(cast: Union[int, str]):
    r = httpx.get(f'{url}{cast}')
    return True if r.status_code == 200 else False


def create_cast(cast: str):
    r = httpx.post(f'{url}', json={"name": cast})
    print(r)
    return r