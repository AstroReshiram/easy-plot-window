import random
import numpy as np
import plotly.graph_objects as go
from PlotWindow import PlotWindow

def generate_coords():
    """Generate ten x y coordinates"""
    return np.array([[random.uniform(0,10), random.uniform(0,10)] for x in range(10)])

coords = generate_coords()

# Create the scatter plot using Plotly
fig = go.Figure(data=go.Scatter(
    x=coords[:, 0],
    y=coords[:, 1],
    mode='markers',
    marker=dict(size=10, color='blue', opacity=0.6),
))

# Update layout for better visualization
fig.update_layout(
    title='Scatter Plot of Random Coordinates',
    xaxis_title='X-axis',
    yaxis_title='Y-axis',
)

PlotWindow(fig).run()