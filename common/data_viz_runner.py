"""Outputs the data visualization."""
import sys
sys.path.append(".")

from loads import connect_load
from data_viz import visualize
import plotly.graph_objects as go

def data_viz_main():
    cursor = connect_load.connect_to_db()
    x, y = visualize.get_xy(cursor)
    spec = visualize.graph_spec(x, y)
    fig = go.Figure(spec['data'], spec['layout'])
    fig.show()
