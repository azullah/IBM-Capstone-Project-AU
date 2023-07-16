# Import required libraries
import pandas as pd
import numpy as np
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

pio.renderers.default = "browser"

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
site_list = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=site_list,value=site_list, multi=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=min_payload,max=max_payload,
                                                step=1,value=[(min_payload/2), (max_payload/2)],
                                                marks={0: '0 kg',
                                                       2500: '2500 kg',
                                                       5000: '5000 kg',
                                                       7500: '7500 kg',
                                                      10000: '10000 kg'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

def get_graph(pick_list):
    # Select Launch site data
    #pick_list = list(pick_list)
    sites_df = spacex_df[spacex_df['Launch Site'].isin(pick_list)]
    fig = px.pie(sites_df, names='Launch Site',
                 values='class',
                 title='Success rates by Launch Site')
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               Input(component_id='payload-slider', component_property='value'))

def get_graph(range_val):
    # Select Launch site data
    #pick_list = list(pick_list)
    df_subset = spacex_df[spacex_df['Payload Mass (kg)'].between(range_val[0],range_val[1])]

    fig = px.scatter(df_subset, x='Payload Mass (kg)',
                 y='class',color='Launch Site',
                 title='Correlation between payload and success / failure')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
