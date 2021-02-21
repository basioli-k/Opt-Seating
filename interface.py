import base64
import datetime
import io

import cProfile
import room_factory
import table_factory
from evaluator import Evaluator
from mutator import Mutator
from plt import visualize_solution, animate
from searcher import Searcher
from seating_plan import SeatingPlan

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
            'width': '100%',
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
    html.Div(id='output-data-upload'),
])

def optimal_seating(df):

    # TODO izvuci informacije iz df-a
    room = room_factory.create(
        'o',
        width='12m',
        inner_width='3m'
    )
    tables = (
        *table_factory.create_multiple(6, 'ltrb', width=150, height=80, ltrb=(0, 2, 0, 2)),
        *table_factory.create_multiple(6, 'ltrb', width=130, height=75, ltrb=(0, 2, 0, 2)),
        *table_factory.create_multiple(4, 'ltrb', width=150, height=150, ltrb=(2, 2, 2, 2)),
    )

    seating_plan = SeatingPlan(tables, tuple())

    mutator = Mutator(
        room,
        table_mutation_probability=.02,
        table_mutation_offset_stdev=100,
        table_mutation_angle_sigma=10,
    )

    evaluator = Evaluator(room)

    def log_fn(i, evaluated_population):
        if i % 100:
            return

        best_fitness, best_instance = evaluated_population[0]
        worst_fitness, worst_instance = evaluated_population[-1]

        print(f"iteration: {i}, "
              f"population size: {len(evaluated_population)}, "
              f"fittness range: {abs(round(best_fitness,2))}-{abs(round(worst_fitness,2))}")
        visualize_solution(room, best_instance, save=f'data/{i:05d}.png')

    searcher = Searcher()

    run = lambda: searcher(
        mutate_fn=mutator,
        evaluate_fn=evaluator,
        log_fn=log_fn,
        initial_population=(seating_plan,),
        max_population_size=1,
        num_iterations=10_000,
    )

    run()
    animate()


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

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback([Output('output-data-upload', 'children')],
             [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
              State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



if __name__ == '__main__':
    app.run_server(debug=True)