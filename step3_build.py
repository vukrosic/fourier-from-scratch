"""Step 3. Build the flat hot bar, with its sharp ends, out of smooth waves. Find each wave's height by trying."""
import math

from save import save

POINTS = 400
XS = [(j + 0.5) / POINTS for j in range(POINTS)]        # places along the bar, as a share of its length
FLAT = [100.0] * POINTS                                  # the target: 100 degrees everywhere


def waves(k):
    return [math.sin(k * math.pi * x) for x in XS]


SIN = {k: waves(k) for k in range(1, 6)}


def total(heights):
    """Add the waves: heights[0] of the 1-hump wave, heights[1] of the 2-hump wave, ..."""
    return [sum(h * SIN[k + 1][j] for k, h in enumerate(heights) if h) for j in range(POINTS)]


def squared_miss(curve, target=FLAT):
    return sum((c - t) ** 2 for c, t in zip(curve, target)) / POINTS


def average_miss(curve, target=FLAT):
    return sum(abs(c - t) for c, t in zip(curve, target)) / POINTS


def best_height(heights, k):
    """Try every height from -200 to 200 in steps of 0.1 for wave k; keep the one with the smallest squared miss."""
    rest = total([h if i != k - 1 else 0 for i, h in enumerate(heights)])
    left = [t - r for t, r in zip(FLAT, rest)]
    return min((squared_miss([h / 10 * s for s in SIN[k]], left), h / 10) for h in range(-2000, 2001))[1]


if __name__ == '__main__':
    one = total([100, 0, 0, 0, 0])
    print('one wave of height 100: average miss %.1f degrees' % average_miss(one))
    heights, steps = [0.0] * 5, []
    for k in range(1, 6):
        heights[k - 1] = best_height(heights, k)
        curve = total(heights)
        steps.append([k, heights[k - 1], average_miss(curve), squared_miss(curve)])
        print('best height of the %d-hump wave: %6.1f   average miss now %5.2f degrees' % (k, heights[k - 1], steps[-1][2]))
    again = [best_height(heights, k) for k in range(1, 6)]
    print('try every wave again, with the others in place:', again)
    print('nothing moved:', again == heights)
    bowl = [[h, squared_miss([h * s for s in SIN[1]])] for h in range(0, 201, 5)]
    save(3, one=average_miss(one), heights=heights, steps=steps, again=again, bowl=bowl,
         curves=[[round(v, 2) for v in total(heights[:n] + [0] * (5 - n))] for n in (1, 3, 5)])
