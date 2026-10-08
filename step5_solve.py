"""Step 5. Heat without the waiting: split the bar into waves, shrink each wave by its own share, add them back."""
import math
import time

from save import save
from step1_heat import CELLS, TICK, cool, hot_bar, jagged_bar
from step4_recipe import drawn

SIN = [[math.sin(k * math.pi * i / CELLS) for i in range(CELLS + 1)] for k in range(CELLS)]
SHRINK = [1 - math.sin(k * math.pi / (2 * CELLS)) ** 2 for k in range(CELLS)]     # what one tick leaves of wave k


def split(bar):
    """The recipe of step 4 on the 99 cells: the heights of waves 1 to 99."""
    return [0.0] + [2 * sum(b * s for b, s in zip(bar, SIN[k])) / CELLS for k in range(1, CELLS)]


def later(heights, ticks):
    """The bar after any number of ticks, in one go."""
    left = [h * SHRINK[k] ** ticks for k, h in enumerate(heights)]
    return [sum(left[k] * SIN[k][i] for k in range(1, CELLS)) for i in range(CELLS + 1)]


if __name__ == '__main__':
    h = split(hot_bar())
    table = []
    print('ticks   minutes  centre by waiting  centre by waves  largest difference')
    for ticks in (10, 100, 1000, 4000, 10000):
        slow, fast = cool(hot_bar(), ticks), later(h, ticks)
        diff = max(abs(a - b) for a, b in zip(slow, fast))
        table.append([ticks, ticks * TICK / 60, slow[50], fast[50], diff])
        print('%5d  %8.1f  %17.4f  %15.4f  %18.0e' % tuple(table[-1]))
    t0 = time.time(); cool(hot_bar(), 10000); t1 = time.time(); later(h, 10000); t2 = time.time()
    work = [10000 * (CELLS - 1), (CELLS - 1) * (CELLS - 1)]
    print('work for 3 hours of cooling: %s cell updates by waiting, %s multiplications by waves' % (format(work[0], ','), format(work[1], ',')))
    left = [[k, SHRINK[k] ** 1000] for k in (1, 3, 5, 7, 9)]
    print('what 1,000 ticks (18 minutes) leave of each wave:', ' '.join('%d: %.1f%%' % (k, 100 * v) for k, v in left))

    starts = {'flat': hot_bar(), 'drawn': [0.0] + [drawn(i / CELLS) for i in range(1, CELLS)] + [0.0], 'jagged': jagged_bar()}
    forget = {}
    print('share of the 1-hump wave in the bar, by squared height:')
    for name, bar in starts.items():
        hs = split(bar)
        row = []
        for ticks in (0, 1000, 4000):
            sq = [(x * SHRINK[k] ** ticks) ** 2 for k, x in enumerate(hs)]
            row.append(sq[1] / sum(sq))
        forget[name] = row
        print('  %-7s start %5.1f%%   after 18 min %6.2f%%   after 72 min %8.4f%%' % (name, 100 * row[0], 100 * row[1], 100 * row[2]))
    save(5, table=table, work=work, left=left, forget=forget, heights=h[:12],
         bars={n: [round(v, 2) for v in b] for n, b in starts.items()},
         after={n: [round(v, 3) for v in later(split(b), 1000)] for n, b in starts.items()})
