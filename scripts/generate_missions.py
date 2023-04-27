#!/usr/bin/env python

import argparse
import os
import lxml.etree as et
import wgs84_transform_util as wtu
import yaml

def create_gpx(filename, prepend, lat0, lon0, reference_heading):
    with open(filename, 'r') as f:
        wpts = yaml.safe_load(f)['waypoints']
    
    lats, lons = wtu.local_xy_to_wgs84([w['x'] for w in wpts], [w['y'] for w in wpts],
                                       lat0=lat0, lon0=lon0, reference_heading=reference_heading)
    alts = [w['z'] for w in wpts]

    gpx = et.Element('gpx', version='1.1', creator='Custom')
    rte = et.SubElement(gpx, 'rte')
    for lat, lon, alt in zip(lats, lons, alts):
        rtep = et.SubElement(rte, 'rtep', lat=str(lat), lng=str(lon))
        ele = et.SubElement(rtep, 'ele')
        ele.text = str(alt)
    
    outfile = os.path.join(
        os.path.dirname(filename),
        f'{prepend}_{os.path.splitext(os.path.basename(filename))[0]}.gpx') 
    et.ElementTree(gpx).write(outfile, pretty_print=True, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = 'translate_mission',
        description = 'Translates kml mission file(s) (KML path from from google earth) to/from Minds-I dashboard mission file(s)')
    parser.add_argument('lat0', help='Starting latitude')
    parser.add_argument('lon0', help='Starting longitude')
    parser.add_argument('reference_heading', help='Reference Heading')
    parser.add_argument('files', nargs='+', help='Input filename(s)')
    parser.add_argument('--prepend', help='String to prepend output filename(s)', default='')

    args = parser.parse_args()
    for filename in args.files:
        create_gpx(filename, prepend=args.prepend,
                   lat0=float(args.lat0), lon0=float(args.lon0), reference_heading=float(args.reference_heading))
