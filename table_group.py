class UsedTablesOfSameKind:
    template: Table
    transformations: []
    available: int

    def num_ppl(self):
        pass

    def chairs_xy(self):
        pass

    def tables_xy(self):
        pass


class UsedTables:
    kinds: UsedTablesOfSameKind[]

    def num_ppl(self):
        pass

    def chairs_xy(self):
        pass

    def matrix_sjedim_za_istim_stolom(self):
        pass

    def tables_xy(self):
        return [xy for k in kinds for xy in k.tables_xy()]