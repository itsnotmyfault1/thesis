import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt

pgf_with_custom_preamble = {
    "pgf.texsystem": "xelatex",
    "font.family": "sans-serif", # use san serif/main font for text elements
    "font.size": 10,
    "text.usetex": False,    # use inline math for ticks
    "pgf.rcfonts": False,   
    "pgf.preamble": [
        r"\usepackage{amsmath}",
        r"\usepackage{fontspec}",
        r"\setmainfont{Avenir Next}",
        r"\setsansfont{Avenir Next}",
        r"\usepackage{units}",
    ]
}
mpl.rcParams.update(pgf_with_custom_preamble)

#define colors http://colorschemedesigner.com/csd-3.5/#3B400hWs0dJMP
color0      = '#476A92'
color0light = '#9EC0E7'
color1      = '#BAD55E'
color1light = '#E3F6A2'
color2      = '#A0468F'
color2light = '#EA9ADB'
color3      = '#DFAE62'
color3light = '#F8D6A3'

#load data
knee_running_data = sio.loadmat('knee_running.mat')
time         = knee_running_data['time']
knee_torque  = knee_running_data['knee_torque']
knee_speed   = knee_running_data['knee_speed']
torque_motor = knee_running_data['torque_motor']
motor_speed  = knee_running_data['motor_speed']
torque_motor_rms  = knee_running_data['torque_motor_rms'][0][0]

tau_max = 4.5
tau_rated = 1.43
volt_lim_speed = [0, 3730, 5460, 5790];
volt_lim_tau =   [tau_max, tau_max, tau_rated, 0];

#create figure
fig, ax = plt.subplots(1,1, figsize = (2,2))

#plot lines
p0, = ax.plot(np.abs(motor_speed)/(2*np.pi)*60., np.abs(torque_motor),
    linewidth=2, color=color0)
p1, = ax.plot(volt_lim_speed, volt_lim_tau,
    linewidth=2, color=color1)
p2, = ax.plot([0, 6000], [tau_rated, tau_rated], '--',
    linewidth=2, color=color2)
p3, = ax.plot([0, 6000], [torque_motor_rms, torque_motor_rms], '--',
    linewidth=2, color=color3)

ax.legend((p0, p1, p2, p3), ('Motor Torque', 'Torque Limit', 
    'Rated Torque', 'RMS Motor Torque'), frameon = False, loc = (-0.2, -1),
    handlelength=3)
ax.xaxis.set_label_text('Motor Speed (RPM)')
ax.yaxis.set_label_text('Motor Torque (N-m)')

#set axis properties
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

#ax.axis([-250, 6000, -0.1, 4.6])
ax.set_yticks((0, 1.43, np.max(np.abs(torque_motor)), tau_max))
ax.set_xticks((0, np.max(np.abs(motor_speed))/(2*np.pi)*60, volt_lim_speed[-1]))
for label in ax.get_xticklabels()[1:]:
    label.set_rotation(45), 
    label.set_rotation_mode('anchor'), 
    label.set_horizontalalignment('right')

inv_data = ax.transData.inverted()
inv_axes = ax.transAxes.inverted()

try:
    ylabelpos_axes = ax.yaxis.get_label().get_position()
    ylabelpos_display = ax.transAxes.transform(ylabelpos_axes)
    ylabelpos_data = inv_data.transform(ylabelpos_display)
    ylabelpos_data[1] = (ax.get_yticks()[0] + ax.get_yticks()[-1])/2.0
    ylabelpos_display = ax.transData.transform(ylabelpos_data)
    ylabelpos_axes = inv_axes.transform(ylabelpos_display)
    ax.yaxis.get_label().set_position(ylabelpos_axes)
except:
    pass

try:
    xlabelpos_axes = ax.xaxis.get_label().get_position()
    xlabelpos_display = ax.transAxes.transform(xlabelpos_axes)
    xlabelpos_data = inv_data.transform(xlabelpos_display)
    xlabelpos_data[0] = (ax.get_xticks()[0] + ax.get_xticks()[-1])/2.0
    xlabelpos_display = ax.transData.transform(xlabelpos_data)
    xlabelpos_axes = inv_axes.transform(xlabelpos_display)
    ax.xaxis.get_label().set_position(xlabelpos_axes)
except:
    pass

filename = 'knee_motor_torque.pdf'
fig.savefig(filename, bbox_inches='tight')

#create figure
plt.close(fig)
fig = plt.figure(figsize = (2,2))
ax = plt.axes()

#plot lines
markersize = 4
p0, = ax.plot(time, knee_torque, linewidth=2, color=color0)

ax.yaxis.set_label_text('Knee Torque (N-m)')
ax.xaxis.set_label_text('Time (s)')

#set axis properties
ax.xaxis.set_tick_params(direction = 'out', width = 1)
ax.yaxis.set_tick_params(direction = 'out', width = 1)
ax.yaxis.set_tick_params(which='minor', direction = 'out', width = 1)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.axis([-5, 105, -55, 155])
ax.spines['left'].set_bounds(-50, 150)
ax.set_yticks(np.arange(-50, 200, 50))
ax.spines['bottom'].set_bounds(0, 100)
ax.set_xticks(np.arange(0,125,25))

filename = 'knee_running_torque.pdf'
fig.savefig(filename, bbox_inches='tight')

#create figure
plt.close(fig)
fig = plt.figure(figsize = (2,2))
ax = plt.axes()

#plot lines
markersize = 4
p0, = ax.plot(time, knee_speed/(2*np.pi), linewidth=2, color=color1)

ax.yaxis.set_label_text('Knee Speed (rev/s)')
ax.xaxis.set_label_text('Time (s)')

#set axis properties
ax.xaxis.set_tick_params(direction = 'out', width = 1)
ax.yaxis.set_tick_params(direction = 'out', width = 1)
ax.yaxis.set_tick_params(which='minor', direction = 'out', width = 1)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.axis([-5, 105, -1.6, 1.6])
ax.spines['left'].set_bounds(-1.5, 1.5)
ax.set_yticks(np.arange(-1.5, 3, 1.5))
ax.spines['bottom'].set_bounds(0, 100)
ax.set_xticks(np.arange(0,125,25))

filename = 'knee_running_speed.pdf'
fig.savefig(filename, bbox_inches='tight')
