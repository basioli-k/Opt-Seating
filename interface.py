import base64
import datetime
import io

from optimal_seating import optimal_seating

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(
        children='Optimal Seating',
        style={
            'textAlign': 'center',
        }
    ),
    html.Div(
        children='Unesite csv ili Excel file sa ulaznim podacima za program.'
    ),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '99%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.P(id='output-text'),
    html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    optimal_seating(df)
@app.callback([Output('output-text', 'children')],
             [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
              State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:  
        return ["Uspjesno ucitani podaci. Pogledajte novo otvoreni prozor kako biste vidjeli rezultate."]

@app.callback([Output('output-data-upload', 'children')],
             [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
              State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:  
        children = [parse_contents(c, n, d) for c, n, d in 
        zip(list_of_contents, list_of_names, list_of_dates)]
        return [""]



if __name__ == '__main__':
    app.run_server(debug=False)