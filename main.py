from math import *
from scipy.stats import norm

speed_of_light = 3e8


def a(hre: float) -> float:
    """
    Correcting factor
    Needed by `def TWOg_pl`
    """
    return 3.2 * (log(hre * 11.75)) ** 2 - 4.97


def TWOg_pl(fc: float, hte: float, hre: float, d: float, Cm: float) -> float:
    """
    fc - 1500..2000 Mhz
    h_te - 30..200 m
    h_re - 1..10 m
    d - 1..20 km
    """
    # assert 1 <= d <= 20
    assert 30 <= hte <= 200
    assert 1 <= hre <= 10
    assert 1500 <= fc <= 2000
    return (
        46.3
        + 33.9 * log10(fc)
        - 13.82 * log10(hte)
        - a(hre)
        + (44.9 - 6.55 * log10(hte))
        + Cm
    )


def THREEg_pl(d: float, f: float) -> float:
    """
    d - distance from BTS to mobile station(MS) in km
    f - frequency in MHz (somewhere around 2 GHz)
    """
    return 40 * log(d, 10) + 30 * log(f, 10) + 49


def FOURg_pl(
    d3d: float,
    fc: float,
    hut: float = 1.5,
    w: float = 10,
    h: float = 20,
    hbs: float = 16,
) -> float:
    """
    fc - GHz
    """
    return (
        161.04
        - 7.1 * log10(w)
        + 7.5 * log10(h)
        - (24.37 - 3.7 * (h / hbs) ** 2) * log10(hbs)
        + (43.42 - 3.1 * log10(hbs)) * (log10(d3d) - 3)
        + 20 * log10(fc)
        - (3.2 * (log10(17.625)) ** 2 - 4.97)
        - 0.6 * (hut - 1.5)
    )


def calc_G2(f: float, A: float = 5) -> float:
    l = speed_of_light / f
    return 4 * pi * A / (l**2)


def wifi_plfs(d: float, f: float) -> float:
    """
    d - distance in m
    f - frequency in Hz
    """
    l = speed_of_light / f
    return -20 * log10(l / (4 * pi * d)) - calc_G2(f)


def wifi_pl__d_less_5(f: float, d: float, x: float) -> float:
    """
    f - frequency in Hz
    d - distance in m
    x - random value
    """
    return wifi_plfs(d, f) + x


def wifi_pl__d_more_5(f: float, d: float, dbp: float, x: float) -> float:
    """
    f - frequency in Hz
    d - distance in m
    dbp - distance to breakpoint in m
    x - random value
    """
    return wifi_plfs(d, f) + 3.5 * 10 * log10(d / dbp) + x


Pt = 43
d = [0.35, 0.32, 0.3]
g2_f = 1800
g3_f = 1800
g4_f = 2.14
wifi_g = 5
hte = 50
hut = 1.5
hre = 5
Cm = 3

print("=========Calculated powers=========")
print("2G:", end=' ')
for cur_d in d:
    print(Pt - TWOg_pl(g2_f, hte, hre, cur_d, Cm), end=' ')

print("\n3G:", end=' ')
for cur_d in d:
    print(Pt - THREEg_pl(cur_d, g3_f), end=' ')

print("\n4G:", end=' ')
for cur_d in d:
    print(Pt - FOURg_pl(cur_d * 1000, g4_f, hut), end=' ')

# This does not work somehow...
# print(Pt - wifi_pl__d_more_5(wifi_g, d * 1000, 5, 0.5))
# print(Pt - wifi_pl__d_less_5(wifi_g, d * 1000, 0.5))

print("\n\n=========Probabilities=========")
g2_powers = [-60, -56, -49]
g3_powers = [-71, -60, -59]
g4_powers = [-83, -67, -77]

g23_sigma = 12
g4_sigma = 6

expected_power = 100
precision = 8

print("2G:", end=' ')
for cur_g2_p in g2_powers:
    val = norm.cdf((expected_power + cur_g2_p)/g23_sigma)
    print(round(val, precision), end=' ')

print("\n3G:", end=' ')
for cur_g3_p in g3_powers:
    val = norm.cdf((expected_power + cur_g3_p)/g23_sigma)
    print(round(val, precision), end=' ')

print("\n4G:", end=' ')
for cur_g4_p in g4_powers:
    val = norm.cdf((expected_power + cur_g4_p)/g4_sigma)
    print(round(val, precision), end=' ')
