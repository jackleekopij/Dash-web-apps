import dash
from dash.dependencies import Input, Output
from dash.dependencies import Event
import dash_core_components as dcc
import dash_html_components as html
from loremipsum import get_sentences
from helpers_html import *
from helpers_data import *
import datetime


# Set application defaults
app = dash.Dash()
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True


tab_names = ["Pomodoro", "JIRA", "Long-term goals"]
pomodoro_tabs = ["Pomodoro", "Break"]

global minutes
global seconds
minutes = 0
seconds = 10

# Set the HTML layout for the page
app.layout = html.Div([
    html.Div(
        dcc.Tabs(
            tabs=set_tab_labels(tab_names),
            value=1,
            id='tabs',
            vertical=True,
            style={
                'height': '100vh',
                'borderRight': 'thin lightgrey solid',
                'textAlign': 'left'
            }
        ),
        style={'width': '20%', 'float': 'left'}
    ),
    html.Div(dcc.Tabs(
        tabs=[{'label':'Pomodoro', 'value':"pom"},{'label':'Break', 'value':'break'} ],
        value=0,
        id='tabs-pomodoro',
        vertical=False)),
    html.Div(
        html.Div(id='tab-output'),
        style={'width': '80%', 'float': 'right'}
    ),
    dcc.Interval(id="interval-component", interval=1 * 1000),
    html.Div(id="reset")
],
    style={
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto',
    'textAlign':'center',
})



@app.callback(Output('tab-output', 'children'), inputs=[Input('tabs', 'value')], events=[Event("interval-component","interval")])
def display_content(value):
    global minutes
    global seconds
    if minutes == 25:
        interval = "25"
        minutes -= 1
    if seconds > 0:
        interval = str(minutes) + ":" + str(seconds)
        seconds -= 1
    else:
        seconds = 59
        minutes -= 1

    if value == 0 and minutes >= 0:
    #if  minutes >= 0:
        return html.Div( [html.H1(interval),html.Div(dcc.Input(value="Enter Pomodoro goal", type="text")), html.Div(html.Button("Start", id="start-timer", style={"height":"75", "width":"200"}))],style={'margin-top': '250'})
    elif minutes < 0:
        return html.Div([html.H1("Pomodoro over!"),
                         html.Div([html.Button("Reset", id="reset-button", style={"height": "75", "width": "200"}),
                                   html.Button("Start", id="start-timer", style={"height": "75", "width": "200"})])],
                        style={'margin-top': '250'})
    else:
        return html.Div(["NO response yet"])

@app.callback(Output("reset", "children"), [Input("reset-button", "n_clicks")])
def global_resets(n_clicks):
    global minutes
    global seconds
    minutes = 0
    seconds = 60

if __name__ == '__main__':
    app.run_server(debug=True)