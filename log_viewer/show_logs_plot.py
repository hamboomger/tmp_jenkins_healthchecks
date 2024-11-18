#!/usr/bin/python3

import pandas as pd
import plotly.express as px
from pathlib import Path

file_name = '2024-11-11-custom.json'

local_jenkins_logs = Path('./jenkins_local_logs') / 'logs'

# Local logs
df1 = pd.read_json(local_jenkins_logs / file_name)
df1['timestamp'] = pd.to_datetime(df1['timestamp']).dt.tz_convert('UTC')

# Flatten the docker info into a string format for hover text
df1['docker_info'] = df1['docker'].apply(lambda containers: "<br>".join(
    f"{c['name']}<br>    Mem: {c['mem']}<br>    CPU: {c['cpu']:.2f}%<br>    Command: {' '.join(c['command'])}"
    for c in containers
))

fig1 = px.line(df1, x ='timestamp', y=['mem_percent'], title='Local logs', markers=True, hover_data={'docker_info': True})

fig1.update_traces(marker=dict(size=8), hovertemplate='<br>'.join([
  "Time: %{x}",
  "Memory Percent: %{y}%",
  "Docker containers:",
  "%{customdata[0]}"
]))

fig1.show()
