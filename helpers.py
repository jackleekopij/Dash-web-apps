import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


def create_checklist_from_vector(list_to_checklist):
    options_list = [{'label': x, 'value': x} for x in list_to_checklist]
    return dcc.Checklist(
        options=options_list,
        values=[options_list[0]],
        labelStyle={'display': 'inline-block'})


def generate_selection_table(sheet_name, e_name, v_name):
    return html.Table(
        # Header
        [html.Tr([html.Th("Sheet name"), html.Th("Equipement selection")])] +

        # Body
        [html.Tr([html.Td(sheet_name, rowSpan="2"), html.Td(e_name)]), html.Tr([html.Td(v_name)]) ]
    )