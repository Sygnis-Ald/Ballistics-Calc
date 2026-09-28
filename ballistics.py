#!/usr/bin/env python3
import argparse
import bisect
import csv
import math
import sys
from dataclasses import dataclass

G0 = 9.80665
R_AIR = 287.058
R_VAP = 461.495
OMEGA = 7.2921159e-5
P0 = 101325.0
T0 = 288.15
LAPSE = 0.0065
GRAIN = 6.479891e-5
INCH = 0.0254
FOOT = 0.3048
INHG = 3386.389
LB_IN2 = 703.06958
MOA = 180.0 * 60.0 / math.pi
MIL = 1000.0

G1 = [
    (0.00, 0.2629), (0.05, 0.2558), (0.10, 0.2487), (0.15, 0.2413), (0.20, 0.2344),
    (0.25, 0.2278), (0.30, 0.2214), (0.35, 0.2155), (0.40, 0.2104), (0.45, 0.2061),
    (0.50, 0.2032), (0.55, 0.2020), (0.60, 0.2034), (0.70, 0.2165), (0.725, 0.2230),
    (0.75, 0.2313), (0.775, 0.2417), (0.80, 0.2546), (0.825, 0.2706), (0.85, 0.2901),
    (0.875, 0.3136), (0.90, 0.3415), (0.925, 0.3734), (0.95, 0.4084), (0.975, 0.4448),
    (1.00, 0.4805), (1.025, 0.5136), (1.05, 0.5427), (1.075, 0.5677), (1.10, 0.5883),
    (1.125, 0.6053), (1.15, 0.6191), (1.20, 0.6393), (1.25, 0.6518), (1.30, 0.6589),
    (1.35, 0.6621), (1.40, 0.6625), (1.45, 0.6607), (1.50, 0.6573), (1.55, 0.6528),
    (1.60, 0.6474), (1.65, 0.6413), (1.70, 0.6347), (1.75, 0.6280), (1.80, 0.6210),
    (1.85, 0.6141), (1.90, 0.6072), (1.95, 0.6003), (2.00, 0.5934), (2.05, 0.5867),
    (2.10, 0.5804), (2.15, 0.5743), (2.20, 0.5685), (2.25, 0.5630), (2.30, 0.5577),
    (2.35, 0.5527), (2.40, 0.5481), (2.45, 0.5438), (2.50, 0.5397), (2.60, 0.5325),
    (2.70, 0.5264), (2.80, 0.5211), (2.90, 0.5168), (3.00, 0.5133), (3.10, 0.5105),
    (3.20, 0.5084), (3.30, 0.5067), (3.40, 0.5054), (3.50, 0.5040), (3.60, 0.5030),
    (3.70, 0.5022), (3.80, 0.5016), (3.90, 0.5010), (4.00, 0.5006), (4.20, 0.4998),
    (4.40, 0.4995), (4.60, 0.4992), (4.80, 0.4990), (5.00, 0.4988),
]

G7 = [
    (0.00, 0.1198), (0.05, 0.1197), (0.10, 0.1196), (0.15, 0.1194), (0.20, 0.1193),
    (0.25, 0.1194), (0.30, 0.1194), (0.35, 0.1194), (0.40, 0.1193), (0.45, 0.1193),
    (0.50, 0.1194), (0.55, 0.1193), (0.60, 0.1194), (0.65, 0.1197), (0.70, 0.1202),
    (0.725, 0.1207), (0.75, 0.1215), (0.775, 0.1226), (0.80, 0.1242), (0.825, 0.1266),
    (0.85, 0.1306), (0.875, 0.1368), (0.90, 0.1464), (0.925, 0.1660), (0.95, 0.2054),
    (0.975, 0.2993), (1.00, 0.3803), (1.025, 0.4015), (1.05, 0.4043), (1.075, 0.4034),
    (1.10, 0.4014), (1.125, 0.3987), (1.15, 0.3955), (1.20, 0.3884), (1.25, 0.3810),
    (1.30, 0.3732), (1.35, 0.3657), (1.40, 0.3580), (1.50, 0.3440), (1.55, 0.3376),
    (1.60, 0.3315), (1.65, 0.3260), (1.70, 0.3209), (1.75, 0.3160), (1.80, 0.3117),
    (1.85, 0.3078), (1.90, 0.3042), (1.95, 0.3010), (2.00, 0.2980), (2.05, 0.2951),
    (2.10, 0.2922), (2.15, 0.2892), (2.20, 0.2864), (2.25, 0.2835), (2.30, 0.2807),
    (2.35, 0.2779), (2.40, 0.2752), (2.45, 0.2725), (2.50, 0.2697), (2.55, 0.2670),
    (2.60, 0.2643), (2.65, 0.2615), (2.70, 0.2588), (2.75, 0.2561), (2.80, 0.2533),
    (2.85, 0.2506), (2.90, 0.2479), (2.95, 0.2451), (3.00, 0.2424), (3.10, 0.2368),
    (3.20, 0.2313), (3.30, 0.2258), (3.40, 0.2205), (3.50, 0.2154), (3.60, 0.2106),
    (3.70, 0.2060), (3.80, 0.2017), (3.90, 0.1975), (4.00, 0.1935), (4.20, 0.1861),
    (4.40, 0.1793), (4.60, 0.1730), (4.80, 0.1672), (5.00, 0.1618),
]

PRESETS = {
    "baseball": (0.145, 0.0737, 0.35, 40.0),
    "golf_ball": (0.0459, 0.0427, 0.25, 70.0),
    "tennis_ball": (0.0577, 0.0670, 0.55, 30.0),
}


class Drag:
    def __init__(self, points):
        pts = sorted(points)
        if not pts:
            raise ValueError("a drag curve needs at least one (mach, cd) point")
        self.m = [p[0] for p in pts]
        self.c = [p[1] for p in pts]

    def __call__(self, mach):
        m, c = self.m, self.c
        if mach <= m[0]:
            return c[0]
        if mach >= m[-1]:
            return c[-1]
        i = bisect.bisect_right(m, mach)
        f = (mach - m[i - 1]) / (m[i] - m[i - 1])
        return c[i - 1] + f * (c[i] - c[i - 1])

    @classmethod
    def constant(cls, cd):
        return cls([(0.0, cd), (10.0, cd)])

    @classmethod
    def from_csv(cls, path):
        pts = []
        with open(path, newline="") as f:
            for row in csv.reader(f):
                try:
                    pts.append((float(row[0]), float(row[1])))
                except (ValueError, IndexError):
                    pass
        if not pts:
            raise ValueError(f"no usable 'mach,cd' rows in {path}")
        return cls(pts)


@dataclass
class Air:
    temp_c: float = 15.0
    pressure: float = P0
    humidity: float = 0.0
    rho_override: float = None

    @classmethod
    def standard(cls, altitude=0.0):
        t = T0 - LAPSE * altitude
        return cls(t - 273.15, P0 * (t / T0) ** 5.25588)

    def density(self):
        if self.rho_override is not None:
            return self.rho_override
        t = self.temp_c
        tk = t + 273.15
        sat = 611.21 * math.exp((18.678 - t / 234.5) * (t / (257.14 + t)))
        pv = min(max(self.humidity, 0.0), 1.0) * sat
        return (self.pressure - pv) / (R_AIR * tk) + pv / (R_VAP * tk)

    def sound(self):
        return math.sqrt(1.4 * R_AIR * (self.temp_c + 273.15))


@dataclass
class Bullet:
    mass: float
    diameter: float
    curve: Drag
    bc: float = None
    length: float = None
    twist: float = None
    right_twist: bool = True
    name: str = "projectile"

    def drag_factor(self, mach):
        cd = self.curve(mach)
        if self.bc:
            return 0.5 * cd * math.pi / 4 / self.bc
        return 0.5 * cd * math.pi * self.diameter ** 2 / 4 / self.mass


def from_bc(model, bc, mass, diameter, custom=None, **kw):
    model = model.upper()
    if bc <= 0:
        raise ValueError("the ballistic coefficient must be above zero")
    if model == "G1":
        curve = Drag(G1)
    elif model == "G7":
        curve = Drag(G7)
    elif model == "CUSTOM" and custom is not None:
        curve = custom
    else:
        raise ValueError("model must be G1, G7 or CUSTOM (with a drag curve)")
    return Bullet(mass, diameter, curve, bc * LB_IN2, name=f"{model} BC={bc}", **kw)


def from_cd(mass, diameter, cd=None, curve=None, **kw):
    if curve is None:
        if cd is None:
            raise ValueError("give either a drag coefficient or a drag curve")
        curve = Drag.constant(cd)
    kw.setdefault("name", "Cd model")
    return Bullet(mass, diameter, curve, **kw)


@dataclass
class Env:
    air: Air
    wind: float = 0.0
    wind_from: float = 90.0
    incline: float = 0.0
    lat: float = None
    azimuth: float = 0.0
    g: float = G0


def tilt(v, a):
    f, u, r = v
    c, s = math.cos(a), math.sin(a)
    return f * c + u * s, -f * s + u * c, r


def earth_spin(env):
    if env.lat is None:
        return 0.0, 0.0, 0.0
    la, az = math.radians(env.lat), math.radians(env.azimuth)
    w = (OMEGA * math.cos(la) * math.cos(az),
         OMEGA * math.sin(la),
         -OMEGA * math.cos(la) * math.sin(az))
    return tilt(w, math.radians(env.incline))


def nudge(v, k, h):
    return [a + h * b for a, b in zip(v, k)]


def fly(b, env, v0, angle, max_range, dt=0.0005):
    inc = math.radians(env.incline)
    g = (-env.g * math.sin(inc), -env.g * math.cos(inc), 0.0)
    wa = math.radians(env.wind_from)
    wx, wy, wz = tilt((-env.wind * math.cos(wa), 0.0, -env.wind * math.sin(wa)), inc)
    sx, sy, sz = earth_spin(env)
    rho = env.air.density()
    c = env.air.sound()

    def acc(vx, vy, vz):
        rx, ry, rz = vx - wx, vy - wy, vz - wz
        s = math.sqrt(rx * rx + ry * ry + rz * rz)
        k = b.drag_factor(s / c) * rho * s
        return (g[0] - k * rx - 2 * (sy * vz - sz * vy),
                g[1] - k * ry - 2 * (sz * vx - sx * vz),
                g[2] - k * rz - 2 * (sx * vy - sy * vx))

    t = x = y = z = 0.0
    v = (v0 * math.cos(angle), v0 * math.sin(angle), 0.0)
    track = [(t, x, y, z) + v]
    while x < max_range and t < 300.0:
        k1 = acc(*v)
        k2 = acc(*nudge(v, k1, dt / 2))
        k3 = acc(*nudge(v, k2, dt / 2))
        k4 = acc(*nudge(v, k3, dt))
        nv = tuple(v[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(3))
        x += dt * 0.5 * (v[0] + nv[0])
        y += dt * 0.5 * (v[1] + nv[1])
        z += dt * 0.5 * (v[2] + nv[2])
        v = nv
        t += dt
        track.append((t, x, y, z) + v)
        if v[0] <= 0.5:
            break
    return track


def at_range(track, r):
    xs = [p[1] for p in track]
    i = bisect.bisect_left(xs, r)
    if i == 0:
        return track[0]
    if i >= len(track):
        return None
    a, b = track[i - 1], track[i]
    span = b[1] - a[1]
    f = (r - a[1]) / span if span else 0.0
    return tuple(a[k] + f * (b[k] - a[k]) for k in range(7))


def solve_zero(b, env, v0, zero, sight, dt=0.0005):
    calm = Env(env.air, g=env.g)

    def miss(angle):
        hit = at_range(fly(b, calm, v0, angle, zero * 1.001, dt), zero)
        return -1e9 if hit is None else hit[2] - sight

    lo, hi = -0.05, 0.35
    if miss(lo) > 0 or miss(hi) < 0:
        raise RuntimeError("that zero range can't be reached with this projectile and speed")
    for _ in range(45):
        mid = 0.5 * (lo + hi)
        if miss(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def stability(b, v0, air):
    if not (b.length and b.twist):
        return None
    grains = b.mass / GRAIN
    d_in = b.diameter / INCH
    length = b.length / b.diameter
    twist = b.twist / b.diameter
    sg = 30.0 * grains / (twist ** 2 * d_in ** 3 * length * (1.0 + length ** 2))
    sg *= (v0 / FOOT / 2800.0) ** (1.0 / 3.0)
    sg *= ((air.temp_c * 1.8 + 32.0 + 460.0) / 519.0) * (29.92 / (air.pressure / INHG))
    return sg


def spin_drift(sg, t, right=True):
    if sg is None or sg < 1.0:
        return 0.0
    return (1 if right else -1) * 1.25 * (sg + 1.2) * t ** 1.83 * INCH


@dataclass
class Row:
    range_m: float
    time: float
    speed: float
    mach: float
    energy: float
    drop: float
    wind_drift: float
    spin_drift: float
    up: float
    side: float


@dataclass
class Solution:
    zero_angle: float
    launch_angle: float
    sg: float
    rows: list
    peak: float
    peak_at: float
    subsonic: float
    transonic: float


def compute(b, env, v0, sight=0.0, zero=None, angle=None, ranges=None,
            max_range=1000.0, step=100.0, dt=0.0005):
    if angle is None:
        zero_angle = solve_zero(b, env, v0, zero, sight, dt) if zero and zero > 0 else 0.0
        angle = zero_angle
    else:
        zero_angle = None

    if ranges is None:
        if step <= 0:
            raise ValueError("the range step must be above zero")
        ranges = [i * step for i in range(int(max_range / step) + 1)]

    track = fly(b, env, v0, angle, max(ranges) * 1.002, dt)
    c = env.air.sound()
    sg = stability(b, v0, env.air)

    rows = []
    for r in ranges:
        p = track[0] if r == 0 else at_range(track, r)
        if p is None:
            break
        t, x, y, z, vx, vy, vz = p
        s = math.sqrt(vx * vx + vy * vy + vz * vz)
        spin = spin_drift(sg, t, b.right_twist)
        drop = y - sight
        side = z + spin
        rows.append(Row(r, t, s, s / c, 0.5 * b.mass * s * s, drop, z, spin,
                        -math.atan2(drop, x) if x > 0 else 0.0,
                        -math.atan2(side, x) if x > 0 else 0.0))

    peak, peak_at = -1e9, 0.0
    subsonic = transonic = None
    for p in track:
        if p[2] - sight > peak:
            peak, peak_at = p[2] - sight, p[1]
        m = math.sqrt(p[4] ** 2 + p[5] ** 2 + p[6] ** 2) / c
        if transonic is None and m < 1.2:
            transonic = p[1]
        if subsonic is None and m < 1.0:
            subsonic = p[1]
    return Solution(zero_angle, angle, sg, rows, peak, peak_at, subsonic, transonic)


def selftest():
    ok = True

    def check(name, passed, note=""):
        nonlocal ok
        ok = ok and bool(passed)
        print(f"  [{'PASS' if passed else 'FAIL'}] {name} {note}")

    print("Running self-tests...")

    vac = Env(Air(rho_override=0.0))
    ball = from_cd(0.01, 0.01, cd=0.3)
    a, v0 = math.radians(30), 100.0
    p = at_range(fly(ball, vac, v0, a, 800.0, 0.001), 400.0)
    exact = 400.0 * math.tan(a) - G0 * 400.0 ** 2 / (2 * v0 ** 2 * math.cos(a) ** 2)
    check("vacuum path matches the exact parabola", abs(p[2] - exact) < 0.01,
          f"(sim {p[2]:.4f} m, exact {exact:.4f} m)")

    bullet = from_bc("G7", 0.25, 175 * GRAIN, 0.308 * INCH)
    std = Env(Air.standard())
    coarse = at_range(fly(bullet, std, 800.0, 0.01, 1000, 0.001), 1000)[2]
    fine = at_range(fly(bullet, std, 800.0, 0.01, 1000, 0.00025), 1000)[2]
    check("result doesn't depend on time step", abs(coarse - fine) < 1e-3,
          f"(diff {abs(coarse - fine) * 1000:.3f} mm)")

    rifle = from_bc("G1", 0.475, 168 * GRAIN, 0.308 * INCH)
    z = compute(rifle, std, 823.0, sight=0.038, zero=100.0, ranges=[100.0])
    check("zero crosses the line of sight at the zero range", abs(z.rows[0].drop) < 1e-4,
          f"(error {z.rows[0].drop * 1000:.4f} mm)")

    table = compute(rifle, std, 823.0, sight=0.038, zero=100.0, max_range=1000, step=100)
    speeds = [r.speed for r in table.rows]
    check("speed always decreases", all(a > b for a, b in zip(speeds, speeds[1:])))

    def drop_drift(bc):
        s = compute(from_bc("G1", bc, 168 * GRAIN, 0.308 * INCH), Env(Air.standard(), 5, 90),
                    823.0, ranges=[600.0], angle=0.0)
        return s.rows[0].drop, s.rows[0].wind_drift

    (d_lo, w_lo), (d_hi, w_hi) = drop_drift(0.3), drop_drift(0.6)
    check("higher BC gives less drop and less drift", d_hi > d_lo and abs(w_hi) < abs(w_lo))
    check("wind from the right pushes the bullet left", w_lo < 0)

    check("air thins out with altitude", Air.standard(3000).density() < Air.standard(0).density())
    rho = Air.standard().density()
    check("standard sea-level density is 1.225 kg/m3", abs(rho - 1.225) < 0.001, f"({rho:.4f})")

    print("All tests passed." if ok else "Some tests FAILED.")
    return ok


def clean(x, digits=2):
    return round(x, digits) + 0.0


def ask(question, default=None, kind=float, allowed=None):
    while True:
        hint = f" [{default}]" if default is not None else ""
        answer = input(f"  {question}{hint}: ").strip()
        if not answer:
            if default is not None:
                return default
            print("    Please type a value.")
            continue
        try:
            value = kind(answer)
        except ValueError:
            print("    Couldn't read that, try again.")
            continue
        if allowed and value not in allowed:
            print("    Please choose one of: " + ", ".join(str(a) for a in allowed))
            continue
        return value


def wizard():
    print("\nBallistics Calculator (metric)")
    print("Press Enter to accept the value in [brackets].\n")
    print("What are you launching?")
    print("  1 = a bullet or pellet with a ballistic coefficient (BC)")
    print("  2 = something with a plain drag coefficient (Cd)")
    print("  3 = a ready-made ball (baseball, golf_ball, tennis_ball)")
    kind = ask("Choose 1, 2 or 3", 1, int, [1, 2, 3])
    argv = []

    if kind == 3:
        name = ask("Which ball?", "baseball", str.lower, sorted(PRESETS))
        argv += ["--preset", name, "--mv", str(ask("Launch speed (m/s)", PRESETS[name][3]))]
        argv += ["--angle", str(ask("Launch angle above horizontal (deg)", 30.0))]
    else:
        argv += ["--mv", str(ask("Launch speed (m/s)", 823))]
        argv += ["--weight", str(ask("Weight (g)", 10.9))]
        argv += ["--diameter", str(ask("Diameter (mm)", 7.82))]
        if kind == 1:
            model = ask("Drag model (G1 or G7)", "G1", str.upper, ["G1", "G7"])
            argv += ["--model", model, "--bc", str(ask("Ballistic coefficient (lb/in^2)", 0.462))]
        else:
            argv += ["--cd", str(ask("Drag coefficient Cd", 0.4))]
        argv += ["--sight-height", str(ask("Sight height above barrel (mm)", 38))]
        argv += ["--zero", str(ask("Zero range (m, 0 = none)", 100))]

    argv += ["--max-range", str(ask("Table goes out to (m)", 1000 if kind != 3 else 100))]
    argv += ["--step", str(ask("Table step (m)", 100 if kind != 3 else 10))]

    wind = ask("Wind speed (m/s, 0 = calm)", 0.0)
    if wind > 0:
        argv += ["--wind-speed", str(wind)]
        argv += ["--wind-dir", str(ask("Wind comes FROM (0 ahead, 90 right, 180 behind, 270 left) deg", 90.0))]

    if ask("Standard weather (sea level, 15 C)? yes/no", "yes", str.lower, ["yes", "no"]) == "no":
        argv += ["--temp", str(ask("Temperature (C)", 15))]
        argv += ["--pressure", str(ask("Station pressure (hPa)", 1013.25))]
        argv += ["--humidity", str(ask("Relative humidity (%)", 50.0))]

    if kind != 3 and ask("Include Earth's rotation (Coriolis)? yes/no", "no", str.lower, ["yes", "no"]) == "yes":
        argv += ["--lat", str(ask("Latitude (deg, north positive)", 40.0))]
        argv += ["--azimuth", str(ask("Direction of fire (deg clockwise from north)", 0.0))]

    print("\nSame thing from the command line:")
    print("  python ballistics.py " + " ".join(argv) + "\n")
    return argv


def parser():
    p = argparse.ArgumentParser(description="External ballistics calculator (metric). "
                                            "Run with no options to be asked questions.")
    p.add_argument("--interactive", action="store_true", help="ask questions instead")
    p.add_argument("--preset", choices=sorted(PRESETS), help="ready-made ball")
    p.add_argument("--mv", type=float, help="launch velocity, m/s")
    p.add_argument("--model", default="G1", choices=["G1", "G7", "CUSTOM"])
    p.add_argument("--bc", type=float, help="ballistic coefficient, lb/in^2")
    p.add_argument("--cd", type=float, help="drag coefficient (instead of a BC)")
    p.add_argument("--drag-csv", help="file of 'mach,cd' lines")
    p.add_argument("--weight", type=float, help="mass, grams")
    p.add_argument("--diameter", type=float, help="diameter, mm")
    p.add_argument("--length", type=float, help="projectile length, mm (spin drift)")
    p.add_argument("--twist", type=float, help="barrel twist, mm per turn (spin drift)")
    p.add_argument("--left-twist", action="store_true", help="left-hand rifling")
    p.add_argument("--sight-height", type=float, default=0.0, help="sight above barrel, mm")
    p.add_argument("--zero", type=float, default=0.0, help="zero range, m (0 = none)")
    p.add_argument("--angle", type=float, help="barrel angle above line of sight, deg (skips zeroing)")
    p.add_argument("--max-range", type=float, default=1000.0, help="last range in the table, m")
    p.add_argument("--step", type=float, default=100.0, help="table spacing, m")
    p.add_argument("--temp", type=float, help="air temperature, C")
    p.add_argument("--pressure", type=float, help="station pressure, hPa")
    p.add_argument("--humidity", type=float, default=0.0, help="relative humidity, percent")
    p.add_argument("--altitude", type=float, default=0.0, help="altitude, m")
    p.add_argument("--wind-speed", type=float, default=0.0, help="wind speed, m/s")
    p.add_argument("--wind-dir", type=float, default=90.0,
                   help="direction wind comes FROM, deg (0 ahead, 90 right, 180 behind, 270 left)")
    p.add_argument("--incline", type=float, default=0.0, help="shot angle, deg (+ uphill)")
    p.add_argument("--lat", type=float, help="latitude, deg (turns Coriolis on)")
    p.add_argument("--azimuth", type=float, default=0.0, help="direction of fire, deg clockwise from north")
    p.add_argument("--dt", type=float, default=0.0005, help="time step, s")
    p.add_argument("--csv", help="save the table to this CSV file")
    p.add_argument("--plot", help="save a trajectory PNG (needs matplotlib)")
    p.add_argument("--selftest", action="store_true", help="run the built-in checks")
    return p


def build(args):
    if args.preset:
        mass, diameter, cd, v_typ = PRESETS[args.preset]
        return from_cd(mass, diameter, cd=cd, name=args.preset), args.mv or v_typ

    if None in (args.mv, args.weight, args.diameter):
        raise ValueError("need at least --mv, --weight and --diameter (or --preset)")
    mass, diameter = args.weight / 1000, args.diameter / 1000
    custom = Drag.from_csv(args.drag_csv) if args.drag_csv else None
    extra = dict(length=args.length / 1000 if args.length else None,
                 twist=args.twist / 1000 if args.twist else None,
                 right_twist=not args.left_twist)
    if args.bc is not None:
        model = "CUSTOM" if custom else args.model
        return from_bc(model, args.bc, mass, diameter, custom, **extra), args.mv
    if args.cd is not None or custom:
        return from_cd(mass, diameter, args.cd, custom, **extra), args.mv
    raise ValueError("give a drag description: --bc, --cd or --drag-csv")


def run(args):
    b, v0 = build(args)
    air = Air.standard(args.altitude)
    if args.temp is not None:
        air.temp_c = args.temp
    if args.pressure is not None:
        air.pressure = args.pressure * 100.0
    air.humidity = args.humidity / 100.0
    env = Env(air, args.wind_speed, args.wind_dir, args.incline, args.lat, args.azimuth)

    sol = compute(b, env, v0, args.sight_height / 1000,
                  zero=args.zero if args.zero > 0 else None,
                  angle=math.radians(args.angle) if args.angle is not None else None,
                  max_range=args.max_range, step=args.step, dt=args.dt)
    if not sol.rows:
        raise RuntimeError("the projectile never reached the first range in the table")

    report(args, b, env, v0, sol)
    if args.csv:
        write_csv(args.csv, sol)
    if args.plot:
        plot(args.plot, b, env, v0, sol, args)
    return 0


def report(args, b, env, v0, sol):
    line = "=" * 96
    print(line)
    print(f" Projectile : {b.name}   mass {b.mass * 1000:.2f} g   diameter {b.diameter * 1000:.2f} mm")
    print(f" Launch     : {v0:.0f} m/s   air density {env.air.density():.4f} kg/m3   "
          f"speed of sound {env.air.sound():.1f} m/s")
    print(f" Wind       : {env.wind:.1f} m/s from {env.wind_from:.0f} deg   "
          f"incline {env.incline:+.1f} deg   Coriolis {'on' if env.lat is not None else 'off'}")
    if sol.zero_angle is not None and args.zero > 0:
        print(f" Zero       : {args.zero:g} m   barrel angle {math.degrees(sol.zero_angle):.4f} deg")
    if sol.sg is not None:
        note = "" if sol.sg >= 1.4 else "  (marginal - spin drift ignored below 1.0)"
        print(f" Stability  : Sg = {sol.sg:.2f}{note}")
    tail = f" Highest point {clean(sol.peak * 100, 1)} cm above line of sight at {sol.peak_at:.0f} m"
    if sol.transonic:
        tail += f"   |  below Mach 1.2 at {sol.transonic:.0f} m"
    if sol.subsonic:
        tail += f"   |  subsonic at {sol.subsonic:.0f} m"
    print(tail)
    print(line)

    print(f"{'Range':>7} {'Speed':>7} {'Mach':>5} {'Energy':>8} {'Time':>6} "
          f"{'Drop':>8} {'Up':>7} {'Up':>6} {'Drift':>8} {'Wind':>7} {'Wind':>6}")
    print(f"{'m':>7} {'m/s':>7} {'':>5} {'J':>8} {'s':>6} {'cm':>8} {'MOA':>7} {'MIL':>6} "
          f"{'cm':>8} {'MOA':>7} {'MIL':>6}")
    print("-" * 96)
    for r in sol.rows:
        side = r.wind_drift + r.spin_drift
        print(f"{r.range_m:7.0f} {r.speed:7.0f} {r.mach:5.2f} {r.energy:8.0f} {r.time:6.3f} "
              f"{clean(r.drop * 100):8.2f} {clean(r.up * MOA):7.2f} {clean(r.up * MIL):6.2f} "
              f"{clean(side * 100):8.2f} {clean(r.side * MOA):7.2f} {clean(r.side * MIL):6.2f}")
    print("-" * 96)

    last = sol.rows[-1]
    side = last.wind_drift + last.spin_drift
    print("\nIn plain words:")
    print(f"  At {last.range_m:.0f} m the projectile is moving at {last.speed:.0f} m/s "
          f"(Mach {last.mach:.2f}) and arrives {last.time:.2f} s after launch.")
    where = "below" if last.drop < 0 else "above"
    if args.preset:
        print(f"  It is {abs(clean(last.drop * 100, 1))} cm {where} its launch height.")
    else:
        print(f"  It is {abs(clean(last.drop * 100, 1))} cm {where} the line of sight, so dial "
              f"{'up' if last.up > 0 else 'down'} about {abs(clean(last.up * MOA, 1))} MOA "
              f"({abs(clean(last.up * MIL, 1))} MIL).")
    if abs(side) * 100 >= 0.05:
        print(f"  Wind, spin and Earth's rotation push it {abs(clean(side * 100, 1))} cm "
              f"to the {'right' if side > 0 else 'left'}.")
    print("\nDrop = height vs line of sight (minus = below). Up = dial up. "
          "Drift = sideways offset (plus = right). Wind = dial right (plus) or left (minus).")


def write_csv(path, sol):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["range_m", "time_s", "speed_mps", "mach", "energy_J", "drop_m", "wind_drift_m",
                    "spin_drift_m", "up_moa", "up_mil", "wind_moa", "wind_mil"])
        for r in sol.rows:
            w.writerow([f"{r.range_m:.2f}", f"{r.time:.4f}", f"{r.speed:.2f}", f"{r.mach:.3f}",
                        f"{r.energy:.1f}", f"{r.drop:.5f}", f"{r.wind_drift:.5f}", f"{r.spin_drift:.5f}",
                        f"{r.up * MOA:.3f}", f"{r.up * MIL:.3f}", f"{r.side * MOA:.3f}", f"{r.side * MIL:.3f}"])
    print(f"\nSaved the table to {path}")


def plot(path, b, env, v0, sol, args):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nmatplotlib isn't installed, so no plot was made (pip install matplotlib).")
        return
    far = max(r.range_m for r in sol.rows)
    track = fly(b, env, v0, sol.launch_angle, far, args.dt)
    sight = args.sight_height / 1000
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot([p[1] for p in track], [(p[2] - sight) * 100 for p in track])
    ax.axhline(0, color="gray", lw=0.8, ls="--")
    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Height vs line of sight (cm)")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    print(f"\nSaved the plot to {path}")


def main(argv=None):
    if argv is None and len(sys.argv) == 1:
        argv = ["--interactive"]
    args = parser().parse_args(argv)
    if args.selftest:
        return 0 if selftest() else 1
    if args.interactive:
        try:
            args = parser().parse_args(wizard())
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return 0
    try:
        return run(args)
    except (ValueError, RuntimeError, OSError) as e:
        print(f"\nCouldn't finish that: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
