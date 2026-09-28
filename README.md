# Ballistics Calculator (metric)

A small external-ballistics calculator written in plain Python. Give it a projectile, a launch speed and the conditions, and it prints a range table: speed, Mach, energy, time of flight, drop, wind drift and scope corrections in MOA and MIL.

Everything is metric. No third-party packages are needed (matplotlib is optional, only for `--plot`).

## Files

| File | What it is |
|------|------------|
| `ballistics.py` | The calculator |
| `Ballistics_Calculator_Documentation.pdf` | Full documentation: physics, code walkthrough, worked example, verification |
| `README.md` | This file |

## Quick start

```
python ballistics.py --selftest
python ballistics.py
```

Running with no options asks you questions and prints the equivalent one-line command at the end.

One-line example:

```
python ballistics.py --mv 823 --bc 0.462 --model G1 --weight 10.9 --diameter 7.82 \
    --sight-height 38 --zero 100 --max-range 1000 --step 100 \
    --wind-speed 5 --wind-dir 90 --lat 40 --azimuth 0 --length 30.9 --twist 280
```

A thrown ball instead of a bullet:

```
python ballistics.py --preset baseball --mv 40 --angle 30 --max-range 100 --step 10
```

## Units

| Quantity | Unit |
|----------|------|
| Speed, wind | m/s |
| Mass | g |
| Diameter, length, twist, sight height | mm |
| Range, zero, table step | m |
| Temperature | C |
| Pressure | hPa (station pressure) |
| Drop and drift in the table | cm |
| Energy | J |

The ballistic coefficient is the one exception: it stays in lb/in², because that is how manufacturers publish it.

## Options

| Option | Meaning |
|--------|---------|
| `--mv` | Launch speed |
| `--model`, `--bc` | G1, G7 or CUSTOM curve and BC |
| `--cd`, `--drag-csv` | Plain Cd, or a CSV of `mach,cd` rows |
| `--weight`, `--diameter` | Projectile mass and diameter |
| `--length`, `--twist`, `--left-twist` | For spin drift |
| `--sight-height`, `--zero` | Sight above barrel, and zero distance |
| `--angle` | Set the barrel angle directly (skips zeroing) |
| `--max-range`, `--step` | Table extent and spacing |
| `--temp`, `--pressure`, `--humidity`, `--altitude` | Air conditions (default: standard day) |
| `--wind-speed`, `--wind-dir` | Wind, and the direction it comes from (0 ahead, 90 right, 180 behind, 270 left) |
| `--incline` | Shot angle, positive uphill |
| `--lat`, `--azimuth` | Turn on Coriolis |
| `--csv`, `--plot` | Save the table or a trajectory PNG |
| `--selftest` | Run the built-in checks |

## Use it as a module

```python
from ballistics import *

bullet = from_bc('G7', 0.243, 0.0113, 0.00782, length=0.0315, twist=0.254)
env = Env(Air.standard(1500), wind=4.0, wind_from=90, lat=45, azimuth=270)
sol = compute(bullet, env, 800.0, sight=0.04, zero=100.0, max_range=1200, step=100)

for r in sol.rows:
    print(r.range_m, r.speed, r.drop, r.wind_drift)
```

Inside the module everything is SI (metres, kilograms, seconds).

## Reading the table

- **Drop**: height compared with the line of sight. Minus is below.
- **Up**: how far to dial up (MOA or MIL).
- **Drift**: sideways offset from wind, Coriolis and spin drift. Plus is right.
- **Wind**: windage correction. Plus is dial right, minus is dial left.

## How it works

A 3-DOF point-mass model integrated with fourth-order Runge-Kutta. Drag comes from G1/G7 reference curves (or your own), scaled by the ballistic coefficient. The sights are zeroed by bisection on the barrel angle. The PDF covers all of this in detail.

## Limits

- Point mass only: no yaw, Magnus force or lift. Spin drift is an empirical add-on.
- Air density and wind are constant along the flight.
- Ball presets use a constant Cd and are only rough.
- Verified against exact physics and self-consistency tests, not against radar data. For anything that matters, check against measured impacts and adjust velocity or BC to match.

A calculator does not replace safe practice. Know your target and what is beyond it, and follow local law and range rules.
