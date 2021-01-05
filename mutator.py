import random
from typing import Union

from table_group import SeatingPlan, SelectionFromTableGroup

def mutator():
    pass


class Mutator:
    def __call__(self,
                 obj: Union[
                     SelectionFromTableGroup,
                     SeatingPlan
                 ],
                 *,
                 p_translate: float = 0.1,
                 p_rotate: float = 0.1,
                 radius: float = 30.
                 ):

        if isinstance(obj, SeatingPlan):
            for group in obj._groups:  # todo eskopelja FIX!!!!
                group.visit(self)
            return

        if isinstance(obj, SelectionFromTableGroup):
            new_translations = []
            new_rotations = []

            for t, r in zip(obj.translations, obj.rotations):
                new_translations.append(
                    t if random.random() > p_translate
                    else (t[0] + random.uniform(0, radius), t[1] + random.uniform(0, radius))
                )

                new_rotations.append(
                    t if random.random() > p_rotate
                    else random.randint(0, 360)
                )

            obj.translations = new_translations
            obj.rotations = new_rotations
