import math
from math import log
from math import log10

def a(hre):
    return 3.2 * (math.log(hre * 11.75)) ** 2 - 4.97


def FOURg_pl(fc, hte, hre, d, Cm):
    return (
        46.3
        + 33.9 * math.log(fc, 10)
        - 13.82 * math.log(hte, 10)
        - a(hre)
        + (44.9 - 6.55 * math.log(hte))
        + Cm
    )


def THREEg_pl(d, f):
    return 40 * math.log(d, 10) + 30 * math.log(f, 10) + 49


def FOURg_pl(w: int, h: int, hbs: int, d3d: int, fc: int, hut: int):
    return (161.04 - 7.1*log10(w) + 7.5*log10(h)
            - (24.37 - 3.7 * (h/hbs)**2) * log10(hbs) 
            + (43.42 - 3.1 * log10(hbs)) * (log10(d3d)-3) + 20*log10(fc)
            - (3.2 * (log10(17.625))**2 - 4.97) - 0.6(hut - 1.5))


def PLfs()

def wifi_pl(d, x):
    return 
