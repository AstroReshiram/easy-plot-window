import math

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from math import cos
import plotly.graph_objs as go
import time
import threading
import numpy as np
import random

from PlotWindow import PlotWindow


def initialize_coords(xmin, xmax, ymin, ymax, vel, n):
    return np.array(
        [[random.uniform(xmin, xmax),
          random.uniform(ymin, ymax),
          random.uniform(-vel, vel),
          random.uniform(-vel, vel)]
         for _ in range(n)]
    )

global coords1
vel = 0.05

coords1 = initialize_coords(0, 5, 0, 10, vel, 10)
coords2 = initialize_coords(5, 10, 0, 10, vel, 100)

def move_coords():
    """Generate ten x y coordinates"""
    next_time = time.time()
    while True:
        if time.time() > next_time:
            coords1[(coords1[:, 0] > 10) | (coords1[:, 0] < 0), 2] *= -1
            coords1[(coords1[:, 1] > 10) | (coords1[:, 1] < 0), 3] *= -1
            coords1[:, 0:2] = coords1[:, 0:2] + coords1[:, 2:4]

            # coords2[(coords2[:, 0] > 10) | (coords2[:, 0] < 0), 2] *= -1
            # coords2[(coords2[:, 1] > 10) | (coords2[:, 1] < 0), 3] *= -1
            # coords2[:, 0:2] = coords2[:, 0:2] + coords2[:, 2:4]
            next_time += 0.05
            find_overlap()
        else:
            time.sleep(0.01)

def vibrate_coords():
    """Generate ten x y coordinates"""
    next_time = time.time()
    while True:
        if time.time() > next_time:
            coords1[:, 0:2] = coords1[:, 0:2] + np.array([[random.uniform(-vel, vel), random.uniform(-vel, vel)]for _ in range(len(coords1))])
            next_time += 0.05
            find_overlap()
        else:
            time.sleep(0.01)


def find_overlap():
    diameter = 0.1
    # Overlapping Xs
    for p1 in coords1:
        # Get the Xs
        Xs = (coords1[:, 0] != p1[0]) & (coords1[:, 0] - 0.1 < p1[0]) & (p1[0] < coords1[:, 0] + 0.1)
        Ys = (coords1[:, 1] != p1[1]) & (coords1[:, 1] - 0.1 < p1[1]) & (p1[1] < coords1[:, 1] + 0.1)
        p2 = coords1[Xs & Ys, :]

        # if len(p2) > 0:
        #     print((p1,p2))
        #     print((p1, p2))
        #
        #     # Calculate angle between the two points
        #     # Or rather the ratio
        #     # Take diameter as 0.1
        #     diff = p2 - p1
        #
        #     # Calculate Angle of Collision == ratio of y/x where H is always 0.1
        #     # theta = math.acos(diff[0]/0.1)
        #
        #     # Get the angle which is tan-1 o a
        #     a = diff[0,0]
        #     o = diff[0,1]
        #     theta = math.atan(o/a)
        #     psi = math.pi/2 - theta
        #
        #     ux1 =
        #     uy1
        #     ux2
        #     uy2
        #
        #     # Calculate new vel for p1
        #     # cos angle
        #     # new_vx = vx cos theta + vy sin psi and
        #     # new_vy = vx sin theta + vy cos psi
        #     # where cos theta = A/H sin theta = O / H tan theta = O/A
        #

        # Only calculate once



t = threading.Thread(target=move_coords, daemon=True)
t.start()

dash_app = dash.Dash(__name__, update_title=None)

dash_app.layout = html.Div([
    dcc.Graph(id='live-graph', style={'height': '100vh'}),
    dcc.Interval(
        id='interval-component',
        interval=100,  # in milliseconds
        n_intervals=0
    )
])


@dash_app.callback(Output('live-graph', 'figure'),
                   Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    data = go.Scatter(
        x=coords1[:, 0],
        y=coords1[:, 1],
        mode='markers',
        marker=dict(size=10, color='red')
    )

    # data2 = go.Scatter(
    #     x=coords2[:, 0],
    #     y=coords2[:, 1],
    #     mode='markers',
    #     marker=dict(size=10, color='blue')
    # )

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
