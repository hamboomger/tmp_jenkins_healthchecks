#!/usr/bin/python3
import json
from zoneinfo import ZoneInfo

import psutil
import os
import requests
from pathlib import Path
from datetime import date, datetime

logs_dir = Path(__file__).parent.resolve() / 'logs'
today = str(date.today())

logs_dir.mkdir(exist_ok=True, parents=True)

logs_file = f'{today}.json'
file_path = logs_dir / logs_file
if not file_path.exists():
    file_path.write_text('[]')

json_contents: list = []
with file_path.open('r') as f:
    json_contents = json.load(f)

def get_json_record():
    naive_datetime = datetime.now()
    server_datetime = naive_datetime.astimezone()
    return {
        'timestamp': server_datetime.isoformat(),
        'mem_percent': psutil.virtual_memory().percent,
        'cpu_percent': psutil.cpu_percent(interval=5),
        'disk_usage': psutil.disk_usage(os.sep).percent
    }

json_record = get_json_record()
json_contents.append(json_record)

with file_path.open('w') as f:
    json.dump(json_contents, f, indent=4)

res = requests.post('https://tmp-jenkins-healthchecks.onrender.com/log-entry',
              json={ 'fileName': logs_file, 'entry': json_record })
res.raise_for_status()

print(f'Added telemetry data for {json_record["timestamp"]}')
