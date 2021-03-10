import base64
import datetime
import io
import shapely

import cProfile
import room_factory
import table_factory
from evaluator import Evaluator
from mutator import Mutator
from plt import visualize_solution, animate
from searcher import Searcher
from seating_plan import SeatingPlan
import numpy as np

import pandas as pd
def read_room(df):
    room_width = -1
    room_height = -1
    if df.loc[0][0] == 'o':
        room = room_factory.create(
            df.loc[0][0],
            width=df.loc[0][1],
            inner_width=df.loc[0][2]
        )
        room_width = int(df.loc[0][1][:-1])
        room_height = int(df.loc[0][1][:-1])
    elif df.loc[0][0] == 'circle':
        room = room_factory.create(
            df.loc[0][0],
            width=df.loc[0][1],
        )
        room_width = int(df.loc[0][1][:-1])
        room_height = int(df.loc[0][1][:-1])
    elif df.loc[0][0] == 'delta' or df.loc[0][0] == 'rect':
        room = room_factory.create(
            df.loc[0][0],
            width=df.loc[0][1],
            height=df.loc[0][2]
        )
        room_width = int(df.loc[0][1][:-1])
        room_height = int(df.loc[0][2][:-1])
    elif df.loc[0][0] == 'L':
        room = room_factory.create(
            df.loc[0][0],
            width=df.loc[0][1],
            height=df.loc[0][2],
            smaller_width=df.loc[0][3],
            smaller_height=df.loc[0][4]
        )
        room_width = int(df.loc[0][1][:-1])
        room_height = int(df.loc[0][2][:-1])
    return room, room_width, room_height


def optimal_seating(df):

    room, room_width, room_height = read_room(df)

    tables = ()
    for index, row in df.iterrows():
        if index == 0: 
            continue
        tables = tables + (*table_factory.create_multiple(int(row[0]), row[1], room_dims=(room_width, room_height),
                                                          width=int(row[2]), height=int(row[3]),
                                                          ltrb=(int(row[4]), int(row[5]), int(row[6]), int(row[7]))),)

    seating_plan = SeatingPlan(
        np.array(tables),
        np.repeat(True, len(tables)),
        3000
    )
    mutator = Mutator(
        room,
        table_mutation_probability=.1,
        table_mutation_offset_stdev=100,
        table_mutation_angle_sigma=0,
    )

    evaluator = Evaluator(room)

    def log_fn(i, evaluated_population):
        if i % 100:
            return

        best_fitness, best_instance = evaluated_population[0]
        worst_fitness, worst_instance = evaluated_population[-1]
        print("no of used tables: ", best_instance.used_tables())
        print(f"iteration: {i}, "
              f"population size: {len(evaluated_population)}, "
              f"fittness range: {abs(round(best_fitness, 2))}-{abs(round(worst_fitness, 2))}")
        visualize_solution(room, best_instance, save=f'data/{i:05d}.png')

    searcher = Searcher()

    run = lambda: searcher(
        mutate_fn=mutator,
        evaluate_fn=evaluator,
        log_fn=log_fn,
        initial_population=(seating_plan,),
        max_population_size=10,
        num_iterations=10_000,
    )

    run()
    animate()