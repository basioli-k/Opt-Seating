import operator
import random
from dataclasses import dataclass
from typing import Callable, Tuple, TypeVar, Generic, Sequence, Iterable

T = TypeVar('T')


@dataclass(frozen=True)
class Searcher(Generic[T]):
    """
        searches for the solution
    """
    def __call__(
            self,
            mutate_fn: Callable[[T], Iterable[T]],
            evaluate_fn: Callable[[T], float],
            log_fn: Callable[..., None],
            initial_population: Tuple[T],
            max_population_size: int,
            num_iterations: int,
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
            evaluated_population = evaluated_population[:max_population_size]
            log_fn(i, evaluated_population)

            children = _evaluate_population(
                tuple(
                    c
                    for x in
                    map(
                        operator.itemgetter(1),
                        random.choices(
                            evaluated_population,
                            k=children_per_iteration,
                        )
                    )
                    for c in mutate_fn(x)
                )
            )
            evaluated_population.extend(
                children
            )
