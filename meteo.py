#!/usr/bin/env python3

from math import log10, sqrt, pow


def T_f2T_c(T_f):
    # Convert temperature in deg F to deg C.
    # Source: https://www.weather.gov/media/epz/wxcalc/tempConvert.pdf
    return (5/9) * (T_f-32)

def T_c2T_f(T_c):
    # Convert temperature in deg C to deg F.
    # Source: https://www.weather.gov/media/epz/wxcalc/tempConvert.pdf
    return (9/5)*T_c + 32

def W_mph2W_mps(W_mph):
    # Convert wind speed in miles per hour to meters per second.
    # Source: https://www.weather.gov/media/epz/wxcalc/windConversion.pdf
    return 0.44704*W_mph

def W_mps2W_mph(W_mps):
    # Convert wind speed in meters per second to miles per hour.
    # Source: https://www.weather.gov/media/epz/wxcalc/windConversion.pdf
    return 2.23694*W_mps

def P_inHg2P_hPa(P_inHg):
    # Convert pressure in inches of mercury to hectopascals (millibars).
    # Source: https://www.weather.gov/media/epz/wxcalc/pressureConversion.pdf
    return 33.8639*P_inHg

def P_hPa2P_inHg(P_hPa):
    # Convert pressure in hectopascals (millibars) to inches of mercury.
    # Source: https://www.weather.gov/media/epz/wxcalc/pressureConversion.pdf
    return 0.0295300*P_hPa

def P_mmHg2P_hPa(P_mmHg):
    # Convert pressure in millimeters of mercury (torr) to hectopascals (millibars).
    # Source: https://www.weather.gov/media/epz/wxcalc/pressureConversion.pdf
    return 1.333224*P_mmHg

def P_hPa2P_mmHg(P_hPa):
    # Convert pressure in hectopascals (millibars) to millimeters of mercury (torr).
    # Source: https://www.weather.gov/media/epz/wxcalc/pressureConversion.pdf
    return 0.750062*P_hPa

def HI_T_f(T_f, RH):
    # Heat Index calculation.
    # T_f in deg F; RH in %; HI (output) in deg F.
    # Source: https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
    hi = 0.5 * (T_f + 61.0 + ((T_f-68.0)*1.2) + (RH*0.094))
    if (T_f+hi)/2 < 80:
        return hi

    hi = -42.379 + 2.04901523*T_f + 10.14333127*RH - 0.22475541*T_f*RH - 0.00683783*T_f*T_f - \
        0.05481717*RH*RH + 0.00122874*T_f*T_f*RH + 0.00085282*T_f*RH*RH - 0.00000199*T_f*T_f*RH*RH

    if RH < 13.0 and T_f > 80 and T_f < 87:
        hi -= ((RH-85)/10) * ((87-T_f)/5)

    return hi

def Dp_T_c(T_c, RH, b=17.62, l=243.12):
    # Dew point calculation.
    # T_c in deg C; RH in %; Dp (output) in deg C.
    # Source:
    # http://irtfweb.ifa.hawaii.edu/~tcs3/tcs3/Misc/Dewpoint_Calculation_Humidity_Sensor_E.pdf
    H = (log10(RH)-2)/0.4343 + (b*T_c)/(l+T_c)
    return l*H / (b-H)

def WC_W_ms(T_c, W_ms):
    # Wind Chill calculation.
    # T_c in deg C; W_ms in meters per second;
    # WC (output) in Watts per meter squared.
    # Source: https://www.weather.gov/media/epz/wxcalc/windChill.pdf
    return (12.1452 + 11.6222*sqrt(W_ms) - 1.16222*W_ms) * (33 - T_c)

def WC_T_f(T_f, W_mph):
    # Wind Chill calculation.
    # T_f in deg F; W_mph in miles per hour; WC (output) in deg F.
    # Source: https://www.weather.gov/media/epz/wxcalc/windChill.pdf
    wp = pow(W_mph, 0.16)
    return 35.47 + (0.6215*T_f) - (35.75*wp) + (0.4275*T_f*wp)
