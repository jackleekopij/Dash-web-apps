import dash
from dash.dependencies import Input, Output, State
from dash.dependencies import Event
import dash_core_components as dcc
import dash_html_components as html
from loremipsum import get_sentences
from helpers_html import *
from helpers_data import *
import datetime
from helpers_mongo import *

from pymongo import MongoClient
import datetime
import pprint
from bson.objectid import ObjectId


# Set application defaults
app = dash.Dash()
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True


tab_names = ["Pomodoro", "JIRA", "Long-term goals"]
pomodoro_tabs = ["Pomodoro", "Break"]




global minutes
global seconds
minutes = 25
seconds = 0




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
        style={'width': '20%', 'float': 'left', 'margin-top':'-150'}
    ),
    html.Div([html.Button("Pomodoro", id="pomodoro-button", style={"height": "50", "width": "150"}),
        html.Button("Break", id="break-button", style={"height": "50", "width": "150"})],style={'margin-top': '150'}),
    html.Div(
        html.Div(id='tab-output'),
        style={'width': '80%', 'float': 'right'}
    ),
    html.Div(dcc.Input(id="pomodoro-task", value="Enter Pomodoro goal", type="text")),
    html.Button("Start", id="start-timer", style={"height":"75", "width":"200"}),\
    html.Button("Stop", id="stop-timer", style={"height":"75", "width":"200"}),
    html.Div(id="task-name"),
    html.Div(id="interval-start"),
    html.Div(id="reset"),
    html.Div(id="hidden-div"),
    html.Div(id="break-hidden"),
    html.Div(id="pomodoro-hidden")],
    style={
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto',
    'textAlign':'center'}
)





####
# App callbacks
####




@app.callback(Output("break-hidden", "children"), [Input("break-button", "n_clicks")])
def change_to_break(click):
    if click != None:
        global minutes
        global seconds
        minutes = 0
        seconds = 10

@app.callback(Output("pomodoro-hidden", "children"), [Input("pomodoro-button", "n_clicks")])
def change_to_break(click):
    if click != None:
        global minutes
        global seconds
        minutes = 0
        seconds = 30




@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')], [State("pomodoro-button", "n_clicks"), State("break-button", "n_clicks"), State("pomodoro-task", "value")], events=[Event("interval-component","interval")])
def display_content(value, pomodoro_button, break_button, task_string):
    global minutes
    global seconds
    if minutes == 25 and pomodoro_button == break_button:
        interval = "25"
        minutes -= 1
        seconds = 59
    elif seconds > 0:
        interval = str(minutes) + ":" + str(seconds)
        seconds -= 1
    else:
        seconds = 59
        minutes -= 1
        interval = str(minutes) + ":" + str(seconds)

    if value == 0 and minutes >= 0:
        return html.Div( [html.H1(interval)],style={'margin-top': '250'})
    elif minutes < 0 and pomodoro_button == break_button:
        if minutes == -1 and seconds == 58:
            write_goal_to_db = MongoDB()
            insert_output = write_goal_to_db.write_to_database(task_string)
            print(insert_output)
        return html.Div([html.H1("Pomodoro over!")],
                        style={'margin-top': '250'})
    elif minutes < 0 and pomodoro_button != break_button:
        return html.Div([html.H1("BREAK OVER!")],
                        style={'margin-top': '250'})
    else:
        return html.Div(["NO response yet"])




@app.callback(Output("reset", "children"), [Input("reset-button", "n_clicks")])
def global_resets(n_clicks):
    global minutes
    global seconds
    minutes = 0
    seconds = 60




@app.callback(Output("hidden-div", "children"), [Input("pomodoro-button", "n_clicks"),Input("start-timer", "n_clicks")])
def reset_counter(n_clicks, start_clicks):
    print("Number of clicks {0}".format(n_clicks))
    if start_clicks == None:
        global minutes
        global seconds
        minutes = 0
        seconds = 10




@app.callback(Output("task-name", "children"), [Input("start-timer", "n_clicks")], [State("pomodoro-task", "value")])
def get_pomodoro_goal(button, pomodoro_goal):
    if pomodoro_goal != "Enter Pomodoro goal":
        return html.H1(pomodoro_goal)
    else:
        return ""



@app.callback(Output("interval-start", "children"), [Input("start-timer", "n_clicks"), Input("stop-timer", "n_clicks")])
def start_interval(n_clicks, stop_clicks):
    if n_clicks > 0 and n_clicks > stop_clicks :
        return dcc.Interval(id="interval-component", interval=1 * 1000)
    if n_clicks == stop_clicks:
        return "Time stopped"
    else:
        return "Not yet started"



@app.callback(Output("stop-timer","n_clicks"), [Input("pomodoro-button", "n_clicks")], [State("stop-timer", "n_clicks")])
def stop_timer(clicks, stop_timer_clicks):
    if clicks != None:
        try:
            return stop_timer_clicks + 1
        except:
            return 1


if __name__ == '__main__':
    app.run_server(debug=True)

