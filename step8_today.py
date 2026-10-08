"""Step 8. Today: the fast way to find every wave at once, and the waves a 2017 language model uses as a ruler."""
import cmath
import math
import random
import time

from save import save
from step7_phone import RATE, press

N = 4096


def slow_waves(sound):
    """Every wave by the recipe, one at a time: N waves times N measurements."""
    n = len(sound)
    turn = [cmath.exp(-2j * math.pi * i / n) for i in range(n)]
    return [sum(sound[i] * turn[(i * k) % n] for i in range(n)) for k in range(n)]


def fast_waves(sound):
    """The fast way: split the measurements into the even ones and the odd ones, solve each half, join the answers."""
    n = len(sound)
    if n == 1:
        return [complex(sound[0])]
    even, odd = fast_waves(sound[0::2]), fast_waves(sound[1::2])
    out = [0j] * n
    for k in range(n // 2):
        t = cmath.exp(-2j * math.pi * k / n) * odd[k]
        out[k], out[k + n // 2] = even[k] + t, even[k] - t
    return out


def position_code(pos, size=512):
    """Vaswani et al. 2017: a position in the sentence, written as the readings of 256 waves of different length."""
    code = []
    for i in range(0, size, 2):
        angle = pos / 10000 ** (i / size)
        code += [math.sin(angle), math.cos(angle)]
    return code


def alike(a, b):
    return sum(x * y for x, y in zip(a, b)) / (len(a) / 2)


if __name__ == '__main__':
    random.seed(1965)
    sound = [v for key in '18071' for v in press(key, noise=1.0)] + [0.0] * 96
    assert len(sound) == N
    t0 = time.time(); slow = slow_waves(sound); t1 = time.time(); fast = fast_waves(sound); t2 = time.time()
    diff = max(abs(a - b) for a, b in zip(slow, fast))
    mults = [N * N, N // 2 * int(math.log2(N))]
    print('%d measurements of a phone sound with noise as loud as one tone (0.51 seconds)' % N)
    print('one wave at a time: %s multiplications, %.1f seconds' % (format(mults[0], ','), t1 - t0))
    print('the fast way:       %s multiplications, %.3f seconds' % (format(mults[1], ','), t2 - t1))
    print('%.0f times fewer multiplications, %.0f times less time; largest difference between the answers %.0e' % (mults[0] / mults[1], (t1 - t0) / (t2 - t1), diff))
    size = [abs(v) * 2 / N for v in fast[:N // 2]]
    usual = sorted(size)[len(size) // 2]                       # the middle height: what noise alone gives
    peaks = []
    for k in sorted(range(1, N // 2 - 1), key=lambda k: -size[k]):
        if size[k] < 4 * usual: break
        if all(abs(k - p) * RATE / N > 40 for p in peaks): peaks.append(k)      # one peak per 40 Hz
    peaks.sort()
    print('peaks more than 4 times the usual height: %d, at' % len(peaks), ' '.join('%.0f' % (k * RATE / N) for k in peaks), 'Hz')
    print('the keys 1, 8, 0, 7, 1 use the tones 697 852 941 1209 1336 Hz')

    print('position codes, 512 numbers each; the longest wave is %s positions long, the shortest %.2f' % (format(round(2 * math.pi * 10000 ** (510 / 512)), ','), 2 * math.pi))
    codes = {p: position_code(p) for p in (10, 11, 12, 15, 20, 60, 110, 1000, 1001, 1002, 1005, 1010, 1050, 1100)}
    rows = []
    print('distance  alike near position 10  alike near position 1,000')
    for d in (1, 2, 5, 10, 50, 100):
        a, b = alike(codes[10], codes[10 + d]), alike(codes[1000], codes[1000 + d])
        rows.append([d, a, b])
        print('%8d  %22.4f  %25.4f' % (d, a, b))
    same = max(abs(a - b) for d, a, b in rows)
    print('largest difference between the two columns: %.0e' % same)
    grid = [[round(v, 3) for v in position_code(p)[:48]] for p in range(40)]
    save(8, n=N, mults=mults, seconds=[t1 - t0, t2 - t1], diff=diff, peaks=[k * RATE / N for k in peaks], usual=usual,
         spectrum=[round(max(size[k:k + 4]), 3) for k in range(0, N // 2, 4)], rows=rows, same=same, grid=grid,
         longest=2 * math.pi * 10000 ** (510 / 512))
