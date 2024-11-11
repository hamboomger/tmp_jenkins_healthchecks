#!/usr/bin/python3
import json
import docker

import psutil
import os
import requests
from pathlib import Path
from datetime import date, datetime

### Utils

def human_readable_size(size, decimal_places=2):
  for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']:
    if size < 1024.0 or unit == 'PiB':
      break
    size /= 1024.0
  return f"{size:.{decimal_places}f} {unit}"

def calculate_cpu_percent(stats):
  # Get CPU usage and system CPU usage from current and previous stats
  cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats["precpu_stats"]["cpu_usage"]["total_usage"]
  system_delta = stats["cpu_stats"]["system_cpu_usage"] - stats["precpu_stats"]["system_cpu_usage"]

  # Get the number of CPUs available
  online_cpus = stats["cpu_stats"].get("online_cpus", 1)  # Use 1 if online_cpus is not available

  # Calculate the CPU usage percentage
  if system_delta > 0 and online_cpus > 0:
    return (cpu_delta / system_delta) * online_cpus * 100.0
  else:
    return 0.0

### Script

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

def get_docker_containers_stats():
  client = docker.from_env()

  def get_stats(container):
    stat = container.stats(stream=False)
    return {
      # 'image': container.image,
      'name': container.name,
      'status': container.status,
      'mem': human_readable_size(stat['memory_stats']['usage']),
      'cpu': calculate_cpu_percent(stat),
      'command': container.attrs["Config"]["Cmd"]
    }

  return [get_stats(container) for container in client.containers.list()]

def get_json_record():
  naive_datetime = datetime.now()
  server_datetime = naive_datetime.astimezone()
  return {
    'timestamp': server_datetime.isoformat(),
    'mem_percent': psutil.virtual_memory().percent,
    'cpu_percent': psutil.cpu_percent(interval=5),
    'disk_usage': psutil.disk_usage(os.sep).percent,
    'docker': get_docker_containers_stats()
  }

json_record = get_json_record()
json_contents.append(json_record)

with file_path.open('w') as f:
  json.dump(json_contents, f, indent=4)

res = requests.post('https://tmp-jenkins-healthchecks.onrender.com/log-entry',
                    json={ 'fileName': logs_file, 'entry': json_record })
res.raise_for_status()

print(f'Added telemetry data for {json_record["timestamp"]}')
