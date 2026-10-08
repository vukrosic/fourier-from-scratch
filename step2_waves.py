"""Step 2. One shape the bar cannot change: a smooth wave. It only shrinks, and finer waves shrink faster."""
import math

from save import save
from step1_heat import CELLS, TICK, cool


def wave(humps, height=100.0):
    """A sine wave along the bar with this many humps (up or down), zero at both ends."""
    return [height * math.sin(humps * math.pi * i / CELLS) for i in range(CELLS + 1)]


def tent(height=100.0):
    """Not a wave: two straight slopes meeting in a corner in the middle."""
    return [height * (1 - abs(2 * i / CELLS - 1)) for i in range(CELLS + 1)]


def shape_change(before, after):
    """Blow the cooled bar back up to its old height. How far is it from its old shape, at worst, in degrees?"""
    scale = max(before) / max(after)
    return max(abs(a * scale - b) for a, b in zip(after, before))


if __name__ == '__main__':
    rows, base = [], None
    print('humps  left after 200 ticks  shape change  half-life        speed')
    for humps in (1, 2, 3, 5, 10):
        w = wave(humps)
        c = cool(w, 200)
        left = max(c) / max(w)
        per_tick = left ** (1 / 200)
        half = math.log(0.5) / math.log(per_tick)                 # ticks until half the height is left
        rate = -math.log(per_tick)
        base = base or rate
        rows.append([humps, left, shape_change(w, c), half, half * TICK, rate / base])
        print('%5d  %19.1f%%  %12.0e  %7.0f ticks = %5.1f min  %5.1fx' % (humps, 100 * left, rows[-1][2], half, half * TICK / 60, rate / base))
    t = tent()
    c = cool(t, 200)
    print('a tent (not a wave) after 200 ticks: %.1f%% left at the top, shape change %.1f degrees' % (100 * max(c) / max(t), shape_change(t, c)))
    save(2, rows=rows, tent=[max(c) / max(t), shape_change(t, c)],
         tent0=[round(v, 2) for v in t], tent200=[round(v, 2) for v in c])
