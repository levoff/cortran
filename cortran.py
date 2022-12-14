# Library to convert between WGS84 Lat/Lon and SK42 Lat/Lon and/or XY
# Maintained at https://github.com/levoff/cortran
# 
# License:
# 
# Copyright (c) 2020-2022 Levon Hovhannisyan
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies of this Software or works derived from this Software.
# 
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#  

# NOTE: Approximate Metric Equivalents for Degrees, Minutes, and Seconds
    # At the equator for longitude and for latitude anywhere, the following approximations are valid:
    # 1� = 111 km  (or 60 nautical miles)
    # 0.1� = 11.1 km
    # 0.01� = 1.11 km (2 decimals, km accuracy)
    # 0.001� =111 m
    # 0.0001� = 11.1 m
    # 0.00001� = 1.11 m
    # 0.000001� = 0.11 m (7 decimals, cm accuracy)
    # 1' = 1.85 km  (or 1 nautical mile)
    # 0.1' = 185 m
    # 0.01' = 18.5 m
    # 0.001' = 1.85 m
    # 30" = 900 m
    # 15" = 450 m
    # 3" = 90 m
    # 1" = 30 m
    # 1/3" = 10 m
    # 0.1" = 3 m
    # 1/9" = 3 m
    # 1/27" = 1 m

# LIST OF AVAILABLE CONVERSIONS
#       WGS84 Lat/Lon <-> SK42 Lat/Lon
#       SK42 Lat/Lon <-> SK42 XY

# TODO: Add USNG conversion
#       Add MGRS conversion


# Implemented according to GOST 51794-2001

# USAGE:
    # 1. WGS-84 coordinates MUST be converted into SK-42 lat,lon coordinates before being converted into X,Y format
    # 2. 'transform_latlon_wgs84_sk42' function converts WGS-84 to SK-42 lat,lon and vice versa
    # 
    # EXAMPLE 1: transform_latlon_wgs84_sk42(lat,lon, H, source='wgs84', target='sk42')
    # Converts input lat,lon WGS-84 coordinates into SK-42 lat,lon coordinates
    # 
    # EXAMPLE 2: transform_latlon_wgs84_sk42(lat,lon, H, source='sk42', target='wgs84')
    # Converts input lat,lon SK-42 coordinates into WGS-84 lat,lon coordinates


from math import sin, cos, tan, pi


def sk42xy_to_sk42latlon(x, y):
    # Implemented according to ГОСТ 51794-2001 equations: 29,30,31,32,33,34,35,36
    n = int(y * 0.000001)
    b = x/6367558.4968
    B0 = b + sin(2*b) * (0.00252588685 - 0.00001491860 * (sin(b)**2) + 0.00000011904 * (sin(b)**4))
    z0 = (y - (10*n + 5)*100000)/(6378245.0 * cos(B0))
    B = B0 - (z0**2) * sin(2*B0) * (0.251684631 - 0.003369263*(sin(B0)**2) + 0.000011276*(sin(B0)**4) 
         -(z0**2) * (0.10500614 - 0.04559916*sin(B0)**2 + 0.00228901*sin(B0)**4 - 0.00002987*sin(B0)**6
         -(z0**2) * (0.042858 - 0.025318*sin(B0)**2 + 0.014346*sin(B0)**4 - 0.001264*sin(B0)**6
         -(z0**2) * (0.01672 - 0.00630*sin(B0)**2 + 0.01188*sin(B0)**4 - 0.00328*sin(B0)**6))))

    L = 6 * (n - 0.5)/57.29577951 + (z0**1) * (1 - 0.0033467108*sin(B0)**2 - 0.0000056002*sin(B0)**4 - 0.0000000187*sin(B0)**6
        -(z0**2) * (0.16778975 + 0.16273586*sin(B0)**2 - 0.00052490*sin(B0)**4 - 0.00000846*sin(B0)**6
        -(z0**2) * (0.0420025 + 0.1487407*sin(B0)**2 - 0.0059420*sin(B0)**4 - 0.0000150*sin(B0)**6
        -(z0**2) * (0.01225 + 0.09477*sin(B0)**2 - 0.03282*sin(B0)**4 - 0.00034*sin(B0)**6
        -(z0**2) * (0.0038 + 0.0524*sin(B0)**2 - 0.0482*sin(B0)**4 - 0.0032*sin(B0)**6)))))
    lon = L*180/pi
    lat = B*180/pi

    return lat,lon

def sk42latlon_to_sk42xy(lat, lon):
    # Implemented according to ГОСТ 51794-2001
    rad = 0.0174533
    Bk = lat
    Lk = lon
    Bk_rad =  Bk*rad
    # Lk_rad =  Lk*rad
    n = int((Lk + 6)/6)
    l = (Lk - abs(3 + 6*(n - 1)))/57.29577951
    sk42_x =  6367558.4968 * Bk_rad - (sin(2*Bk_rad)) * (16002.8900 + 66.9607 * (sin(Bk_rad) ** 2) + 0.3515 * (sin(Bk_rad) ** 4) - (l **2) *(1594561.25 + 5336.535*(sin(Bk_rad)**2) + 26.790 * (sin(Bk_rad) ** 4) + 0.149 * (sin(Bk_rad)**6) + (l**2)*(672483.4 - 811219.9 * (sin(Bk_rad) ** 2) + 5420.0*(sin(Bk_rad)**4) - 10.6 * (sin(Bk_rad)**6) + (l**2)*(278194 - 830174*(sin(Bk_rad)**2) + 572434*(sin(Bk_rad)**4) - 16010*(sin(Bk_rad)**6) + (l**2)*(109500 - 574700*(sin(Bk_rad)**2) + 863700*(sin(Bk_rad)**4) - 398600*(sin(Bk_rad)**6))))));
    sk42_y = (5 + 10*n) * (10**5) + l * cos(Bk_rad) * (6378245 + 21346.1415 * (sin(Bk_rad)**2) + 107.1590 * (sin(Bk_rad)**4) + 0.5977*(sin(Bk_rad)**6) + (l**2)*( 1070204.16 - 2136826.66*(sin(Bk_rad)**2) + 17.98*(sin(Bk_rad) ** 4) - 11.99*(sin(Bk_rad)**6)) + (l**2)*(270806 - 1523417*(sin(Bk_rad) ** 2) + 1327645 * (sin(Bk_rad) ** 4) - 21701*(sin(Bk_rad) ** 6) + (l**2)*(79690 - 866190*(sin(Bk_rad) ** 2) + 1730360 * (sin(Bk_rad) ** 4) - 945460*(sin(Bk_rad)**6))));
    return sk42_x, sk42_y

def transform_latlon_wgs84_sk42(lat,lon, H, source='wgs84', target='sk42'):
    # Implemented according to ГОСТ 51794-2001 equations: 22,23
    Bd = lat 
    Ld = lon
    ro = 206264.8062
    a_kras = 6378245.0
    alP = 1 / 298.3
    e2P = 2 * alP - (alP ** 2)
    a_wgs84 = 6378137.0
    alW = 1 / 298.257223563
    e2W = 2 * alW - (alW ** 2)
    a = (a_kras + a_wgs84) / 2
    e2 = (e2P + e2W) / 2
    da = a_wgs84 - a_kras
    de2 = e2W - e2P
    
    # Manual calibrated by me (optimal for Caucasian area)
    dx = 24.0   #25+-2m
    dy = -143.9 #-141+-2m
    dz = -80.90 #-80+-3m
    wx = -0.00  #+-0.1
    wy = -0.35  #+-0.1
    wz = -0.82  #+-0.1
    ms = -0.12*0.000001  #+-0.25

    # EPSG:15865, Pulkovo 1942 to WGS 84 (best for Armenia, +-2m near the Georgian border)
    dx = 25.0
    dy = -141
    dz = -78.5
    wx = -0.00
    wy = -0.35
    wz = -0.736
    ms = 0
    
    B = Bd * pi / 180.0
    L = Ld * pi / 180.0
    M = a * (1 - e2) * (1 - e2 * sin(B)**2) ** -1.5
    N = a * (1 - e2 * sin(B) ** 2) ** -0.5
    dB = ro / (M + H) * (N / a * e2 * sin(B) * cos(B) * da + (N ** 2 / (a ** 2) + 1) * N * sin(B) * cos(B) * de2 / 2 - (dx * cos(L) + dy * sin(L)) * sin(B) + dz * cos(B)) - wx * sin(L) * (1 + e2 * cos(2 * B)) + wy * cos(L) * (1 + e2 * cos(2 * B)) - ro * ms * e2 * sin(B) * cos(B)
    dL = ro / ((N + H) * cos(B)) * (-dx * sin(L) + dy * cos(L)) + tan(B) * (1 - e2) * (wx * cos(L) + wy * sin(L)) - wz
    
    if source == 'wgs84' and target == 'sk42':
        lat = Bd - dB / 3600.0
        lon = Ld - dL / 3600.0
        return lat,lon
    elif source == 'sk42' and target == 'wgs84':
        lat = Bd + dB / 3600.0
        lon = Ld + dL / 3600.0
        return lat,lon
    else:
        return 0,0










