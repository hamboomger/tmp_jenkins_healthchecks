#!/usr/bin/python3

import pandas as pd
import plotly.express as px
from pathlib import Path

file_name = '2024-11-08.csv'

local_jenkins_logs = Path('./jenkins_local_logs') / 'logs'
remote_server_logs = Path('./remote_logs') / 'logs'


# Local logs
df1 = pd.read_csv(local_jenkins_logs / file_name)
df1['Timestamp'] = pd.to_datetime(df1['Timestamp'])

fig1 = px.line(df1, x ='Timestamp', y =df1.columns[1:], title='Local logs')
fig1.show()

# Remote logs
df2 = pd.read_csv(remote_server_logs / file_name)
df2['Timestamp'] = pd.to_datetime(df2['Timestamp'])

fig2 = px.line(df2, x ='Timestamp', y =df2.columns[1:], title='Remote logs')
fig2.show()
