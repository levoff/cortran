import math
from geopy.distance import distance
import pyproj

def haversine(coord1, coord2):
    R = 6378137.0  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2+math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))


cities = {
    'london': (51.5073219,  -0.1276474),
    'berlin': (52.5170365,  13.3888599),
    'vienna': (48.2083537,  16.3725042),
    'sydney': (-33.8548157, 151.2164539),
    'madrid': (40.4167047,  -3.7035825),  
    'yerevn': (40.1872000,  44.5152000),
    'shorja': (40.0718300,  45.8897700),
    'gyumri': (40.7929000,  43.8465000) 
}



# geod = pyproj.Geod('+a=6378137 +f=0.0033528106647475126')
geod = pyproj.Geod(ellps='WGS84')

initial_point = cities['yerevn']

print('Point\t\tHaver\t\tDiff\t\tPyProj\t\tGeoPy\tAzimuth(PyProj)')

for city, coord in cities.items():
    lat0, lon0 = initial_point
    lat1, lon1 = coord
    dist_haver = haversine(initial_point, coord)
    dist_geopy = distance(initial_point, coord)
    azimuth, azimuth_back, dist_pyproj = geod.inv(lon0, lat0, lon1, lat1)

    print(city.ljust(10), 
                str(round(dist_haver/1000, 3)).ljust(10),
                str(round(dist_haver - dist_pyproj, 3)).ljust(10), 
                str(round(dist_pyproj/1000, 3)).ljust(10),
                str(round(dist_geopy.km, 3)).ljust(10), 
                'azimuths:', str(round(azimuth,1)), str(round(azimuth_back,1)))

