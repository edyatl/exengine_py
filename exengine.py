#!/usr/bin/env python3
from typing import Tuple, Dict
import sys

tid_counter: int = 0


# buy_orders_cur_len = set()
# sel_orders_cur_len = set()

def counter() -> int:
    global tid_counter
    tid_counter += 1
    return tid_counter


def cancel_order(oid: int,
                 buy_orders: Dict[int, Tuple[int, float]],
                 sel_orders: Dict[int, Tuple[int, float]]) -> None:
    try:
        buy_orders.pop(oid)
        print('X', oid, sep=',')
    except KeyError:
        try:
            sel_orders.pop(oid)
            print('X', oid, sep=',')
        except KeyError as ex:
            pass  # print("ERROR No such key: '%s'" % ex)


def mktrade(buy_orders: Dict[int, Tuple[int, float]],
            sel_orders: Dict[int, Tuple[int, float]]) -> None:

    max_price_buy_order: Tuple[int, Tuple[int, float]] = (0, (0, 0))
    min_price_sel_order: Tuple[int, Tuple[int, float]] = (0, (0, 0))

    if buy_orders.values() and sel_orders.values():
        max_price_buy_order = max(buy_orders.items(), key=(lambda x: (x[1][1], -x[0])))
        min_price_sel_order = min(sel_orders.items(), key=(lambda x: (x[1][1], x[0])))

        # buy_orders_cur_len.add(len(buy_orders))
        # sel_orders_cur_len.add(len(sel_orders))

    if max_price_buy_order[0] > 0 and min_price_sel_order[0] > 0:

        if min_price_sel_order[1][1] <= max_price_buy_order[1][1]:

            cleared_order: Tuple[int, Tuple[int, float]] = min((min_price_sel_order, max_price_buy_order),
                                                               key=(lambda x: (x[1][0], x[0])))
            rest_order: Tuple[int, Tuple[int, float]] = max((min_price_sel_order, max_price_buy_order),
                                                            key=(lambda x: (x[1][0], x[0])))

            if min_price_sel_order[0] < max_price_buy_order[0]:
                side: str = 'S'
                oid1: int = min_price_sel_order[0]
                oid2: int = max_price_buy_order[0]
                tprice: float = min_price_sel_order[1][1]
            else:
                side: str = 'B'
                oid1: int = max_price_buy_order[0]
                oid2: int = min_price_sel_order[0]
                tprice: float = max_price_buy_order[1][1]

            try:
                buy_orders.pop(cleared_order[0])
                sel_orders[rest_order[0]] = (sel_orders.get(rest_order[0], 0)[0] - cleared_order[1][0],
                                             sel_orders.get(rest_order[0], 0)[1])
                if sel_orders[rest_order[0]][0] == 0:
                    sel_orders.pop(rest_order[0])
                print('T,{},{},{},{},{},{}'.format(counter(), side, oid1, oid2, cleared_order[1][0], tprice))
            except KeyError:
                try:
                    sel_orders.pop(cleared_order[0])
                    buy_orders[rest_order[0]] = (buy_orders.get(rest_order[0], 0)[0] - cleared_order[1][0],
                                                 buy_orders.get(rest_order[0], 0)[1])
                    if buy_orders[rest_order[0]][0] == 0:
                        buy_orders.pop(rest_order[0])
                    print('T,{},{},{},{},{},{}'.format(counter(), side, oid1, oid2, cleared_order[1][0], tprice))
                except KeyError as ex:
                    print("ERROR No such key: '%s'" % ex)

            mktrade(buy_orders, sel_orders)


def main() -> None:
    sel_orders: Dict[int, Tuple[int, float]] = {}
    buy_orders: Dict[int, Tuple[int, float]] = {}

    for line in sys.stdin.readlines():
        cmd: tuple = tuple(line.split(','))
        if cmd[0] == 'C':
            cancel_order(int(cmd[1]), buy_orders, sel_orders)
        elif cmd[0] == 'O':
            if cmd[2] == 'B':
                buy_orders[int(cmd[1])] = buy_orders.get(int(cmd[1]), (int(cmd[3]), float(cmd[4])))
                mktrade(buy_orders, sel_orders)
            elif cmd[2] == 'S':
                sel_orders[int(cmd[1])] = sel_orders.get(int(cmd[1]), (int(cmd[3]), float(cmd[4])))
                mktrade(buy_orders, sel_orders)
            else:
                print('ERROR Bad operation')
        else:
            print('ERROR Bad command')
    # print(sel_orders, buy_orders, sep='\n')
    # print(max(buy_orders_cur_len), max(sel_orders_cur_len), sep='\n')


if __name__ == '__main__':
    main()
