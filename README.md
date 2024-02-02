# cortran
Coordinate Translations library for WGS84 &lt;-> SK42


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

decimal   
places  degrees      N/S or E/W     E/W at         E/W at       E/W at
                     at equator     lat=23N/S      lat=45N/S    lat=67N/S
------- -------      ----------     ----------     ---------    ---------
0       1            111.32 km      102.47 km      78.71 km     43.496 km
1       0.1          11.132 km      10.247 km      7.871 km     4.3496 km
2       0.01         1.1132 km      1.0247 km      787.1 m      434.96 m
3       0.001        111.32 m       102.47 m       78.71 m      43.496 m
4       0.0001       11.132 m       10.247 m       7.871 m      4.3496 m
5       0.00001      1.1132 m       1.0247 m       787.1 mm     434.96 mm
6       0.000001     11.132 cm      102.47 mm      78.71 mm     43.496 mm
7       0.0000001    1.1132 cm      10.247 mm      7.871 mm     4.3496 mm
8       0.00000001   1.1132 mm      1.0247 mm      0.7871mm     0.43496mm



# LIST OF AVAILABLE CONVERSIONS
#       WGS84 Lat/Lon <-> SK42 Lat/Lon
#       SK42 Lat/Lon <-> SK42 XY
#       UTM <-> WGS84

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
*/ 

