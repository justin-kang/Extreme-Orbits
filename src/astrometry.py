import math
import numpy as np
import astropy.constants
from celestialbody import CelestialBody
from position import projected_separation_com, position_angle_com

JD = 2451545.0
AU = astropy.constants.au.value
PC = astropy.constants.pc.value
PI = math.pi

# the change in RA and DEC caused by the planet's orbit
def _offsets_planet(dist, body_a, body_b, times):
    separations = np.array([])
    angles = np.array([])
    for time in times:
        separation = projected_separation_com(body_a, body_b, time, time)[2]
        separations = np.append(separations, separation)
        angle = position_angle_com(body_a, body_b, time, time)[2] * PI/180
        angles = np.append(angles, angle)
    d_ra = np.arctan(np.multiply(separations, np.sin(angles)) / dist)
    d_dec = np.arctan(np.multiply(separations, np.cos(angles)) / dist)
    index = separations.tolist().index(max(np.fabs(separations)))
    print(max(np.absolute(d_ra))*1000)
    print(max(np.absolute(d_dec))*1000)
    return d_ra * 1000, d_dec * 1000

# finds the equatorial pole
def _eq_pole(time):
    t = (time - JD) * 0.01
    t2 = t**2
    t3 = t**3
    return (84381.448 - 46.8150*t - 0.00059*t2 + 0.001813*t3) / 3600 * PI/180

# converts ecliptic coordinates to equatorial
def _ec_to_eq(lon, lat, time):
    ra = 0
    dec = 0
    x_ec = math.cos(lon) * math.cos(lat)
    y_ec = -math.sin(lon) * math.cos(lat)
    z_ec = math.sin(lat)
    pole = _eq_pole(time)
    x_eq = x_ec
    y_eq = math.sin(pole)*z_ec + math.cos(pole)*y_ec
    z_eq = math.cos(pole)*z_ec - math.sin(pole)*y_ec
    ra = math.atan2(-y_eq, x_eq) * 180 / PI
    while ra < 0:
        ra = ra + 360
    while ra > 360:
        ra = ra - 360
    if math.fabs(z_eq) > 1:
        dec = 90 * z_eq / math.fabs(z_eq)
        ra = 0
    else:
        dec = math.asin(z_eq) * 180 / PI
        if math.fabs(dec) >= 90:
            ra = 0
            if dec > 90:
                dec = 90
            if dec < -90:
                dec = -90
    return ra, dec

# converts equatorial coordinates to ecliptic
def _eq_to_ec(ra, dec, time):
    lat = 0
    lon = 0
    x_eq = math.cos(ra) * math.cos(dec)
    y_eq = -math.sin(ra) * math.cos(dec)
    z_eq = math.sin(dec)
    pole = _eq_pole(time)
    cosp = math.cos(pole)
    sinp = math.sin(pole)
    x_ec = x_eq
    y_ec = -math.sin(pole)*z_eq + math.cos(pole)*y_eq
    z_ec = math.cos(pole)*z_eq + math.sin(pole)*y_eq
    lon = math.atan2(-y_ec, x_ec) * 180/PI
    while lon < 0:
        lon = lon + 360
    while lon > 360:
        lon = lon - 360
    if math.fabs(z_ec) > 1:
        lat = 90 * z_ec / math.fabs(z_ec)
        lon = 0
    else:
        lat = math.asin(z_ec) * 180 / PI
        if math.fabs(lat) >= 90:
            lon = 0
            if lat > 90:
                lat = 90
            if lat < -90:
                lat = -90
    return lon, lat

# converts ecliptic coordinates to equatorial for many times
def _many_ec_to_eq(lon, lat, times):
    ra = np.array([])
    dec = np.array([])
    for idx, time in enumerate(times):
        rat, dect = _ec_to_eq(lon[idx], lat[idx], time)
        ra = np.append(ra, rat * PI/180)
        dec = np.append(dec, dect * PI/180)
    return ra, dec

# converts equatorial coordinates to ecliptic for many times
def _many_eq_to_ec(ra, dec, times):
    lon = np.array([])
    lat = np.array([])
    for time in times:
        lont, latt = _eq_to_ec(ra, dec, time)
        lon = np.append(lon, lont * PI/180)
        lat = np.append(lat, latt * PI/180)
    return lon, lat

# gives the sun's longitude wrt Earth for a given time
def _sun_longitude(times):
    d = times - JD
    mean_anomaly = 357.529 + 0.98560028 * d
    mean_longitude = 280.459 + 0.98564736 * d
    return (mean_longitude + 1.915 * np.sin(mean_anomaly * PI/180) + 
        0.020 * np.sin(2 * mean_anomaly * PI/180)) * PI/180

# the change in RA and DEC caused by parallax
def _offsets_parallax(ra, dec, dist, times):
    parallax = AU / (dist * PC)
    sun_lon = _sun_longitude(times)
    lon, lat = _many_eq_to_ec(ra, dec, times)
    dl = parallax * np.sin(sun_lon - lon) / np.cos(lat)
    db = -parallax * np.cos(sun_lon - lon) * np.sin(lat)
    new_ra, new_dec = _many_ec_to_eq(lon + dl, lat + db, times)
    return (new_ra - ra) * 180/PI * 60*60*1000, \
        (new_dec - dec) * 180/PI * 60*60*1000

# the change in RA and DEC caused by the star's proper motion
def _offsets_proper(m_ra, m_dec, times):
    return m_ra * (times - JD), m_dec * (times - JD)

# change in RA and DEC caused by planet in mas
def astrometry_planet(ra, dec, dist, body_a, body_b, times):
    return _offsets_planet(dist, body_a, body_b, times)

# change in RA and DEC caused by planet and parallax in mas
def astrometry_parallax(ra, dec, dist, body_a, body_b, times):
    # convert from degrees to radians
    ra = ra * PI/180
    dec = dec * PI/180
    ra_plan, dec_plan = astrometry_planet(dist, body_a, body_b, times)
    ra_par, dec_par = _offsets_parallax(ra, dec, dist, times)
    return ra_plan + ra_par, dec_plan + dec_par

# change in RA and DEC caused by planet, parallax, and proper motion in mas
def astrometry_proper(m_ra, m_dec, ra, dec, dist, body_a, body_b, times):
    # convert from degrees to radians
    ra = ra * PI/180
    dec = dec * PI/180
    # convert from mas/yr to mas/day
    m_ra = m_ra / 365
    m_dec = m_dec / 365
    ra_par, dec_par = astrometry_parallax(ra, dec, dist, times)
    ra_prop, dec_prop = _offsets_proper(m_ra, m_dec, times)
    return ra_par + ra_prop, dec_par + dec_prop