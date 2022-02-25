# -*- coding: utf-8 -*-
"""
TITLE:      generateAttitudeData
DATE:       02-03-2022
AUTHOR:     MA540 Team 4
    
DESCRIPTION:
A python script that generates a csv file of rotation quaternions to be
read in by the blenderRenderRotation script. Rotation parameters are randomized
within reasonable bounds. A set of fixed parameters may be specified by the user.

INPUTS:

dur   : Durration of rotation in seconds
fps   : Animation frames per second

"""

#%% IMPORTS %%#
import numpy as np
import random as rnd
import quat
import csv
from datetime import datetime

#%% USER INPUT %%#
num_files = 3;

#%% ********************** BEGIN GENERATING FILES ********************** %%#
for file_count in range(num_files):
    
    #%% GENERATE FILE ID %%#
    today = datetime.now();
    
    # Format As YYYYMMDDhhmmssCCCC 
    # CCCC is a 4-digit counter starting at 0 that increments for each file
    
    Y = str(today.year);
    M = str(today.month);
    D = str(today.day);
    h = str(today.hour);
    m = str(today.minute);
    s = str(today.second);
    c = str(file_count);
    
    YYYY  = Y.zfill(4); 
    MM    = M.zfill(2);
    DD    = D.zfill(2);
    hh    = h.zfill(2);
    mm    = m.zfill(2);
    ss    = s.zfill(2);
    CCCC = c.zfill(4);
    
    file_id = YYYY+MM+DD+hh+mm+ss+CCCC;
    
    #%% SOLAR VECTOR %%#
    sun_angle = rnd.uniform(0,2*np.pi);  # Sun angle in ZY plane (radians)
    
    #%% ROTATION PARAMETERS %%#
    # Fixed Parameters
    fps   = 24;                                         # Frames Per Second
    dt    = 1/fps;                                      # Time interval
    t_max = 12;                                         # Maximum Duration
    t_min = 8;                                          # Minimum Duration
    
    # Variable Parameters
    dur        = rnd.uniform(t_min,t_max);                   # Durration in Seconds
    t          = np.linspace(0,dur,int(np.ceil(fps*dur)));   # Time Vector
    num_frames = len(t);                                     # Number of frames
    
    omega_max = 5*(2*np.pi/dur);                                        # Maximum of 6 rotations
    omega_min = 2*(2*np.pi/dur);                                        # Minimum of 3 rotations
    theta     = 0;                                                      # Anglular Displacement
    omega     = rnd.uniform(omega_min,omega_max);                       # Angular velocity [s^-1]
    rot_axis  = np.array([rnd.random(), rnd.random(), rnd.random()]);   # Rotation Axis
    init_axis = np.array([rnd.random(), rnd.random(), rnd.random()]);   # Initial Rotation Axis
    init_ang  = np.array(rnd.random()*np.pi*2);                         # Initial Rotation
    
    # Initialize Quaternions
    q_init = quat.Quat();                           # Initial attitude quaternion
    q_init.setAngleAxis(init_ang, init_axis);
    
    q_rot = quat.Quat();                            # Applied rotation quaternion
    q_rot.setAngleAxis(theta, rot_axis);
    
    q = q_init;                                     # Quaternion attitude variable 
    
    path     = "./rotation_data/";
    filename = "rotation_data_" + file_id + ".csv";
    filepath = path + filename;
    
    #%% WRITE TO CSV %%#
    with open(filepath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write Header
        csvwriter.writerow(np.array(["file_id","fps","dur","num_frames","sun_angle"]));
        csvwriter.writerow(np.array([file_id,fps,dur,num_frames,sun_angle]));
        csvwriter.writerow(np.array(["omega","x_rot", "y_rot", "z_rot"]));
        csvwriter.writerow(np.array([omega,rot_axis[0],rot_axis[1],rot_axis[2]]));
        
        # Write Header
        csvwriter.writerow(np.array(["q0","q1","q2","q3","t"]));
        for i in range(num_frames):
            # Write Row
            row = np.array([q.q0, q.q1, q.q2, q.q3, t[i]]); 
            csvwriter.writerow(row);
            #print("Print Row: ", row.astype('str'))    
            
            # Apply Rotation
            theta+=omega*dt;                        # Update Rotation Angle
            q_rot.setAngleAxis(theta, rot_axis);    # Rotation Quaternion
            q = q_rot*q_init;                       # Apply init and rotation
    
            # Successive rotations: Multiply two quaternions
            # q3 = q1*q2     is  Perform rotation q2 then q1
    
    print("FILE: " + filename + " SAVED");
