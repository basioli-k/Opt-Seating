import cProfile
import room_factory
import table_factory
from evaluator import Evaluator
from mutator import Mutator
from plt import visualize_solution, animate
from searcher import Searcher
from seating_plan import SeatingPlan

if __name__ == '__main__':
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

    seating_plan = SeatingPlan(tables, tuple(True for i in range(len(tables))))
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
        print("no of used tables: ",best_instance.used_tables())
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
        max_population_size=5,
        num_iterations=10_000,
    )

    run()
    animate()

    # cProfile.run('run()', sort=SortKey.CUMULATIVE)
# 5.477
