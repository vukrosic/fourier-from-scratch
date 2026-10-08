"""Step 7. The same recipe on sound: which key was pressed on a phone, read from the noisy signal alone."""
import math
import random

from save import save

RATE = 8000                                   # a phone line measures the sound 8,000 times a second
ROWS = [697, 770, 852, 941]                   # every key sounds one row tone and one column tone together
COLS = [1209, 1336, 1477]
KEYS = ['123', '456', '789', '*0#']
SLOT = 800                                    # one key = 0.1 second = 800 measurements
SIN = {hz: [math.sin(2 * math.pi * hz * i / RATE) for i in range(SLOT)] for hz in ROWS + COLS}
COS = {hz: [math.cos(2 * math.pi * hz * i / RATE) for i in range(SLOT)] for hz in ROWS + COLS}


def press(key, noise=0.0):
    """0.1 second of the two tones of this key, plus random noise."""
    r = next(i for i, row in enumerate(KEYS) if key in row)
    c = KEYS[r].index(key)
    return [SIN[ROWS[r]][i] + SIN[COLS[c]][i] + random.gauss(0, noise) for i in range(SLOT)]


def strength(sound, hz):
    """The recipe: multiply by the wave, average, double. Done twice (the wave and the wave shifted a quarter step),
    because we do not know at which moment the tone started."""
    a = 2 * sum(s * w for s, w in zip(sound, SIN[hz])) / SLOT
    b = 2 * sum(s * w for s, w in zip(sound, COS[hz])) / SLOT
    return math.sqrt(a * a + b * b)


def read_key(sound):
    row = max(range(4), key=lambda r: strength(sound, ROWS[r]))
    col = max(range(3), key=lambda c: strength(sound, COLS[c]))
    return KEYS[row][col]


if __name__ == '__main__':
    random.seed(1822)
    dial = '1807'
    sounds = [press(k, noise=3.0) for k in dial]
    print('dialled %s; noise 3 times as strong as one tone; 800 numbers per key, for example:' % dial)
    print('  ' + ' '.join('%+.1f' % v for v in sounds[0][:10]))
    table = []
    print('key  ' + '  '.join('%4d Hz' % hz for hz in ROWS + COLS) + '   read as')
    for snd in sounds:
        st = [strength(snd, hz) for hz in ROWS + COLS]
        table.append([round(v, 3) for v in st])
        print(' ?   ' + '  '.join('%7.2f' % v for v in st) + '   ' + read_key(snd))
    heard = ''.join(read_key(s) for s in sounds)
    print('heard:', heard)
    rates = []
    for noise in (1, 3, 10, 20, 40):
        right = 0
        for _ in range(300):
            key = random.choice('1234567890*#')
            right += read_key(press(key, noise)) == key
        rates.append([noise, right])
        print('noise %2d times one tone: %3d of 300 keys read right' % (noise, right))
    clean = press('1')
    save(7, dial=dial, heard=heard, table=table, rates=rates,
         clean=[round(v, 3) for v in clean[:240]], noisy=[round(v, 2) for v in sounds[0][:240]])
