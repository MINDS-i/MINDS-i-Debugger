import math

import numpy as np


def wgs84_to_local_xy(lat, lon, lat0, lon0, alt0=0.0):
    '''Convert  WGS84 lat/lon values into a local cartesian frame

    Args:
        lat (float): Latitude of point (or array of points) to convert
        lon (float): Longitude of point (or array of points) to convert
        lat0 (float): Local origin latitude
        lon0 (float): Local origin longitude
        alt0 (float): Local origin altitude. If altitude is unknown, it
                      is okay to use the default, as it only contributes
                      a small amount to the precision

    Returns:
        (x, y): Corresponding local x,y coordinates of the input
                coordinates. Note that these will be arrays if input
                lats and lons are arrays.
    '''
    lat = np.array(lat)
    lon = np.array(lon)
    earth_eccentricity = 0.08181919084261
    earth_equator_radius = 6378137.0
    reference_latitude = lat0 * math.pi / 180.0
    reference_longitude = lon0 * math.pi / 180.0
    reference_heading=0.0
    cos_heading = math.cos(reference_heading)
    sin_heading = math.sin(reference_heading)

    depth = -alt0

    p = earth_eccentricity * math.sin(reference_latitude)
    p = 1.0 - np.multiply(p, p)

    rho_e_num = earth_equator_radius * (1.0 - earth_eccentricity * earth_eccentricity)
    rho_e_den = np.multiply(np.sqrt(p), p)
    rho_e = np.divide(rho_e_num, rho_e_den)
    rho_n = np.divide(earth_equator_radius, np.sqrt(p))

    rho_lat = rho_e - depth
    rho_lon = (rho_n - depth) * np.cos(reference_latitude)

    rlat = lat * math.pi / 180
    rlon = lon * math.pi / 180
    dlat = (rlat - reference_latitude) * rho_lat
    dlon = (rlon - reference_longitude) * rho_lon

    y = dlat * cos_heading + dlon * sin_heading
    x = -1.0 * (dlat * sin_heading - dlon * cos_heading)

    return x, y


def local_xy_to_wgs84(x, y, lat0, lon0, alt0=0.0):
    '''Convert  local x/y cartesian points into WGS84 coordinates

    Args:
        x (float): Local x coordinate of point (or array of points)
        y (float): Local x coordinate of point (or array of points)
        lat0 (float): Local origin latitude
        lon0 (float): Local origin longitude
        alt0 (float): Local origin altitude. If altitude is unknown, it
                      is okay to use the default, as it only contributes
                      a small amount to the precision

    Returns:
        (lat, lon): Corresponding local x,y coordinates of the input
                    coordinates. Note that these will be arrays if
                    input x and y coordinates are arrays.
    '''

    x = np.array(x)
    y = np.array(y)
    earth_eccentricity = 0.08181919084261
    earth_equator_radius = 6378137.0
    reference_heading = 0.0
    reference_latitude = lat0 * math.pi / 180.0
    reference_longitude = lon0 * math.pi / 180.0
    cos_heading = math.cos(reference_heading)
    sin_heading = math.sin(reference_heading)

    depth = -alt0

    p = earth_eccentricity * math.sin(reference_latitude)
    p = 1.0 - np.multiply(p, p)

    rho_e_num = earth_equator_radius * (1.0 - earth_eccentricity * earth_eccentricity)
    rho_e_den = np.multiply(np.sqrt(p), p)
    rho_e = np.divide(rho_e_num, rho_e_den)
    rho_n = np.divide(earth_equator_radius, np.sqrt(p))

    rho_lat = rho_e - depth
    rho_lon = (rho_n - depth) * np.cos(reference_latitude)

    dLon = cos_heading * x - sin_heading * y
    dLat = sin_heading * x + cos_heading * y
    rlat = (dLat / rho_lat) + reference_latitude
    rlon = (dLon / rho_lon) + reference_longitude

    latitude = rlat * 180.0 / math.pi
    longitude = rlon * 180.0 / math.pi

    return latitude, longitude
