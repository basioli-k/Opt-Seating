import table_factory
import room_factory
from svg import Svg


if __name__ == '__main__':
    room = room_factory.create(
        'o',
        width='10m',
    )
    table_warehouse = (
        table_factory.create_multiple(10, '2222', width=140, height=140),
        table_factory.create_multiple(20, '2020', width=120, height=60),
    )



    #
    # plt = MatplotlibDrawer()
    # room.visit(plt)
    # for table in tables:
    #     table.visit(plt)
    # plt.show()

    svg = Svg()
    room.visit(svg)
    for table in tables:
        table.visit(svg)
    svg.save()
