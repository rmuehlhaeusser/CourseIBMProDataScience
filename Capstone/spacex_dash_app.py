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

#fill the drop down
site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': entry, 'value': entry} for entry in spacex_df['Launch Site'].unique()]
# slider
slider_ticks  = {i: str(i) for i in range(0, 10001, 1000)}
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id = 'site-dropdown', options = site_options, value = 'ALL',
                                             placeholder = 'Select a Launch site here',
                                             searchable = True,
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000,marks=slider_ticks,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(site):
    filtered_df = spacex_df[spacex_df["class"]==1].groupby("Launch Site").size().reset_index(name='Count')
    if site == 'ALL':
        fig = px.pie(filtered_df, values='Count',names='Launch Site', title='Total Success Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df["Launch Site"]==site].groupby("class").size().reset_index(name='Count')
        fig = px.pie(filtered_df, values='Count',names='class', title=f'Total Success Launches for Site {site}')
        return fig 
    return html.H1('nothing selected')  



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(site,payloadrange):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=payloadrange[0]) & (spacex_df['Payload Mass (kg)']<=payloadrange[1])]
    if site == 'ALL':
        fig = px.scatter(data_frame=filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',hover_data=['Launch Site'],title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = filtered_df[filtered_df["Launch Site"]==site]
        fig = px.scatter(data_frame=filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',hover_data=['Launch Site'],title=f'Correlation between Payload and Success for Site {site}')
        return fig
    return html.H1('nothing selected') 


# Run the app
if __name__ == '__main__':
    app.run_server()
