import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import time
from pynput import mouse
import threading
import numpy as np
import random

from PlotWindow import PlotWindow

# Global variable to store mouse coordinates
mouse_coords = {'x': 0, 'y': 0}


# Function to update mouse coordinates
def on_move(x, y):
    global mouse_coords
    mouse_coords['x'] = x
    mouse_coords['y'] = y


# Set up the mouse listener in a separate thread
def start_mouse_listener():
    with mouse.Listener(on_move=on_move) as listener:
        listener.join()


mouse_listener_thread = threading.Thread(target=start_mouse_listener)
mouse_listener_thread.start()

global coords
coords = np.array([[random.uniform(0, 10), random.uniform(0, 10)] for x in range(100)])
vel = 0.1


def generate_coords():
    """Generate ten x y coordinates"""
    global coords
    while True:
        # Move it randomly
        vels = np.array([[random.uniform(-vel, vel), random.uniform(-vel, vel)] for x in range(100)])
        coords = coords + vels
        time.sleep(0.03)


t = threading.Thread(target=generate_coords)
t.start()

dash_app = dash.Dash(__name__, update_title=None)

dash_app.layout = html.Div([
    dcc.Graph(id='live-graph', style={'height': '100vh'}),
    dcc.Interval(
        id='interval-component',
        interval=30,  # in milliseconds
        n_intervals=0
    )
])


@dash_app.callback(Output('live-graph', 'figure'),
                   Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    data = go.Scatter(
        x=coords[:, 0],
        y=coords[:, 1],
        mode='markers',
        marker=dict(size=10, color='red')
    )

    layout = go.Layout(
        title='Live Mouse Coordinates',
        xaxis=dict(range=[0, 10]),  # Adjust the range according to your screen resolution
        yaxis=dict(range=[0, 10])  # Adjust the range according to your screen resolution
    )

    return {'data': [data], 'layout': layout}


def run():
    dash_app.run_server(debug=True, use_reloader=False, host="127.0.0.1", port="9999")


if __name__ == '__main__':
    t = threading.Thread(target=run, daemon=True)
    t.start()

    PlotWindow().show("http://127.0.0.1:9999/")
    t.join()
