"""Visualizes bird data using a horizontal bar chart.

The horizontal bar chart contains unique birds, ordered from most seen to least seen. Hovering over each bar should show it's bird information and picture pulled from the Wikipedia API.

"""
import plotly.express as px
 
df = px.data.tips()
fig = px.bar(df, x="total_bill", y="day", orientation='h')
# fig.show()

def get_x_y():
    """Get (x,y) coordinates from the daily_birds table, where 
    (x,y) => (frequency of bird sighting, bird)
    
    Returns:
        List: a list of [x,y]
    """