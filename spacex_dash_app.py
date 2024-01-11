# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
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
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                            value='ALL',                                                
                                            placeholder="Select a Launch Site",
                                            searchable=True),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                    min=0, 
                                                    max=10000, 
                                                    step=1000,
                                                    value=[min_payload, max_payload],
                                                    marks={str(i): str(i) for i in range(0, 10000, 1000)}),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
 Output('success-pie-chart', 'figure'),
 Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
 if selected_site == 'ALL':
     # Use all rows in the dataframe
     filtered_df = spacex_df
     fig = px.pie(filtered_df, values='class', names='Launch Site', title='Total Success Launches by Site')
 else:
     # Filter the dataframe to include only data for the selected site
     filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
     fig = px.pie(filtered_df, values='class', names='class', title=f"Success Rates for {selected_site}")
 return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
   Output('success-payload-scatter-chart', 'figure'),
   [Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')]
)
def update_scatter_plot(selected_site, selected_payload):
   if selected_site == 'ALL':
       df_filtered = spacex_df
   else:
       df_filtered = spacex_df[spacex_df['Launch Site'] == selected_site]

   fig = px.scatter(df_filtered, 
                   x='Payload Mass (kg)', 
                   y='class', 
                   color='Booster Version Category',
                   title='Correlation between Payload and Success for all Sites')

   return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
