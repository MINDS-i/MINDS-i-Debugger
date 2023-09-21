#!/usr/bin/env python 

import argparse
import simplekml
import matplotlib.pyplot as plt
import data_decoder

def main():    
    parser = argparse.ArgumentParser(description="Create a KML files from a rover log. Each KML will be \
        saved as an individual file in the local directory.")
    parser.add_argument("filepath")
    parser.add_argument('-a','--all',action='store_true',help='Create all available KML files. Default if no options are given.')
    parser.add_argument('--gps_path',action='store_true',help='Create a KML showing the GPS path of the rover.')    
    parser.add_argument('--gps_points',action='store_true',help='Create a KML of the rover\'s GPS points.')    
    parser.add_argument('--extrapolated',action='store_true',help='Create a KML of the software extraploated GPS points.')    
    parser.add_argument('--rover_heading_pts',action='store_true',help='Create a KML of the rover\'s heading at each of its GPS points.')    
    parser.add_argument('--path_heading_pts',action='store_true',help='Create a KML of the rover\'s desired heading (towards next goal point) at each of its GPS points.')
    parser.add_argument('--intermediate_pts',action='store_true',help='Create a KML of all intermediate (goal) points created by the line-gravity algorithm.')

    args = parser.parse_args()

    # if no specific output option is request then all ouput options will be completed
    if not (args.all or args.gps_path or args.gps_points or args.extrapolated or args.rover_heading_pts or args.path_heading_pts or args.intermediate_pts):
        args.all = True

    # Create a KML file for path data
    if args.all == True or args.gps_path:
        kml_path = simplekml.Kml()

        ls = kml_path.newlinestring(name='rover_path')
        ls.extrude = 1
        ls.altitudedmode = simplekml.AltitudeMode.relativetoground
        ls.style.linestyle.width = 4
        ls.style.linestyle.color = simplekml.Color.yellow

        old_lat = ''
        old_lon = ''    
        points = []
        with open(args.filepath) as fp:
            cnt = 0
            for line in fp:
                msg_str, msg = data_decoder.read_log_dataline(line)
                if msg_str.split('Stamped')[-1] == 'RawPosition' and (old_lat != msg.latitude or old_lon != msg.longitude):
                    cnt += 1
                    points.append((msg.longitude, msg.latitude))
                    old_lat = msg.latitude
                    old_lon = msg.longitude

        ls.coords = points
        kml_path.save(args.filepath.rsplit(".",1)[0] + "_path.kml")

    # Create a KML file for GPS points data
    if args.all == True or args.gps_points:
        kml_points = simplekml.Kml()
        old_lat = ''
        old_lon = ''    
        with open(args.filepath) as fp:
            cnt = 0
            for line in fp:
                msg_str, msg = data_decoder.read_log_dataline(line)
                if msg_str.split('Stamped')[-1] == 'RawPosition' and (old_lat != msg.latitude or old_lon != msg.longitude):
                    cnt += 1
                    kml_points.newpoint(name=f"P{str(cnt)}", coords=[(msg.longitude, msg.latitude)])
                    old_lat = msg.latitude
                    old_lon = msg.longitude
        kml_points.save(args.filepath.rsplit(".",1)[0] + "_points.kml")

    # Create a KML file for extrapolated points
    if args.all == True or args.extrapolated:
        kml_extrap = simplekml.Kml()

        old_lat = ''
        old_lon = ''    
        old_e_lat = ''
        old_e_lon = ''    
        with open(args.filepath) as fp:
            cnt = 0
            cnt2 = 0
            cnt3 = 0
            cnt4 = 0
            cnt5 = 0
            cnt6 = 0
            x_sonar=[]
            x_steer=[]
            for line in fp:
                msg_str, msg = data_decoder.read_log_dataline(line)
                if msg_str.split('Stamped')[-1] == 'RawPosition' and (old_lat != msg.latitude or old_lon != msg.longitude):
                    cnt2 = 0
                    cnt += 1
                    old_lat = msg.latitude
                    old_lon = msg.longitude
                elif msg_str.split('Stamped')[-1] == 'ExtrapolatedPosition' and (old_e_lat != msg.latitude or old_e_lon != msg.longitude) and (old_lat != msg.latitude or old_lon != msg.longitude):
                    cnt2 += 1
                    pnt = kml_extrap.newpoint(name=f"P{str(cnt)}_{str(cnt2)}", coords=[(msg.longitude, msg.longitude)])
                    pnt.style.iconstyle.color = simplekml.Color.red
                    old_e_lat = msg.latitude
                    old_e_lon = msg.longitude
        kml_extrap.save(args.filepath.rsplit(".",1)[0] + "_extrap.kml")

    # Create a KML file for headings to next waypoints
    if args.all == True or args.path_heading_pts:
        kml_path_heading_pts = simplekml.Kml()

        old_lat = ''
        old_lon = ''    
        old_h_lat = ''
        old_h_lon = ''    
        with open(args.filepath) as fp:
            cnt = 0
            cnt3 = 0
            for line in fp:
                msg_str, msg = data_decoder.read_log_dataline(line)
                if msg_str.split('Stamped')[-1] == 'RawPosition' and (old_lat != msg.latitude or old_lon != msg.longitude):
                    cnt3 = 0
                    cnt += 1
                    old_lat = msg.latitude
                    old_lon = msg.longitude
                elif msg_str.split('Stamped')[-1] == 'Waypoint' and (old_h_lat != old_lat or old_h_lon != old_lon):
                    cnt3 += 1
                    pnt = kml_path_heading_pts.newpoint(name=f"P{str(cnt)}_{str(cnt3)}", coords=[(old_lon, old_lat)])
                    pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/arrow.png'
                    heading = msg.path_heading + 180.0 # add 180 because icon naturally points down
                    if heading > 360:
                        heading += -360
                    pnt.style.iconstyle.heading = heading                 
                    old_h_lat = old_lat
                    old_h_lon = old_lon
        kml_path_heading_pts.save(args.filepath.rsplit(".",1)[0] + "_path_heading.kml")

    # Create a KML file for the rover's headings
    if args.all == True or args.rover_heading_pts:
        kml_rover_heading_pts = simplekml.Kml()

        old_lat = ''
        old_lon = ''    
        with open(args.filepath) as fp:
            cnt = 0
            cnt4 = 0
            for line in fp:
                msg_str, msg = data_decoder.read_log_dataline(line)
                if msg_str.split('Stamped')[-1] == 'RawPosition' and (old_lat != msg.latitude or old_lon != msg.longitude):
                    cnt4 = 0
                    cnt += 1
                    old_lat = msg.latitude
                    old_lon = msg.longitude
                elif msg_str.split('Stamped')[-1] == 'Orientation' and old_lat != '' and old_lon != '':
                    cnt4 += 1
                    pnt = kml_rover_heading_pts.newpoint(name=f"P{str(cnt)}_{str(cnt4)}", coords=[(old_lon, old_lat)])
                    pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/arrow.png'
                    heading = float(msg.heading) + 180.0 # add 180 because icon naturally points down
                    if heading > 360:
                        heading += -360
                    pnt.style.iconstyle.heading = heading                 
        kml_rover_heading_pts.save(args.filepath.rsplit(".",1)[0] + "_true_heading.kml")

    # Create a kml for intermediate waypoints supplied by line-gravity
    if args.all == True or args.intermediate_pts:
        kml_intermediate = simplekml.Kml()

        old_lat = ''
        old_lon = ''    
        with open(args.filepath) as fp:
            cnt = 0
            for line in fp:
                msg_str, msg = data_decoder.read_log_dataline(line)
                if msg_str.split('Stamped')[-1] == 'Waypoint' and (old_lat != msg.lat_intermediate or old_lon != msg.lon_intermediate) and msg.lon_intermediate != '0.0000000':
                    cnt += 1
                    kml_intermediate.newpoint(name=f"P{str(cnt)}", coords=[(msg.lon_intermediate, msg.lat_intermediate)])
                    old_lat = msg.lat_intermediate
                    old_lon = msg.lon_intermediate

        kml_intermediate.save(args.filepath.rsplit(".",1)[0] + "_intermediate.kml")
    
if __name__ == '__main__':
    main()
