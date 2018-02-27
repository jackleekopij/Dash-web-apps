import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from helpers import create_checklist_from_vector,generate_selection_table

from openpyxl import load_workbook
from datetime import datetime
from openpyxl.utils.dataframe import dataframe_to_rows

import pandas as pd

import numpy as np


# Create the Dash app and any of the global variables
app = dash.Dash()

app.config['suppress_callback_exceptions']=True

vector_to_graph_map = [["Pressure"," Bottom hole pressure"],
          ["Pressure"," Tubing head pressure"],
          ["Rates"," Oil production rate"],
          ["Rates"," Gas production rate"],
          ["Rates"," Water production rate"],
          ["Rates"," Liquid production rate"],
          ["Ratios_Performance"," Oil-gas ratio"],
          ["Ratios_Performance"," Water cut"],
          ["Ratios_Performance"," Gas-oil ratio"],
          ["Ratios_Performance"," Water-gas ratio"],
          ["Ratios_Performance"," Gas-liquid ratio"],
          ["Cumulative", " Oil production cumulative"],
          ["Cumulative", " Water production cumulative"],
          ["Cumulative"," Gas production cumulative"]]

json_property_map = {x[1]:x[0] for x in vector_to_graph_map}
print("The map value for  Bottom hole pressure: {0}" .format(json_property_map[" Bottom hole pressure"]))

# Read in the data into the Dash app
wb = load_workbook('Gap_getgapresults_prod.xlsm')
sheet_names = wb.get_sheet_names()
sheet_names = [x for x in sheet_names if 'IX' in x]
ws = wb['IX_0']

data = ws.values

well = next(data)[0:]
idx = next(data)[0:]
idx2 = next(data)[0:]

index = [idx, idx2]
tuples = list(zip(*index))

final_index = pd.MultiIndex.from_tuples(tuples, names=['equipment', 'vector'])


df = pd.DataFrame(data, columns=final_index)

list_to_checklist = df.columns.levels[0]
list_to_checklist2 = df.columns.levels[1]

y_data = df['PLA01ST1', ' Bottom hole pressure'].tolist()
x_data = pd.to_datetime(df['Equipment', 'Vector'], format="%d/%m/%Y").tolist()
z_data = df['PLA01ST1', ' Gas production rate'].tolist()


# create the app layout for t
app.layout = html.Div(children=[
    html.H1(children='Pluto res eng overview'),
    #dcc.Graph(id='graph-1'),
    generate_selection_table(sheet_names[0],dcc.Checklist(
        id="checklist-1",
        options=[{'label': x, 'value': x} for x in list_to_checklist],
        values=[list_to_checklist[0]],
        labelStyle={'display': 'inline-block'}),
        dcc.Checklist(
            id="checklist-1a",
            options=[{'label': x, 'value': x} for x in list_to_checklist2],
            values=[list_to_checklist2[0]],
            labelStyle={'display': 'inline-block'})
                             ),
    html.Div(id="graph-1"),
    html.Div(id="my-div"),
    html.Div(id="my-div2"),
    #dcc.Graph(id='double-axis',figure={"data":[{'x':x_data,'y':y_data, 'yaxis':"y1"},{'x':x_data,'y':z_data,'yaxis':"y2"}],
    #   "layout":{"yaxis":{"title":"yaxis1"},"yaxis2":{"title":"yaxis2", "overlaying":"y","side":"right"}}})
])




# Define callbacks for functions
@app.callback(Output('my-div', 'children'), [Input("checklist-1",'values')])
def checklist_update(checklist):
    return " ".join(checklist)

@app.callback(Output('my-div2', 'children'), [Input("checklist-1a",'values')])
def checklist_update(checklist):
    return " ".join(checklist)


#@app.callback(Output('graph-1', 'figure'), [Input('checklist-1', 'values'), Input('checklist-1a', 'values')])
@app.callback(Output('graph-1', 'children'), [Input('checklist-1', 'values'), Input('checklist-1a', 'values')])
def get_graph(checklist1,checklist1a):
    data_pressure_list = [ ]
    data_rates_list = [ ]
    data_ratios_performance_list = [ ]
    data_cumulative_list  = [ ]

    cluster_list = [ ]

    graphs = [ ]
    counter = 1
    for i in checklist1:
        for j in checklist1a:
            print("The type to match on: {0}: ".format(type(j)))
            print("The value to match on: {0}: ".format(j))
            # Put individual graph logic here:
            if json_property_map[str(j)] == "Pressure":
                try:
                    data_pressure_list.append({'x':x_data, 'y':df[i,j].tolist(), 'name':str(i) + str(j), 'yaxis':'y'+str(counter)})
                    if (json_property_map[j] not in  cluster_list):
                        cluster_list.append(json_property_map[j])
                except:
                    print("No key for equipment: {},  vector: {}".format(i,j))

            if json_property_map[j] == "Rates":
                try:
                    data_rates_list.append({'x':x_data, 'y':df[i,j].tolist(), 'name':str(i) + str(j), 'yaxis':'y'+str(counter)})
                    if (json_property_map[j] not in  cluster_list):
                        cluster_list.append(json_property_map[j])
                except:
                    print("No key for equipment: {},  vector: {}".format(i,j))

            if json_property_map[j] == "Ratios_Performance":
                try:
                    data_ratios_performance_list.append({'x':x_data, 'y':df[i,j].tolist(), 'name':str(i) + str(j), 'yaxis':'y'+str(counter)})
                    if (json_property_map[j] not in  cluster_list):
                        cluster_list.append(json_property_map[j])
                except:
                    print("No key for equipment: {},  vector: {}".format(i,j))

            if json_property_map[j] == "Cumulative":
                try:
                    data_cumulative_list.append({'x':x_data, 'y':df[i,j].tolist(), 'name':str(i) + str(j), 'yaxis':'y'+str(counter)})
                    if (json_property_map[j] not in  cluster_list):
                        cluster_list.append(json_property_map[j])
                except:
                    print("No key for equipment: {},  vector: {}".format(i,j))

    if "Pressure" in cluster_list:
        graphs.append(dcc.Graph(id="pressure", figure={'data':data_pressure_list ,'layout':{'legend':{'x': 0}}}))
    if "Rates" in cluster_list:
        graphs.append(dcc.Graph(id="rates", figure={'data': data_rates_list,'layout':{'legend':{'x': 0}}}))
    if "Ratios_Performance" in cluster_list:
        graphs.append(dcc.Graph(id="ratio_perf", figure={'data': data_ratios_performance_list,'layout':{'legend':{'x': 0}}}))
    if "Cumulative" in cluster_list:
        graphs.append(dcc.Graph(id="cumulative", figure={'data': data_cumulative_list,'layout':{'legend':{'x': 0}}}))

    return graphs

if __name__ == '__main__':
    app.run_server(debug=True)