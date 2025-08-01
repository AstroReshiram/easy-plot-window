import random
import numpy as np
import plotly.graph_objects as go

from PlotWindow import PlotWindow

def generate_coords():
    """Generate ten x y coordinates"""
    return np.array([[random.uniform(0,10), random.uniform(0,10)] for x in range(10)])

coords1 = generate_coords()

# Create the scatter plot using Plotly
fig = go.Figure(data=go.Scatter(
    x=coords1[:, 0],
    y=coords1[:, 1],
    mode='markers',
    marker=dict(size=10, color='blue', opacity=0.6),
))

# Update layout for better visualization
fig.update_layout(
    title='Scatter Plot of Random Coordinates',
    xaxis_title='X-axis',
    yaxis_title='Y-axis',
)



# b = PlotWindow(fig)
# b.run()
# b.exit()

import plotly.express as px
df = px.data.gapminder()
fig1 = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country",
           log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])

# app = QApplication([])
PlotWindow().show([fig, fig1])
#PlotWindow(fig1)

# app.exec()