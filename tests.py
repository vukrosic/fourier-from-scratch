"""Checks. run_all.sh runs them last, on the numbers the eight steps saved in runs/."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
r = {i: json.load(open(os.path.join(HERE, 'runs', 'step%d.json' % i))) for i in range(1, 9)}

# 1. heat only flows downhill: the ends stay at 0, the centre never warms up, the zigzags go first
assert all(shot[0] == 0 and shot[-1] == 0 for shot in r[1]['shots'].values())
assert all(a >= b for a, b in zip(r[1]['centre'], r[1]['centre'][1:]))
assert r[1]['rough'][1] < r[1]['rough'][0] / 20 and r[1]['top'][1] > r[1]['top'][0] / 2

# 2. a wave keeps its shape; a wave with k humps dies k x k times faster; a tent does not keep its shape
for humps, left, change, half, minutes, times in r[2]['rows']:
    assert change < 1e-9 and abs(times - humps ** 2) < 0.01 * humps ** 2
assert r[2]['tent'][1] > 5

# 3. each new wave makes the miss smaller or leaves it; a second pass changes nothing
misses = [row[2] for row in r[3]['steps']]
assert all(a >= b for a, b in zip(misses, misses[1:])) and misses[-1] < r[3]['one']
assert r[3]['again'] == r[3]['heights']

# 4. the recipe gives the same heights as the search; more waves, smaller miss; the flat bar follows 400 / pi / k
assert all(abs(a - b) < 0.06 for a, b in zip(r[4]['flat'][:5], r[3]['heights']))
assert all(a[1] > b[1] and a[2] > b[2] for a, b in zip(r[4]['table'], r[4]['table'][1:]))
assert abs(r[4]['quarter'] - 400 / math.pi) < 1e-6
assert all(abs(r[4]['flat'][k - 1] * k - 400 / math.pi) < 0.1 for k in (1, 3, 5, 7, 9))

# 5. waves and waiting give the same bar; the waves need about 100 times less work
assert all(row[4] < 1e-9 for row in r[5]['table'])
assert r[5]['work'][0] > 100 * r[5]['work'][1]
assert all(share[0] < share[1] <= share[2] <= 1.0000001 for share in r[5]['forget'].values())

# 6. the overshoot does not shrink, it moves to the jump; it is the 9% of the Gibbs phenomenon
tops = [row[1] for row in r[6]['rows']]
assert max(tops) - min(tops) < 0.1 and all(a[2] > b[2] for a, b in zip(r[6]['rows'], r[6]['rows'][1:]))
assert abs(r[6]['over'] - 0.0894898722) < 1e-6
assert r[6]['cooled'][1][1] < 100.01

# 7. the number that was dialled is the number that was heard
assert r[7]['heard'] == r[7]['dial'] == '1807'
assert r[7]['rates'][0][1] == 300 and r[7]['rates'][-1][1] < 100

# 8. the fast way gives the same waves; it finds the five tones; the position codes only depend on the distance
assert r[8]['diff'] < 1e-9 and r[8]['mults'][0] > 600 * r[8]['mults'][1]
assert len(r[8]['peaks']) == 5 and all(abs(p - t) < 6 for p, t in zip(r[8]['peaks'], (697, 852, 941, 1209, 1336)))
assert r[8]['same'] < 1e-12 and all(a[1] > b[1] for a, b in zip(r[8]['rows'], r[8]['rows'][1:]))

print('all checks passed')
