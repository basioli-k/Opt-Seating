import operator
import random
from dataclasses import dataclass
from typing import Callable, Tuple, TypeVar, Generic, Sequence, Iterable
import numpy as np
from crossover import Crossover

T = TypeVar('T')


def same_dimension_tables(table1, table2):
    if table1.template.height == table2.template.height and table1.template.width == table2.template.width:
        return True
    elif table1.template.height == table2.template.width and table1.template.width == table2.template.height:
        return True
    else:
        return False


def squared_offset_distance(table1, table2):
    return (table1.offset_x - table2.offset_y) ** 2 + (table1.offset_y - table2.offset_y) ** 2


def population_metric(room_layout1, room_layout2, biggest_distance):  # ideja je sto je ovo veće to su populacije razlicitije
    compared_to = [False, ] * len(room_layout2.tables)  # mozemo uzeti neku brojku koja ce odredivati kad je razlika dovoljno velika
    metric = 0  # npr dijagonala ili promjer * n/5 gdje je n broj stolova ili tako nesto
    for i in range(0, len(room_layout1.tables)):
        shortest_distance = biggest_distance  # set this to some number, example diagonal of the room, diameter,...
        shortest_distance_index = -1
        # todo if table isn't used (false in used_table_mask) dont go in the other loop
        for j in range(0, len(room_layout2.tables)):
            if same_dimension_tables(room_layout1.tables[i], room_layout2.tables[j]) and not compared_to[j]:
                dist = squared_offset_distance(room_layout1.tables[i], room_layout2.tables[j])
                if dist < shortest_distance:
                    shortest_distance = dist
                    if shortest_distance_index != -1:
                        compared_to[shortest_distance_index] = False
                    shortest_distance_index = j
                    compared_to[shortest_distance_index] = True
        metric += shortest_distance

    return metric > biggest_distance


def population_metric_2(room_layout1, room_layout2, biggest_distance):
    metric = 0
    layout1 = np.array([(table.offset_x, table.offset_y) for table in room_layout1.tables])
    layout2 = np.array([(table.offset_x, table.offset_y) for table in room_layout2.tables])
    #used_table = np.array(room_layout1.used_table_mask && room_layout2.used_tables_mask)
    metric = np.sum(np.linalg.norm(layout1-layout2)**2)
    #todo obavezno promijeniti kada dodemo used_tables_mask
    return metric > biggest_distance


@dataclass(frozen=True)
class Searcher(Generic[T]):

    """
        searches for the solution
    """

    def __call__(
            self,
            mutate_fn: Callable[[T], Iterable[T]],
            evaluate_fn: Callable[[T], float],
            crossover: Crossover,
            log_fn: Callable[..., None],
            initial_population: Tuple[T],
            max_population_size: int,
            num_iterations: int,
            biggest_distance: float,
            children_per_iteration: int = 1,
    ):
        """
        :param mutate_fn: function performing the mutations
        :param evaluate_fn: function evaluating the current solution
        :param log_fn: logging function
        """

        def _evaluate_population(population: Sequence[T]):
            return list(zip(
                map(evaluate_fn, population),
                population,
            ))

        evaluated_population = _evaluate_population(initial_population)
        for i in range(num_iterations):
            evaluated_population.sort(key=operator.itemgetter(0), reverse=True)
            size = max_population_size if abs(evaluated_population[-1][0]) - abs(evaluated_population[0][0]) >= 1 else 1
            evaluated_population = evaluated_population[:size]
            #crossover.cross_plans(evaluated_population, evaluate_fn)
            #evaluated_population.sort(key=operator.itemgetter(0), reverse=True)
            log_fn(i, evaluated_population)

            temp = []
            for x in map(
                    operator.itemgetter(1),
                    random.choices(
                        evaluated_population,
                        k=children_per_iteration,
                    )
            ):
                for c in mutate_fn(x):
                    if population_metric(c, x, biggest_distance):
                        temp.append(c)

            children = _evaluate_population(tuple(temp))
            evaluated_population.extend(
                children
            )
