#!/usr/bin/python3

import pandas as pd
import plotly.express as px
from pathlib import Path

file_name = '2024-11-05.csv'
df = pd.read_csv(Path('./jenkins_local_logs') / 'logs' / file_name)
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d-%m-%Y %H:%M:%S')

fig = px.line(df, x = 'Timestamp', y = df.columns[1:])
fig.show()
