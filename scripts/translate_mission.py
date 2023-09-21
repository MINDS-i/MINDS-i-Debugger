#!/usr/bin/env python

import argparse
from bs4 import BeautifulSoup
import os
import lxml.etree as et

def to_gpx(filename):
    with open(filename, 'r') as f:
        kml = f.read()
    soup = BeautifulSoup(kml, 'xml')

    coordinates_text = soup.find('Placemark').find('LineString').find('coordinates').text.strip().split(' ')

    gpx = et.Element('gpx', version='1.1', creator='Custom')
    rte = et.SubElement(gpx, 'rte')
    for coordinate_text in coordinates_text:
        lon, lat, alt = coordinate_text.split(',')
        rtep = et.SubElement(rte, 'rtep', lat=lat, lng=lon)
        ele = et.SubElement(rtep, 'ele')
        ele.text = alt
    et.ElementTree(gpx).write(f'{os.path.splitext(filename)[0]}.gpx', pretty_print=True, encoding='utf-8', xml_declaration=True)

def to_kml(filename):
    with open(filename, 'r') as f:
        gpx = f.read()
    soup = BeautifulSoup(gpx, 'xml')

    gpx_coordinates = []
    rteps = soup.findAll('rtep')
    for rtep in rteps:
        gpx_coordinates.append(f"{rtep.get('lng')},{rtep.get('lat')},{rtep.find('ele').text}")

    namespaces = {None: 'http://www.opengis.net/kml/2.2',
                  'gx': 'http://www.google.com/kml/ext/2.2',
                  'kml': 'http://www.opengis.net/kml/2.2',
                  'atom': 'http://www.w3.org/2005/Atom'}
    kml = et.Element('kml', nsmap=namespaces)
    document = et.SubElement(kml, 'Document')
    name = et.SubElement(document, f'{os.path.splitext(os.path.basename(filename))[0]}.kml')
    style_map = et.SubElement(document, 'StyleMap', id='m_ylw-pushpin')
    pair = et.SubElement(style_map, 'Pair')
    key = et.SubElement(pair, 'key')
    key.text = 'normal'
    style_url = et.SubElement(pair, 'styleUrl')
    style_url.text = '#s_ylw-pushpin'
    pair = et.SubElement(style_map, 'Pair')
    key = et.SubElement(pair, 'key')
    key.text = 'highlight'
    style_url = et.SubElement(pair, 'styleUrl')
    style_url.text = '#s_ylw-pushpin_hl'
    style = et.SubElement(document, 'Style', id='s_ylw-pushpin')
    icon_style = et.SubElement(style, 'IconStyle')
    scale = et.SubElement(icon_style, 'scale')
    scale.text = '1.1'
    icon = et.SubElement(icon_style, 'Icon')
    href = et.SubElement(icon, 'href')
    href.text = 'http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png'
    hot_spot = et.SubElement(icon_style, 'hotSpot', x="20", y="2", x_units='pixels', yunits='pixels')
    icon_style = et.SubElement(style, 'IconStyle')
    scale = et.SubElement(icon_style, 'scale')
    scale.text = '1.3'
    icon = et.SubElement(icon_style, 'Icon')
    href = et.SubElement(icon, 'href')
    href.text = 'http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png'
    hot_spot = et.SubElement(icon_style, 'hotSpot', x="20", y="2", x_units='pixels', yunits='pixels')
    placemark = et.SubElement(document, 'Placemark')
    name = et.SubElement(placemark, 'name')
    name.text = os.path.splitext(os.path.basename(filename))[0]
    style_url = et.SubElement(placemark, 'styleUrl')
    style_url = '#m_ylw-pushpin</styleUrl'
    line_string = et.SubElement(placemark, 'LineString')
    tessellate = et.SubElement(line_string, 'tessellate')
    tessellate.text = '1'
    coordinates = et.SubElement(line_string, 'coordinates')
    coordinates.text = ' '.join(gpx_coordinates)

    et.ElementTree(kml).write(f'{os.path.splitext(filename)[0]}.kml', pretty_print=True, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = 'translate_mission',
        description = 'Translates kml mission file(s) (KML path from from google earth) to/from Minds-I dashboard mission file(s)')
    parser.add_argument('files', nargs='+', help='Input filename(s)')

    args = parser.parse_args()
    for filename in args.files:
        ext = os.path.splitext(filename)[1]
        if ext == '.kml':
            to_gpx(filename)
        elif ext == '.gpx':
            to_kml(filename)
        else:
            raise ValueError(f'Invalid file extension ({ext})')
