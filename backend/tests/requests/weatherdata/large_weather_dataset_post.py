import gzip
import time
from datetime import datetime, timedelta
from io import BytesIO
from random import uniform
import json

import requests

url = '35.217.32.244'
port = 80
jwt_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTc1Nzg4NzksIm5iZiI6MTU5NzU3ODg3OSwianRpIjoiYmEyOGUyY2YtMDNkMi00ZTg5LWIyM2UtMDdmYTlhZDg2NDNlIiwiZXhwIjoxNTk3NTgyNDc5LCJpZGVudGl0eSI6ImRlZmF1bHRfYWRtaW4iLCJmcmVzaCI6dHJ1ZSwidHlwZSI6ImFjY2VzcyIsInVzZXJfY2xhaW1zIjp7InJvbGUiOiJBRE1JTiIsInN0YXRpb25faWQiOm51bGx9fQ.bLhAti040BZYr1Y7nX6PVPmJRQgJSsu9XgKnearQw_k'

start_timepoint = datetime(year=2020, month=8, day=1, hour=0, minute=0, second=0)
end_timepoint = datetime(year=2020, month=9, day=1, hour=0, minute=0, second=0)
time_delta = timedelta(minutes=10)


def truncate_digits(number, num_digits=3) -> str:
    return '{:.{}f}'.format(number, num_digits)


def zip_payload(object_payload) -> bytes:
    json_payload = json.dumps(object_payload)
    byte_stream = BytesIO()
    with gzip.GzipFile(fileobj=byte_stream, mode='w') as g:
        g.write(bytes(json_payload, 'utf8'))

    return byte_stream.getvalue()


payload = []

timepoint = start_timepoint
rain_counter = 0
while timepoint < end_timepoint:
    rain_counter += uniform(0, 20)

    dataset_at_timepoint = {
        'timepoint': timepoint.isoformat(),
        'station_id': 'TES',
        'pressure': truncate_digits(uniform(980, 1050)),
        'uv': truncate_digits(uniform(0, 12)),
        'rain_counter': truncate_digits(rain_counter),
        'speed': truncate_digits(uniform(0, 120)),
        'gusts': truncate_digits(uniform(0, 200)),
        'direction': truncate_digits(uniform(0, 360)),
        'wind_temperature': truncate_digits(uniform(-30, 50)),
        'temperature_humidity': [
            {
                'sensor_id': 'OUT1',
                'temperature': truncate_digits(uniform(-30, 50)),
                'humidity': truncate_digits(uniform(0, 100))
            },
            {
                'sensor_id': 'IN',
                'temperature': truncate_digits(uniform(10, 30)),
                'humidity': truncate_digits(uniform(20, 80))
            }
        ]
    }

    payload.append(dataset_at_timepoint)

    timepoint += time_delta

headers = {
    'Authorization': 'Bearer {}'.format(jwt_token),
    'Content-Encoding': 'gzip',
    'Content-Type': 'application/json'
}

start_time = time.time()
r = requests.post('http://{}:{}/api/v1/data'.format(url, port), data=zip_payload(payload), headers=headers)
end_time = time.time()
r.raise_for_status()
print('Request took {} ms, status code {}'.format((end_time - start_time) * 1000, r.status_code))
