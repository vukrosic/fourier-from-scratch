"""Step 6. The verdict. Next to the jump the sum of waves overshoots, and more waves do not make the spike lower."""
import math

from save import save

IRON = 23.0                                       # square millimetres per second
LIFE = 1000.0 ** 2 / (math.pi ** 2 * IRON)        # seconds until cooling leaves 1/e of the 1-hump wave on a 1 m bar


def total(n, x, seconds=0.0):
    """The first n waves of the flat 100-degree bar (humps 1, 3, 5, ...) at place x, after some seconds of cooling."""
    s = 0.0
    for k in range(1, 2 * n, 2):
        s += 400 / (math.pi * k) * math.sin(k * math.pi * x) * (math.exp(-k * k * seconds / LIFE) if seconds else 1)
    return s


def spike(n, seconds=0.0):
    """The highest value near the end of the bar, and where it is (millimetres from the end)."""
    xs = [3.0 / n * (j + 1) / 600 for j in range(600)]
    return max((total(n, x, seconds), 1000 * x) for x in xs)


if __name__ == '__main__':
    rows, zoom = [], {}
    print(' waves  highest value   where        average miss  value at the very end')
    for n in (10, 100, 1000, 10000):
        top, mm = spike(n)
        miss = None
        if n <= 1000:
            pts = 4000
            miss = sum(abs(total(n, (j + 0.5) / pts) - 100) for j in range(pts)) / pts
            zoom[n] = [round(total(n, 3.0 / n * j / 120), 2) for j in range(121)]
        rows.append([n, top, mm, miss, total(n, 0.0)])
        print('%6d  %13.2f  %6.2f mm  %s  %10.1f' % (n, top, mm, ('%13.3f' % miss) if miss is not None else '            -', rows[-1][4]))
    over = (rows[-1][1] - 100) / 200
    print('too hot by %.2f degrees = %.2f%% of the jump the waves see (from -100 to 100)' % (rows[-1][1] - 100, 100 * over))
    cooled = [[s, spike(1000, s)[0], max(total(1000, (j + 0.5) / 2000, s) for j in range(2000))] for s in (0.001, 0.01, 0.1, 1.0)]
    for s, near, anywhere in cooled:
        print('1,000 waves after %5.3f seconds of cooling: highest value on the bar %.2f' % (s, max(near, anywhere)))
    save(6, rows=rows, zoom=zoom, over=over, cooled=[[s, max(a, b)] for s, a, b in cooled], life=LIFE)
