import operator
from typing import Tuple, Callable, TypeVar, Sequence
from seating_plan import SeatingPlan
from visitor import visitor
import random

T = TypeVar('T')


class Crossover:
    def __init__(self, different_tables: int = 3):
        self._different_tables = different_tables
    #make change if probability greater than 1/2*noOfDifferentTypesOfTables

    def cross_plans(self, population, evaluator_fn: Callable[[T], float]):
        i = random.randint(0, len(population) - 1)
        j = random.randint(0, len(population) - 1)
        if i == j :
            return
        if i > j:
            i, j = tuple((j, i))
        first_parent = population[i][1] #first parent is always "better"
        second_parent = population[j][1]
        for k in range(len(first_parent.tables)):
            if 1/(2 * self._different_tables) > random.uniform(0, 1):
                x, y, angle = first_parent.tables[k].offset_x, first_parent.tables[k].offset_y, first_parent.tables[k].angle
                first_parent.tables[k].offset_x, first_parent.tables[k].offset_y = second_parent.tables[k].offset_x, second_parent.tables[k].offset_y
                first_parent.tables[k].angle = second_parent.tables[k].angle
                second_parent.tables[k].offset_x, second_parent.tables[k].offset_y, second_parent.tables[k].angle = x, y, angle
                #ako neki raspored nema stol svejedno cemo napraviti zamjenu na ovom mjestu nema stol
        fit1 = evaluator_fn(first_parent)
        fit2 = evaluator_fn(second_parent)
        temp_population = [population[i], population[j], (fit1, first_parent), (fit2, second_parent)]
        temp_population.sort(key=operator.itemgetter(0), reverse=True)
        #print("tmp: ", [x[0] for x in temp_population])
        population[i] = temp_population[0]
        population[j] = temp_population[1]
        #print([x[0] for x in population])


