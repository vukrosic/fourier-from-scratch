"""Step 1. A bar that cools, by one rule: every cell moves halfway to the average of its two neighbours."""
import random

from save import save

CELLS = 100                      # an iron bar one metre long, cut into 100 cells of 1 cm
IRON = 23.0                      # how fast heat spreads in iron: 23 square millimetres per second
TICK = 0.25 * 10.0 ** 2 / IRON   # with 1 cm cells, "halfway to the average" takes this many seconds: 1.087


def cool(bar, ticks=1):
    """bar: 101 temperatures along the bar. Both ends are pressed on ice and stay at 0 degrees."""
    for _ in range(ticks):
        bar = [0.0] + [(bar[i] + (bar[i - 1] + bar[i + 1]) / 2) / 2 for i in range(1, CELLS)] + [0.0]
    return bar


def hot_bar():
    """The whole bar at 100 degrees, both ends on ice: a sharp jump at each end."""
    return [0.0] + [100.0] * (CELLS - 1) + [0.0]


def jagged_bar():
    """A smooth hill with a fine zigzag on top."""
    random.seed(1807)
    hill = [60 * 4 * (i / CELLS) * (1 - i / CELLS) for i in range(CELLS + 1)]
    return [0.0] + [hill[i] + (15 if i % 2 else -15) + random.uniform(-5, 5) for i in range(1, CELLS)] + [0.0]


def roughness(bar):
    """How much the bar goes up and down from cell to cell, added along its length."""
    return sum(abs(bar[i + 1] - bar[i]) for i in range(CELLS))


def minutes(ticks):
    return ticks * TICK / 60


if __name__ == '__main__':
    print('one tick = %.3f seconds of real iron' % TICK)
    bar, shots, centre, t999, t50 = hot_bar(), {}, [], None, None
    for tick in range(0, 10001):
        if tick in (0, 1, 10, 100, 1000, 4000, 10000):
            shots[tick] = [round(v, 3) for v in bar]
        if tick % 20 == 0:
            centre.append(round(bar[50], 3))
        if t999 is None and bar[50] < 99.9:
            t999 = tick
        if t50 is None and bar[50] < 50:
            t50 = tick
        bar = cool(bar)
    print('ticks  minutes  1 cm from the end  25 cm in  the centre')
    for tick in (0, 10, 100, 1000, 4000, 10000):
        s = shots[tick]
        print('%5d  %7.1f  %17.1f  %8.1f  %10.1f' % (tick, minutes(tick), s[1], s[25], s[50]))
    print('the centre first drops below 99.9 at tick %d (%.1f minutes)' % (t999, minutes(t999)))
    print('the centre reaches 50 degrees at tick %d (%.0f minutes)' % (t50, minutes(t50)))

    j0 = jagged_bar()
    j50 = cool(j0, 50)
    print('a hill with a zigzag: roughness %.0f; after 50 ticks (%.0f seconds): %.0f' % (roughness(j0), 50 * TICK, roughness(j50)))
    print('the top of the hill in that time: %.1f -> %.1f degrees' % (max(j0[40:61]), max(j50[40:61])))
    save(1, tick=TICK, shots=shots, centre=centre, t999=t999, t50=t50, m999=minutes(t999), m50=minutes(t50),
         jag0=[round(v, 2) for v in j0], jag50=[round(v, 2) for v in j50],
         rough=[roughness(j0), roughness(j50)], top=[max(j0[40:61]), max(j50[40:61])])
