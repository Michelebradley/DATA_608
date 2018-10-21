import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
from plotly import graph_objs as go
from plotly.graph_objs import *
from flask import Flask
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import flask

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)
mapbox_access_token = 'pk.eyJ1IjoibWljaGVsZWJyYWRsZXkiLCJhIjoiY2puaHdjdWVpMGljMDNrbzVjNW5zZTVrMSJ9.XWvfrYtiyGeHiv7K2tBO-Q'
health = trees.health
health[health == "Poor"] = 'rgb(255, 0, 0)'
health[health == "Fair"] = 'rgb(255, 255, 102)'
health[health == "Good"] = 'rgb(0, 204, 102)'

app = dash.Dash('app', server=server)

#hg app.scripts.config.serve_locally = False
#kljhk dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Filter By Number of Stewards. Color indicates health of Tree'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'None', 'value': 'None'},
            {'label': '1 or 2', 'value': '1or2'},
            {'label': '3 or 4', 'value': '3or4'},
            {'label': 'All', 'value': 'All'}
        ],
        value='All'
    ),
    dcc.Graph(id='my-graph')
], className="container")

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    if selected_dropdown_value == "All":
        trees2 = trees
    else:
        trees2 = trees[trees['steward'] == selected_dropdown_value]

    return go.Figure(
        data=Data([
            Scattermapbox(
                lat=trees2['latitude'],
                lon=trees2['longitude'],
                mode='markers',
                marker=dict(
                    size=6,
                    color = health
                ),
                text=trees2['steward'],
            ),
        ]),
        layout=Layout(
            autosize=True,
            height=750,
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=40.7272,
                    lon=-73.991251
                ),
                pitch=0,
                zoom=9
            ),
        )
    )

app.css.append_css({
    'external_url': (
    'https://cdn.rawgit.com/plotly/dash-app-stylesheets/96e31642502632e86727652cf0ed65160a57497f/dash-hello-world.css'
    )
})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })


if __name__ == '__main__':
    app.run_server()