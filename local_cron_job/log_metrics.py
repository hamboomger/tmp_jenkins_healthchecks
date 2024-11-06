#!/usr/bin/python3
import json

import psutil
import os
import requests
from pathlib import Path
from datetime import date, datetime

logs_dir = Path('./logs')
today = str(date.today())

logs_dir.mkdir(exist_ok=True, parents=True)

logs_file = f'{today}.csv'
file_path = logs_dir / logs_file
if not file_path.exists():
    file_path.write_text('Timestamp,Cpu usage,Mem usage,Disk usage\n')

with file_path.open('a') as f:
    timestamp = str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    mem_percent = psutil.virtual_memory().percent
    cpu_percent = psutil.cpu_percent(interval=5)
    disk_usage = psutil.disk_usage(os.sep).percent

    log_entry = f'{timestamp},{cpu_percent},{mem_percent},{disk_usage}\n'
    f.write(log_entry)

    res = requests.post('https://tmp-jenkins-healthchecks.onrender.com/log-entry',
                  json={ 'fileName': logs_file, 'entry': log_entry })
    res.raise_for_status()

    print(f'Added telemetry data for {timestamp}')
