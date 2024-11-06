#!/bin/python3

import psutil
import os
from pathlib import Path
from datetime import date, datetime

logs_dir = Path('/home/ubuntu/test-dir/logs')
today = str(date.today())

logs_dir.mkdir(exist_ok=True, parents=True)

logs_file = logs_dir / f'{today}.csv'
if not logs_file.exists():
    logs_file.write_text('Timestamp,Cpu usage,Mem usage,Disk usage\n')

with logs_file.open('a') as f:
    timestamp = str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    mem_percent = psutil.virtual_memory().percent
    cpu_percent = psutil.cpu_percent(interval=5)
    disk_usage = psutil.disk_usage(os.sep).percent
    f.write(f'{timestamp},{cpu_percent},{mem_percent},{disk_usage}\n')

    print(f'Add telemetry data for {timestamp}')
