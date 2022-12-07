# LINKS:
    # https://www.movable-type.co.uk/scripts/latlong-utm-mgrs.html
    # https://ru.wikibooks.org/wiki/Реализации_алгоритмов/Перевод_географических_координат_в_прямоугольные_в_прямоугольные_координаты_проекции_Гаусса-Крюгера
    # https://gis-lab.info/qa/wgs84-sk42-wgs84-formula.html
    # https://en.wikipedia.org/wiki/Geographic_coordinate_conversion
    # https://epsg.io/transform#s_srs=4326&t_srs=28408&x=45.7324520&y=39.8704700
    # https://epsg.io/transform#s_srs=4326&t_srs=4284&x=45.7324520&y=39.8704700
    # https://epsg.io/srs/transform/45.732452,39.87047.json?key=default&s_srs=4326&t_srs=4284
    # https://epsg.io/srs/transform/45.732452,39.87047.json?key=default&s_srs=4326&t_srs=28408
    # https://github.com/Wrussia/CoordinatesConvertor
    # https://github.com/dvonck/datumfitter/blob/master/FitTransfrom.py
    # https://fypandroid.wordpress.com/2011/09/03/converting-utm-to-latitude-and-longitude-or-vice-versa/
    # https://gis.stackexchange.com/questions/147425/formula-to-convert-from-wgs-84-utm-zone-34n-to-wgs-84
    # https://www.ccgalberta.com/ccgresources/report11/2009-410_converting_latlon_to_utm.pdf
    # https://esurveying.net/free-software/utm-latitude-longitude-conversion
    # https://gis-lab.info/qa/wgs84-sk42-wgs84-formula.html
    # zone = int(lon/6.0+1)

# Approximate Metric Equivalents for Degrees, Minutes, and Seconds
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

# EPSG codes:
    # EPSG 4326 - WGS84 Ellipsoidal 2D CS. Axes: latitude, longitude. Orientations: north, east. UoM: degree
    # EPSG 4979 - Ellipsoidal 3D CS. Axes: latitude, longitude, ellipsoidal height. Orientations: north, east, up. UoM: degree, degree, metre.
    # EPSG 4284 - SK42 Ellipsoidal 2D CS. Axes: latitude, longitude. Orientations: north, east. UoM: degree
    # EPSG 28408 - SK42 Cartesian 2D CS. Axes: northing, easting (X,Y). Orientations: north, east. UoM: m.
    # EPSG 32638 - MGRS Cartesian 2D CS. Axes: easting, northing (E,N). Orientations: east, north. UoM: m. WGS 84 / UTM zone 38N





from cortran import *

# Ref points for precision test: longitude,latitude
points = [
# [43.005981,41.335576],
# [43.505859,41.339700],
# [44.005737,41.339700],
# [44.505615,41.339700],
# [45.005493,41.331451],
# [45.505371,41.339700],
# [45.999756,41.339700],
# [46.505127,41.335576],
[43.001862,41.167283],
[43.501740,41.167283],
[44.001617,41.167283],
[44.502869,41.167283],
[45.001373,41.168317],
[45.502625,41.168317],
[46.001129,41.166249],
[46.501007,41.166249],
[43.005981,41.000630],
[43.500023,41.000500],
[44.000244,41.000630],
[44.502869,41.004775],
[45.002747,41.004775],
[45.505371,41.002703],
[46.005249,41.006848],
[46.501007,41.000889],
[43.005981,40.672306],
[43.505859,40.668140],
[44.005737,40.672306],
[44.511108,40.672306],
[45.010986,40.672306],
[45.505371,40.672306],
[46.010742,40.672306],
[46.510620,40.672306],
[43.000488,40.338170],
[43.505859,40.338170],
[44.011230,40.342357],
[44.505615,40.342357],
[45.010986,40.346544],
[45.505371,40.350731],
[46.005249,40.342357],
[46.499634,40.346544],
[43.005981,39.998164],
[43.505859,40.006580],
[44.011230,40.002372],
[44.505615,40.006580],
[45.010986,40.002372],
[45.505371,40.010787],
[46.005249,40.006580],
[46.510620,40.010787],
[44.011230,39.669142],
[44.516602,39.664914],
[45.010986,39.673370],
[45.510864,39.664914],
[45.999756,39.673370],
[46.499634,39.673370],
[47.010498,39.677598],
[47.510376,39.673370],
[44.505615,39.334297],
[45.010986,39.342794],
[45.505371,39.338546],
[46.016235,39.342794],
[46.505127,39.351290],
[47.010498,39.347043],
[47.510376,39.338546],
[45.505371,39.006379],
[46.010742,39.010648],
[46.501694,39.001043],
[47.002258,38.997841],
[46.005249,38.666212],
[46.507874,38.668356],
[47.007751,38.668356]]



def epsg_convert(lat,lon, source=4326, target=4284, online=True):
    if online:
        import requests
        # source - Input coordinate system as EPSG code
        # target - Output coordinate system as EPSG code
        # EPSG 4326 - WGS84 Ellipsoidal 2D CS. Axes: latitude, longitude. Orientations: north, east. UoM: degree
        # EPSG 4979 - Ellipsoidal 3D CS. Axes: latitude, longitude, ellipsoidal height. Orientations: north, east, up. UoM: degree, degree, metre.
        # EPSG 4284 - SK42 Ellipsoidal 2D CS. Axes: latitude, longitude. Orientations: north, east. UoM: degree
        # EPSG 28408 - SK42 Cartesian 2D CS. Axes: northing, easting (X,Y). Orientations: north, east. UoM: m.
        # EPSG 32638 - MGRS Cartesian 2D CS. Axes: easting, northing (E,N). Orientations: east, north. UoM: m. WGS 84 / UTM zone 38N
        x = requests.get(f'https://epsg.io/srs/transform/{lon},{lat}.json?key=default&s_srs={source}&t_srs={target}')
        return x.json().get('results')[0].get('y'), x.json().get('results')[0].get('x')
    
    else:
        # Offline conversion using pyproj library
        from pyproj import Transformer
        transformer = Transformer.from_crs(f"epsg:{source}", f"epsg:{target}",always_xy=False)
        x, y = transformer.transform(lat,lon)

        # THIS IS SLOW ON WEAK PROCESSORS
        # import pyproj
        # p = pyproj.Proj('+proj=tmerc +lat_0=0 +lon_0=45 +k=1 +x_0=8500000 +y_0=0 +ellps=krass +towgs84=25,-141,-78.5,0,0.35,0.736,0 +units=m +no_defs')
        # x, y = p(lat,lon, inverse=True)

        return x,y

def test_reference_points(online=False):
    n=0
    xd=0
    yd=0
    for p in points:
        xy1 = epsg_convert(p[1], p[0], source=4326, target=28408, online=online)
        latsk42, lonsk42 = sk42xy_to_sk42latlon(xy1[0], xy1[1])
        latwgs84, lonwgs84 = transform_latlon_wgs84_sk42(latsk42, lonsk42, 1000, source='sk42', target='wgs84')
        xy2 = epsg_convert(latwgs84, lonwgs84, source=4326, target=28408, online=online)
        dx = xy1[0] - xy2[0]
        dy = xy1[1] - xy2[1]
        # print(xy1)
        # print(xy2)
        # print('%.6f, %.6f'%(p[1], p[0]))
        # print('%.6f, %.6f'%(latwgs84, lonwgs84))
        print(f'p{n+1}',dx,dy)
        # print(xy1)
        # print(xy2)
        xd=xd+dx
        yd=yd+dy
        n=n+1

    print('X error:',round(xd/len(points)*100,1), 'cm')
    print('Y error:',round(yd/len(points)*100,1), 'cm')

def test_wgs_to_sk_to_xy_to_sk_to_wgs_online():
    for p in points[:1]:
        print(p[1], p[0])
        # 1
        sk42_ll = epsg_convert(p[1], p[0], source=4326, target=4284, online=True)
        print(sk42_ll)
        # 2
        sk42_xy = epsg_convert(sk42_ll[0], sk42_ll[1], source=4284, target=28408, online=True)
        print(sk42_xy)
        # 3
        sk42_ll = epsg_convert(sk42_xy[0], sk42_xy[1], source=28408, target=4284, online=True)
        print(sk42_ll)
        # 4
        wgs84_ll= epsg_convert(sk42_ll[0], sk42_ll[1], source=4284, target=4326, online=True)
        print(wgs84_ll)
        # 5
        sk42_xy1= epsg_convert(wgs84_ll[0], wgs84_ll[1], source=4326, target=28408, online=True)
        print(sk42_xy1, '\n-------')
        print(sk42_xy1[0]-sk42_xy[0])

def test_wgs_to_sk_to_xy_to_sk_to_wgs_offline():
    for p in points[:1]:
        print(p[1], p[0])
        # 1
        sk42_ll = transform_latlon_wgs84_sk42(p[1], p[0], 1000, source='wgs84', target='sk42')
        print(sk42_ll)
        # 2
        sk42_xy = epsg_convert(sk42_ll[0], sk42_ll[1], source=4284, target=28408, online=True)
        print(sk42_xy)
        # 3
        sk42_ll = epsg_convert(sk42_xy[0], sk42_xy[1], source=28408, target=4284, online=True)
        print(sk42_ll)
        # 4
        wgs84_ll= epsg_convert(sk42_ll[0], sk42_ll[1], source=4284, target=4326, online=True)
        print(wgs84_ll)
        # 5
        sk42_xy1= epsg_convert(wgs84_ll[0], wgs84_ll[1], source=4326, target=28408, online=True)
        print(sk42_xy1)
        print(sk42_xy1[0]-sk42_xy[0])



test_reference_points(online=True)
test_wgs_to_sk_to_xy_to_sk_to_wgs_online()
test_wgs_to_sk_to_xy_to_sk_to_wgs_offline()





