# Fourier from scratch

Code for the video **Become Joseph Fourier in 16 Minutes**.
In 1807 Joseph Fourier told the Paris Institute that any line, even one with sharp corners, can be built by adding smooth waves. His judges did not print it for 15 years.
These eight small programs test the claim on a hot iron bar, then on a phone signal: 522 lines of Python 3, standard library only, nothing to install.

```bash
python3 tests.py      # checks every step
./run_all.sh          # runs all eight, about 40 seconds; expected output is in demo-output.txt
```

| File | Idea | What the run shows |
| --- | --- | --- |
| `step1_heat.py` | A bar that cools by one rule | 100 cells of iron, the ends held at 0°. Every cell moves halfway to the average of its two neighbours. The centre stays at 100° for 7.5 minutes and reaches 50° after 69 minutes. The roughness of a zigzag on the bar falls from 3,030 to 118 in 54 seconds. |
| `step2_waves.py` | The shape the bar cannot change | A smooth wave keeps its shape and only shrinks (shape change 4e-14). A wave with 2 humps shrinks 4 times faster, 3 humps 9 times, 10 humps 100 times. A tent, which is not a wave, changes shape by 11.9°. |
| `step3_build.py` | Build a flat bar from waves, by trying | Best heights of waves 1 to 5: 127.3, 0, 42.4, 0, 25.5. The average miss falls from 36.3° to 16.3°. Trying each wave again with the others in place moves nothing. |
| `step4_recipe.py` | The recipe | Multiply the shape by a wave, take the average, double it: that is the wave's height. It returns the same heights (127.32 = 400 / π). With 320 waves the average miss on the flat bar is 0.63°, and 0.13° on a curve drawn by hand. |
| `step5_solve.py` | Heat without the waiting | Split the bar into waves, shrink each wave by its own share, add them back. The answer matches the cell-by-cell run to 4e-12 with 9,801 multiplications in place of 990,000 cell updates. After 72 minutes the 1-hump wave is 99.9999% of every bar we tried. |
| `step6_spike.py` | The verdict | Next to the jump the sum of waves is too hot by 17.9°: 8.95% of the jump. With 10, 100, 1,000 and 10,000 waves the spike stays 117.9° high and only moves closer to the end: 50 mm, 5 mm, 0.5 mm, 0.05 mm. After 0.01 seconds of cooling it is gone. |
| `step7_phone.py` | The same recipe on sound | A phone key is two tones at once. With noise 3 times as strong as one tone, the recipe reads the dialled number 1807 and 300 of 300 random keys. At 10 times it reads 129 of 300, at 40 times 35 of 300. |
| `step8_today.py` | Today | The 1965 fast method finds every wave in 4,096 numbers with 24,576 multiplications in place of 16,777,216 (683 times fewer); the answers differ by 2e-12 and five peaks stand at the five tones of the keys. Position codes of the 2017 transformer (512 numbers, waves 6.28 to 60,611 positions long): two codes 1 apart score 0.97, 10 apart 0.68, 100 apart 0.44, the same near position 10 and near position 1,000. |

`save.py` writes each step's numbers to `runs/`; `values.py` collects them for the video. The two timing lines in step 8 change with the computer.

## What this code is not

- The bar is a model: 100 cells, heat leaves only at the two ends and never to the air.
- Fourier's claim, any line at all, is too wide. Dirichlet and Riemann later wrote down which lines are allowed.
- The spike is the Gibbs phenomenon (Wilbraham 1848, Gibbs 1899): 0.0895 of the jump, at any number of waves.
- The position codes are those of the 2017 transformer; later models use other recipes.

## One experiment we did not run

Our jumps sit at the two ends of the bar. Heat only the left half, so that the jump sits in the middle of the bar. Does the 9% spike appear there too? `step6_spike.py` is the place to start.

## Sources

- Joseph Fourier: Wikipedia "Joseph Fourier"; MacTutor biography (University of St Andrews).
- The spike: Wikipedia "Gibbs phenomenon".
- Phone keys: Wikipedia "DTMF signaling" (Bell System, 1963).
- The fast method: Wikipedia "Fast Fourier transform" (Cooley and Tukey, 1965; Gauss, 1805, unpublished).
- Position codes: Vaswani et al., "Attention Is All You Need", 2017, arXiv 1706.03762, section 3.5.

MIT licence.
