import operator
from typing import Tuple, Callable, TypeVar, Sequence, Iterable
from seating_plan import SeatingPlan
from visitor import visitor
import random

T = TypeVar('T')


class Crossover:
    def __init__(self, different_tables: int = 3):
        self._different_tables = different_tables
    #make change if probability greater than 1/2*noOfDifferentTypesOfTables

    def __call__(self, population) -> bool:
        i = random.randint(0, len(population) - 1)
        j = random.randint(0, len(population) - 1)
        if i == j :
            return
        first_parent = population[i][1]
        second_parent = population[j][1]
        for k in range(len(first_parent.tables)):
            if 1/(2 * self._different_tables) > random.uniform(0, 1):
                x, y, angle = first_parent.tables[k].offset_x, first_parent.tables[k].offset_y, first_parent.tables[k].angle
                first_parent.tables[k].offset_x, first_parent.tables[k].offset_y = second_parent.tables[k].offset_x, second_parent.tables[k].offset_y
                first_parent.tables[k].angle = second_parent.tables[k].angle
                second_parent.tables[k].offset_x, second_parent.tables[k].offset_y, second_parent.tables[k].angle = x, y, angle
                #ako neki raspored nema stol svejedno cemo napraviti zamjenu na ovom mjestu nema stol
        population.append(first_parent)
        population.append(second_parent)



