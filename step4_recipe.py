"""Step 4. The recipe: multiply the shape by a wave, take the average, double it. That is the wave's height."""
import math

from save import save

POINTS = 2000
XS = [(j + 0.5) / POINTS for j in range(POINTS)]


def amounts(shape, count):
    """How much of each wave is in the shape: wave 1, wave 2, ... wave count."""
    return [2 * sum(s * math.sin(k * math.pi * x) for s, x in zip(shape, XS)) / POINTS for k in range(1, count + 1)]


def rebuild(am, xs=XS):
    return [sum(a * math.sin((k + 1) * math.pi * x) for k, a in enumerate(am)) for x in xs]


def average_miss(curve, target):
    return sum(abs(c - t) for c, t in zip(curve, target)) / len(curve)


def drawn(x):
    """A made-up temperature along the bar: a ramp, a flat shelf, a cliff, a round hill and a slope down."""
    if x < 0.15:
        return 400 * x
    if x < 0.35:
        return 60.0
    if x < 0.5:
        return 20.0
    if x < 0.8:
        return 20 + 70 * math.sin(math.pi * (x - 0.5) / 0.3)
    return 100 * (1 - x)


if __name__ == '__main__':
    flat = [100.0] * POINTS
    am = amounts(flat, 320)
    print('the flat bar, waves 1 to 7:', ' '.join('%.2f' % a for a in am[:7]))
    print('height times number of humps:', ' '.join('%.2f' % (a * (k + 1)) for k, a in enumerate(am[:9]) if k % 2 == 0))
    print('400 / pi = %.2f' % (400 / math.pi))
    shape = [drawn(x) for x in XS]
    dm = amounts(shape, 320)
    print('a drawn curve, waves 1 to 7:', ' '.join('%.2f' % a for a in dm[:7]))
    view = [(j + 0.5) / 240 for j in range(240)]
    target = [drawn(x) for x in view]
    table, curves, fcurves = [], {}, {}
    print('waves  average miss, flat bar  average miss, drawn curve')
    for n in (1, 5, 20, 80, 320):
        mf = average_miss(rebuild(am[:n]), flat)
        md = average_miss(rebuild(dm[:n]), shape)
        table.append([n, mf, md])
        curves[n] = [round(v, 2) for v in rebuild(dm[:n], view)]
        fcurves[n] = [round(v, 2) for v in rebuild(am[:n], view)]
        print('%5d  %22.2f  %25.2f' % (n, mf, md))
    save(4, flat=am[:40], drawn=dm[:40], table=table, target=[round(v, 2) for v in target], curves=curves, fcurves=fcurves,
         quarter=400 / math.pi)
