#!/usr/bin/python3

import pandas as pd
import plotly.express as px
from pathlib import Path

file_name = '2024-11-08.json'

local_jenkins_logs = Path('./jenkins_local_logs') / 'logs'
remote_server_logs = Path('./remote_logs') / 'logs'


# Local logs
df1 = pd.read_csv(local_jenkins_logs / file_name)

fig1 = px.line(df1, x ='timestamp', y =df1.columns[1:-1], title='Local logs')
fig1.show()

# Remote logs
df2 = pd.read_json(remote_server_logs / file_name)

fig2 = px.line(df2, x ='timestamp', y =df2.columns[1:-1], title='Remote logs')
fig2.show()
