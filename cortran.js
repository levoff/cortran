/*
# Library to convert between WGS84 Lat/Lon and SK42 Lat/Lon and/or XY
# Maintained at https://github.com/levoff/cortran
# 
# License:
# 
# Copyright (c) 2020-2023 Levon Hovhannisyan
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


function sk42xy_to_sk42latlon(x, y) {
    // Implemented according to ГОСТ 51794-2001 equations: 29,30,31,32,33,34,35,36
    const n = Math.floor(y * 0.000001);
    const b = x/6367558.4968;
    const B0 = b + Math.sin(2*b) * (0.00252588685 - 0.00001491860 * (Math.sin(b)**2) + 0.00000011904 * (Math.sin(b)**4));
    const z0 = (y - (10*n + 5)*100000)/(6378245.0 * Math.cos(B0));
    const B = B0 - (z0**2) * Math.sin(2*B0) * (0.251684631 - 0.003369263*(Math.sin(B0)**2) + 0.000011276*(Math.sin(B0)**4) 
         -(z0**2) * (0.10500614 - 0.04559916*Math.sin(B0)**2 + 0.00228901*Math.sin(B0)**4 - 0.00002987*Math.sin(B0)**6
         -(z0**2) * (0.042858 - 0.025318*Math.sin(B0)**2 + 0.014346*Math.sin(B0)**4 - 0.001264*Math.sin(B0)**6
         -(z0**2) * (0.01672 - 0.00630*Math.sin(B0)**2 + 0.01188*Math.sin(B0)**4 - 0.00328*Math.sin(B0)**6))));

    const L = 6 * (n - 0.5)/57.29577951 + (z0**1) * (1 - 0.0033467108*Math.sin(B0)**2 - 0.0000056002*Math.sin(B0)**4 - 0.0000000187*Math.sin(B0)**6
        -(z0**2) * (0.16778975 + 0.16273586*Math.sin(B0)**2 - 0.00052490*Math.sin(B0)**4 - 0.00000846*Math.sin(B0)**6
        -(z0**2) * (0.0420025 + 0.1487407*Math.sin(B0)**2 - 0.0059420*Math.sin(B0)**4 - 0.0000150*Math.sin(B0)**6
        -(z0**2) * (0.01225 + 0.09477*Math.sin(B0)**2 - 0.03282*Math.sin(B0)**4 - 0.00034*Math.sin(B0)**6
        -(z0**2) * (0.0038 + 0.0524*Math.sin(B0)**2 - 0.0482*Math.sin(B0)**4 - 0.0032*Math.sin(B0)**6)))));
    const lon = L*180/Math.PI;
    const lat = B*180/Math.PI;
    return [lat,lon];
}

function sk42latlon_to_sk42xy(lat, lon) {
    // Implemented according to ГОСТ 51794-2001
    const rad = 0.0174533;
    const Bk = lat;
    const Lk = lon;
    const Bk_rad = Bk * rad;
    // Lk_rad =  Lk*rad
    const n = Math.floor((Lk + 6) / 6);
    const l = (Lk - Math.abs(3 + 6 * (n - 1))) / 57.29577951;
    const sk42_x = 6367558.4968 * Bk_rad - Math.sin(2 * Bk_rad) * (16002.8900 + 66.9607 * Math.pow(Math.sin(Bk_rad), 2) + 0.3515 * Math.pow(Math.sin(Bk_rad), 4) - Math.pow(l, 2) * (1594561.25 + 5336.535 * Math.pow(Math.sin(Bk_rad), 2) + 26.790 * Math.pow(Math.sin(Bk_rad), 4) + 0.149 * Math.pow(Math.sin(Bk_rad), 6) + Math.pow(l, 2) * (672483.4 - 811219.9 * Math.pow(Math.sin(Bk_rad), 2) + 5420.0 * Math.pow(Math.sin(Bk_rad), 4) - 10.6 * Math.pow(Math.sin(Bk_rad), 6) + Math.pow(l, 2) * (278194 - 830174 * Math.pow(Math.sin(Bk_rad), 2) + 572434 * Math.pow(Math.sin(Bk_rad), 4) - 16010 * Math.pow(Math.sin(Bk_rad), 6)))));
    const sk42_y = (5 + 10 * n) * 100000 + l * Math.cos(Bk_rad) * (6378245 + 21346.1415 * Math.pow(Math.sin(Bk_rad), 2) + 107.1590 * Math.pow(Math.sin(Bk_rad), 4) + 0.5977 * Math.pow(Math.sin(Bk_rad), 6) + Math.pow(l, 2) * (1070204.16 - 2136826.66 * Math.pow(Math.sin(Bk_rad), 2) + 17.98 * Math.pow(Math.sin(Bk_rad), 4) - 11.99 * Math.pow(Math.sin(Bk_rad), 6)) + Math.pow(l, 2) * (270806 - 1523417 * Math.pow(Math.sin(Bk_rad), 2) + 1327645 * Math.pow(Math.sin(Bk_rad), 4) - 21701 * Math.pow(Math.sin(Bk_rad), 6) + Math.pow(l, 2) * (79690 - 866190 * Math.pow(Math.sin(Bk_rad), 2) + 1730360 * Math.pow(Math.sin(Bk_rad), 4) - 945460 * Math.pow(Math.sin(Bk_rad), 6))));
    return [sk42_x, sk42_y];
}




function transform_latlon_wgs84_sk42(lat, lon, H, source='wgs84', target='sk42') {
  // Implemented according to ГОСТ 51794-2001 equations: 22,23
  const pi = Math.PI;
  const Bd = lat;
  const Ld = lon;
  const ro = 206264.8062;
  const a_kras = 6378245.0;
  const alP = 1 / 298.3;
  const e2P = 2 * alP - (alP ** 2);
  const a_wgs84 = 6378137.0;
  const alW = 1 / 298.257223563;
  const e2W = 2 * alW - (alW ** 2);
  const a = (a_kras + a_wgs84) / 2;
  const e2 = (e2P + e2W) / 2;
  const da = a_wgs84 - a_kras;
  const de2 = e2W - e2P;

  // Manual calibrated by me (optimal for Caucasian area)
  let dx = 24.0;   //25+-2m
  let dy = -143.9; //-141+-2m
  let dz = -80.90; //-80+-3m
  let wx = -0.00;  //+-0.1
  let wy = -0.35;  //+-0.1
  let wz = -0.82;  //+-0.1
  let ms = -0.12*0.000001;  //+-0.25

  // EPSG:15865, Pulkovo 1942 to WGS 84 (best for Armenia, +-2m near the Georgian border)
  dx = 25.0;
  dy = -141;
  dz = -78.5;
  wx = -0.00;
  wy = -0.35;
  wz = -0.736;
  ms = 0;
  
  let B = Bd * pi / 180.0;
  let L = Ld * pi / 180.0;
  let M = a * (1 - e2) * (1 - e2 * Math.sin(B)**2) ** -1.5;
  let N = a * (1 - e2 * Math.sin(B) ** 2) ** -0.5;
  let dB = ro / (M + H) * (N / a * e2 * Math.sin(B) * Math.cos(B) * da + (N ** 2 / (a ** 2) + 1) * N * Math.sin(B) * Math.cos(B) * de2 / 2 - (dx * Math.cos(L) + dy * Math.sin(L)) * Math.sin(B) + dz * Math.cos(B)) - wx * Math.sin(L) * (1 + e2 * Math.cos(2 * B)) + wy * Math.cos(L) * (1 + e2 * Math.cos(2 * B)) - ro * ms * e2 * Math.sin(B) * Math.cos(B);
  let dL = ro / ((N + H) * Math.cos(B)) * (-dx * Math.sin(L) + dy * Math.cos(L)) + Math.tan(B) * (1 - e2) * (wx * Math.cos(L) + wy * Math.sin(L)) - wz;


  if (source === 'wgs84' && target === 'sk42') {
    let lat = Bd - dB / 3600.0;
    let lon = Ld - dL / 3600.0;
    return [lat, lon];
  } else if (source === 'sk42' && target === 'wgs84') {
    let lat = Bd + dB / 3600.0;
    let lon = Ld + dL / 3600.0;
    return [lat, lon];
  } else {
    return [0, 0];
  }

}


// https://github.com/TimothyGu/utm
// 'use strict'

// Check this link for more accurate conversion
// https://gis.stackexchange.com/questions/147425/formula-to-convert-from-wgs-84-utm-zone-34n-to-wgs-84/278112#278112

var K0 = 0.9996;

var E = 0.00669438;
var E2 = Math.pow(E, 2);
var E3 = Math.pow(E, 3);
var E_P2 = E / (1 - E);

var SQRT_E = Math.sqrt(1 - E);
var _E = (1 - SQRT_E) / (1 + SQRT_E);
var _E2 = Math.pow(_E, 2);
var _E3 = Math.pow(_E, 3);
var _E4 = Math.pow(_E, 4);
var _E5 = Math.pow(_E, 5);

var M1 = 1 - E / 4 - 3 * E2 / 64 - 5 * E3 / 256;
var M2 = 3 * E / 8 + 3 * E2 / 32 + 45 * E3 / 1024;
var M3 = 15 * E2 / 256 + 45 * E3 / 1024;
var M4 = 35 * E3 / 3072;

var P2 = 3 / 2 * _E - 27 / 32 * _E3 + 269 / 512 * _E5;
var P3 = 21 / 16 * _E2 - 55 / 32 * _E4;
var P4 = 151 / 96 * _E3 - 417 / 128 * _E5;
var P5 = 1097 / 512 * _E4;

var R = 6378137;

var ZONE_LETTERS = 'CDEFGHJKLMNPQRSTUVWXX';

function utm_to_wgs84(easting, northing, zoneNum, zoneLetter, northern, strict) {
  strict = strict !== undefined ? strict : true;

  if (!zoneLetter && northern === undefined) {
    throw new Error('either zoneLetter or northern needs to be set');
  } else if (zoneLetter && northern !== undefined) {
    throw new Error('set either zoneLetter or northern, but not both');
  }

  if (strict) {
    if (easting < 100000 || 1000000 <= easting) {
      throw new RangeError('easting out of range (must be between 100 000 m and 999 999 m)');
    }
    if (northing < 0 || northing > 10000000) {
      throw new RangeError('northing out of range (must be between 0 m and 10 000 000 m)');
    }
  }
  if (zoneNum < 1 || zoneNum > 60) {
    throw new RangeError('zone number out of range (must be between 1 and 60)');
  }
  if (zoneLetter) {
    zoneLetter = zoneLetter.toUpperCase();
    if (zoneLetter.length !== 1 || ZONE_LETTERS.indexOf(zoneLetter) === -1) {
      throw new RangeError('zone letter out of range (must be between C and X)');
    }
    northern = zoneLetter >= 'N';
  }

  var x = easting - 500000;
  var y = northing;

  if (!northern) y -= 1e7;

  var m = y / K0;
  var mu = m / (R * M1);

  var pRad = mu +
             P2 * Math.sin(2 * mu) +
             P3 * Math.sin(4 * mu) +
             P4 * Math.sin(6 * mu) +
             P5 * Math.sin(8 * mu);

  var pSin = Math.sin(pRad);
  var pSin2 = Math.pow(pSin, 2);

  var pCos = Math.cos(pRad);

  var pTan = Math.tan(pRad);
  var pTan2 = Math.pow(pTan, 2);
  var pTan4 = Math.pow(pTan, 4);

  var epSin = 1 - E * pSin2;
  var epSinSqrt = Math.sqrt(epSin);

  var n = R / epSinSqrt;
  var r = (1 - E) / epSin;

  var c = _E * pCos * pCos;
  var c2 = c * c;

  var d = x / (n * K0);
  var d2 = Math.pow(d, 2);
  var d3 = Math.pow(d, 3);
  var d4 = Math.pow(d, 4);
  var d5 = Math.pow(d, 5);
  var d6 = Math.pow(d, 6);

  var latitude = pRad - (pTan / r) *
                 (d2 / 2 -
                  d4 / 24 * (5 + 3 * pTan2 + 10 * c - 4 * c2 - 9 * E_P2)) +
                  d6 / 720 * (61 + 90 * pTan2 + 298 * c + 45 * pTan4 - 252 * E_P2 - 3 * c2);
  var longitude = (d -
                   d3 / 6 * (1 + 2 * pTan2 + c) +
                   d5 / 120 * (5 - 2 * c + 28 * pTan2 - 3 * c2 + 8 * E_P2 + 24 * pTan4)) / pCos;

  return {
    lat: toDegrees(latitude),
    lon: toDegrees(longitude) + zoneNumberToCentralLongitude(zoneNum)
  };
}

function wgs84_to_utm(latitude, longitude, forceZoneNum) {
  if (latitude > 84 || latitude < -80) {
    throw new RangeError('latitude out of range (must be between 80 deg S and 84 deg N)');
  }
  if (longitude > 180 || longitude < -180) {
    throw new RangeError('longitude out of range (must be between 180 deg W and 180 deg E)');
  }

  var latRad = toRadians(latitude);
  var latSin = Math.sin(latRad);
  var latCos = Math.cos(latRad);

  var latTan = Math.tan(latRad);
  var latTan2 = Math.pow(latTan, 2);
  var latTan4 = Math.pow(latTan, 4);

  var zoneNum;

  if (forceZoneNum === undefined) {
    zoneNum = latLonToZoneNumber(latitude, longitude);
  } else {
    zoneNum = forceZoneNum;
  }

  var zoneLetter = latitudeToZoneLetter(latitude);

  var lonRad = toRadians(longitude);
  var centralLon = zoneNumberToCentralLongitude(zoneNum);
  var centralLonRad = toRadians(centralLon);

  var n = R / Math.sqrt(1 - E * latSin * latSin);
  var c = E_P2 * latCos * latCos;

  var a = latCos * (lonRad - centralLonRad);
  var a2 = Math.pow(a, 2);
  var a3 = Math.pow(a, 3);
  var a4 = Math.pow(a, 4);
  var a5 = Math.pow(a, 5);
  var a6 = Math.pow(a, 6);

  var m = R * (M1 * latRad -
               M2 * Math.sin(2 * latRad) +
               M3 * Math.sin(4 * latRad) -
               M4 * Math.sin(6 * latRad));
  var easting = K0 * n * (a +
                          a3 / 6 * (1 - latTan2 + c) +
                          a5 / 120 * (5 - 18 * latTan2 + latTan4 + 72 * c - 58 * E_P2)) + 500000;
  var northing = K0 * (m + n * latTan * (a2 / 2 +
                                         a4 / 24 * (5 - latTan2 + 9 * c + 4 * c * c) +
                                         a6 / 720 * (61 - 58 * latTan2 + latTan4 + 600 * c - 330 * E_P2)));
  if (latitude < 0) northing += 1e7;

  return {
    easting: easting,
    northing: northing,
    zoneNum: zoneNum,
    zoneLetter: zoneLetter
  };
}

function latitudeToZoneLetter(latitude) {
  if (-80 <= latitude && latitude <= 84) {
    return ZONE_LETTERS[Math.floor((latitude + 80) / 8)];
  } else {
    return null;
  }
}

function latLonToZoneNumber(latitude, longitude) {
  if (56 <= latitude && latitude < 64 && 3 <= longitude && longitude < 12) return 32;

  if (72 <= latitude && latitude <= 84 && longitude >= 0) {
    if (longitude <  9) return 31;
    if (longitude < 21) return 33;
    if (longitude < 33) return 35;
    if (longitude < 42) return 37;
  }

  return Math.floor((longitude + 180) / 6) + 1;
}

function zoneNumberToCentralLongitude(zoneNum) {
  return (zoneNum - 1) * 6 - 180 + 3;
}

function toDegrees(rad) {
  return rad / Math.PI * 180;
}

function toRadians(deg) {
  return deg * Math.PI / 180;
}

// console.log(sk42xy_to_sk42latlon(4429609, 8500000));
// console.log(sk42latlon_to_sk42xy(40.0, 45.0));
// console.log(transform_latlon_wgs84_sk42(40.0, 45.0, 0, 'sk42', 'wgs84'));


export {
    sk42xy_to_sk42latlon,
    sk42latlon_to_sk42xy,
    transform_latlon_wgs84_sk42,
    wgs84_to_utm,
    utm_to_wgs84
};

