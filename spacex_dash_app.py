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
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                ],
                                value='ALL',
                                placeholder="Select a Launch Site",
                                searchable=True,
                                style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={i: str(i) for i in range(0, 10001, 1000)},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # If ALL sites are selected, use all rows in the dataframe spacex_df
        fig = px.pie(spacex_df, names='class', title='Success vs. Failure for All Sites')
    else:
        # If a specific launch site is selected, filter the dataframe spacex_df for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Render and return a pie chart graph to show the success (class=1) and failed (class=0) counts for the selected site
        fig = px.pie(filtered_df, names='class', title=f'Success vs. Failure for {selected_site}')
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'),
               Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, payload_range):
    # Filter the dataframe based on the selected launch site and payload range
    if selected_site == 'ALL':
        # Render a scatter plot to display all values for variable Payload Mass (kg) and variable class
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Payload vs. Success for All Sites',
                         labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Outcome'},
                         )
    else:
        # If a specific launch site is selected, filter the spacex_df
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Render a scatter chart to show values Payload Mass (kg) and class for the selected site
        # Color-label the point using Booster Version Category
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Success for {selected_site}',
                         labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Outcome'},
                         )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
