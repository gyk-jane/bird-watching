"""Visualizes bird data using a horizontal bar chart.

The horizontal bar chart contains unique birds, ordered from most seen to least seen. Hovering over each bar should show its bird species name and number of sightings.

"""
import sys
sys.path.append(".")

from loads import connect_load
from itertools import cycle
import plotly.graph_objects as go
import plotly.express as px
import inspect
import pandas as pd

def get_xy(cursor):
    """Get (x,y) coordinates from the daily_birds table, where 
    (x,y) => (frequency of bird sighting, bird)
    
    Args:
        cursor (Cursor): a pymysql object that allows for connection to the database
    Returns:
        Tuple: tuples containing unpacked x, y values
        
    """
    DAILY_BIRDS = 'daily_birds'
    
    get_xy_query = inspect.cleandoc(f"""
                                   SELECT howMany, comName
                                   FROM {DAILY_BIRDS}
                                   WHERE howMany > 0
                                   ORDER BY howMany DESC, comName ASC;""")
    cursor.execute(get_xy_query)
    coords = cursor.fetchall()
    x, y = zip(*coords)
    
    return x, y

def graph_spec(x, y):
    return {'data': [
        go.Bar(
            x = x,
            y = y,
            orientation = 'h',
            marker = dict(
                color = x,
                colorscale = 'brwnyl'
                )
            )
        ],
        'layout': go.Layout(
            font = dict(size=13),
            xaxis = dict(automargin=True),
            yaxis = dict(tickangle=-25, showticklabels=True, automargin=True, autorange="reversed"),
            margin = dict(t=20, b=20, r=10)
        )
    }
    
def plot(cursor, x, y):
    """Shows the bar chart.
    
    Args:
        cursor (Cursor): a pymysql object that allows for connection to the database
    
    """
    spec = graph_spec(x, y)
    fig = go.Figure(spec['data'], spec['layout'])
    fig.show()
  
