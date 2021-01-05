import table_factory
import room_factory
from plt import MatplotlibDrawer
# from svg import Svg
from table_group import SelectionFromTableGroup, SelectionGrouped

if __name__ == '__main__':
    room = room_factory.create(
        'o',
        width='10m',
    )
    table_warehouse = (
        table_factory.create_multiple(10, '2222', width=140, height=140),
        table_factory.create_multiple(20, '2020', width=120, height=60),
    )

    group1 = SelectionFromTableGroup(template=table_factory.create('2222', width=140, height=140), available=10)
    group1.add(rotation=90)
    group1.add(translation=(100, 170))
    group1.add(translation=(-150, -70), rotation=20)

    group2 = SelectionFromTableGroup(template=table_factory.create('2020', width=120, height=60), available=5)
    group2.add(translation=(300, 270))
    group2.add(translation=(-370, -100), rotation=20)

    print(f"group 1 has {group1.num_ppl()} people")
    print(f"group 2 has {group2.num_ppl()} people")

    selection = SelectionGrouped([group1, group2])
    assert group1.num_ppl() + group2.num_ppl() == selection.num_ppl()

    for i in selection.mask_same_table():
        for j in i:
            if j:
                print('+', end=" ")
            else:
                print('-', end=" ")
        print('\n')
    # x, y = selection.chairs_xy()
    # tables = selection.tables_xy()

    # plt = MatplotlibDrawer()
    # room.visit(plt)
    # group1.visit(plt)
    # group2.visit(plt)
    #
    # # plt.scatter(x, y, color="red")
    # # for table in tables:
    # #     plt.plot(*table, stroke='red', fill='red')
    # plt.show()

    # svg = Svg()
    # room.visit(svg)
    # for table in table_warehouse:
    #    table.visit(svg)
    # svg.save()
