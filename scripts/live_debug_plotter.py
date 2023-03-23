import argparse
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons
import matplotlib.widgets
import os
import wgs84_transform_util as wtu
import math
import random

class DebugPlotter:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal', adjustable='box')
        self.lines = []
        self.lines.append((self.ax.plot(0.0, 0.0, marker='o', markersize=5, color='blue', label='bot_location')[0], 'blue'))
        self.lines.append((self.ax.plot(0.0, 0.0, linewidth=2, color='blue', label='bot_odometry')[0], 'blue'))
        self.lines.append((self.ax.arrow(0.0, 0.0, 0.0, 0.0, width=0.01, head_width=0.3, color='blue', label='bot_heading'), 'blue'))
        self.lines.append((self.ax.arrow(0.0, 0.0, 0.0, 0.0, width=0.01, head_width=0.3, color='yellow', label='bot_true_steer_output'), 'yellow'))
        self.lines.append((self.ax.arrow(0.0, 0.0, 0.0, 0.0, width=0.01, head_width=0.3, color='black', label='bot_sc_output'), 'black'))
        self.lines.append((self.ax.arrow(0.0, 0.0, 0.0, 0.0, width=0.01, head_width=0.3, color='green', label='path_heading'), 'green'))
        self.lines.append((self.ax.plot(0.0, 0.0, linewidth=2, color='red', label='path')[0], 'red'))
        self.lines.append((self.ax.plot(0.0, 0.0, marker='o', markersize=5, color='black', label='target')[0], 'black'))
        self.label_to_lines = {p[0].get_label(): p[0] for p in self.lines}
        #self.ax.legend()
        self.map_size = 15.0
        self.arrow_size = 0.6096

        #line_colors = ['blue' for l in self.label_to_lines.values()]
        ax_cb = self.fig.add_axes([0.05, 0.4, 0.1, 0.15])
        self.legend_cbs = CheckButtons(
            ax=ax_cb,
            labels=self.label_to_lines.keys(),
            actives=[l.get_visible() for l in self.label_to_lines.values()],
            #label_props={'color': line_colors},
            #frame_props={'edgecolor': line_colors},
            #check_props={'facecolor': line_colors},)
        )
        [cb.set_color(color) for cb, (_, color) in zip(self.legend_cbs.labels, self.lines)]
        self.legend_cbs.on_clicked(self.toggle_visibility)

        ax_follow = self.fig.add_axes([0.05, 0.25, 0.05, 0.015])
        self.btn_follow = Button(ax_follow, 'Follow Bot')
        self.btn_follow.on_clicked(self.follow_bot)
        ax_fixed = self.fig.add_axes([0.1, 0.25, 0.05, 0.015])
        self.btn_fixed = Button(ax_fixed, 'Fixed Map')
        self.btn_fixed.on_clicked(self.fixed_map)

        self.lat0 = None
        self.lon0 = None
        self.initialized = False
        self.follow_bot = True
        self.bot_odometry_x = []
        self.bot_odometry_y = []

    def toggle_visibility(self, label):
        line = self.label_to_lines[label]
        line.set_visible(not line.get_visible())
        line.figure.canvas.draw_idle()

    def follow_bot(self, event):
        self.follow_bot = True

    def fixed_map(self, event):
        self.follow_bot = False

    def heading_deg_to_vector(self, deg):
        # N: 0; E:90; S:180; W: 270
        # longitude associated with X
        # latitude associated with Y
        x = math.sin(float(deg) * math.pi / 180.0)
        y = math.cos(float(deg) * math.pi / 180.0)
        return (x, y)

    def calc_bearing(self, lat1, lon1, lat2, lon2):
        lat1 *= math.pi / 180.0
        lat2 *= math.pi / 180.0
        lon1 *= math.pi / 180.0
        lon2 *= math.pi / 180.0
        dLon = lon2 - lon1

        y = math.sin(dLon) * math.cos(lat2);
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)

        brng = math.atan2(y, x)

        brng *= 180.0 / math.pi
        brng = (brng + 360) % 360

        return brng
    
    def update(self, bot_lat, bot_lon, bot_heading,
               wp1_lat, wp1_lon, wp2_lat, wp2_lon,
               sc_steering_angle, true_steering_angle, path_heading,
               heading_error, crosstrack_error):
        # todo need a heading_lock or intialized flag to do this right
        if not self.initialized and (bot_lat == 0.0 and bot_lon == 0.0):
            return
        self.initialized = True

        if self.lat0 is None:
            self.lat0 = bot_lat
            self.lon0 = bot_lon

        #print(bot_heading)
        
        bearing = self.calc_bearing(wp1_lat, wp1_lon, wp2_lat, wp2_lon)

        (bot_x), (bot_y) = wtu.wgs84_to_local_xy(bot_lat, bot_lon, lat0=self.lat0, lon0=self.lon0, alt0=0.0)
        if self.follow_bot:
            self.ax.set_xlim([bot_x - self.map_size / 2.0, bot_x + self.map_size / 2.0])
            self.ax.set_ylim([bot_y - self.map_size / 2.0, bot_y + self.map_size / 2.0])

        # update bot location on plot
        self.label_to_lines['bot_location'].set_xdata(bot_x)
        self.label_to_lines['bot_location'].set_ydata(bot_y)
        self.bot_odometry_x.append(bot_x)
        self.bot_odometry_y.append(bot_y)
        self.label_to_lines['bot_odometry'].set_xdata(self.bot_odometry_x)
        self.label_to_lines['bot_odometry'].set_ydata(self.bot_odometry_y)

        # update bot orientation on plot
        dx, dy = self.heading_deg_to_vector(bot_heading)
        self.label_to_lines['bot_heading'].set_data(
            x=bot_x, y=bot_y,
            dx=self.arrow_size*dx,
            dy=self.arrow_size*dy)

        # update bot true steer plot
        dx, dy = self.heading_deg_to_vector(bot_heading + (true_steering_angle - 90.0))
        self.label_to_lines['bot_true_steer_output'].set_data(
            x=bot_x, y=bot_y,
            dx=self.arrow_size*dx,
            dy=self.arrow_size*dy)

        # update bot sc steering value plot
        dx, dy = self.heading_deg_to_vector(bot_heading + sc_steering_angle)
        self.label_to_lines['bot_sc_output'].set_data(
            x=bot_x, y=bot_y,
            dx=self.arrow_size*dx,
            dy=self.arrow_size*dy)

        (wp1_x, wp2_x), (wp1_y, wp2_y) = wtu.wgs84_to_local_xy([wp1_lat, wp2_lat], [wp1_lon, wp2_lon],
                                                                lat0=self.lat0, lon0=self.lon0, alt0=0.0)
        print(f'bot_heading: {bot_heading} test: {math.atan2(wp2_x - wp1_x, wp2_y - wp1_y) * 180.0 / math.pi} path_heading: {path_heading} bearing: {bearing} heading_error: {heading_error} crosstrack_error: {crosstrack_error} sc: {sc_steering_angle} ts: {true_steering_angle}')
        #print(wp1_lat, wp1_lon)
        # update path plot
        self.label_to_lines['path'].set_xdata([wp1_x, wp2_x])
        self.label_to_lines['path'].set_ydata([wp1_y, wp2_y])

        # update path heading_plot
        dx, dy = self.heading_deg_to_vector(path_heading)
        self.label_to_lines['path_heading'].set_data(
            x=bot_x, y=bot_y,
            dx=self.arrow_size*dx,
            dy=self.arrow_size*dy)

        # update target plot
        self.label_to_lines['target'].set_xdata(wp2_x)
        self.label_to_lines['target'].set_ydata(wp2_y)

        # update plot
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.show(block=False)
        #plt.pause(1.0)