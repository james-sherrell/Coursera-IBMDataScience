# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[{'label':'All Sites', 'value':'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                    ],  
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min = 0, max = 10000, step = 1000,
                                    value = [min_payload,max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def chosen_site_successes(site):
    if site=='ALL':
        data = spacex_df[spacex_df['class']==1].groupby("Launch Site")['class'].value_counts().reset_index()
        title = "Launch Success/Failure for All Sites"
        fig = px.pie(data, values='count', title=title, names='Launch Site')
    else:
        t = spacex_df[ spacex_df['Launch Site'] == site]
        data = pd.DataFrame(columns = ['class','count'])
        data.loc[0] = [0, t[t['class']==0].shape[0]]
        data.loc[1] = [1, t[t['class']==1].shape[0]]
        title = f"Launch Success/Failure for {site}"
        fig = px.pie(data, values='count', title=title, names='class')
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'), 
        Input(component_id='payload-slider', component_property='value')
    ]
)
def chosen_site_payloads(site, min_max):
    if site=='ALL':
        data = spacex_df
        title = "Launch Success/Failure for Payload Masses"   
    else:
        data= spacex_df[spacex_df['Launch Site'] == site]
        title = f"Launch Success/Failure for Payload Masses at {site}" 
    
    return px.scatter(data_frame=data, x='Payload Mass (kg)', y='class', color='Booster Version', title=title, range_x = min_max)


# Run the app
if __name__ == '__main__':
    app.run()
