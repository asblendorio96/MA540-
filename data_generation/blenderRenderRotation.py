"""
TITLE:      blenderRenderRotation.py
DATE:       02-03-2022
AUTHOR:     MA540 Team 4
    
DESCRIPTION:
This script interfaces with the Blender API to generate and render an animation
of the active object.


INPUTS:
    
fps             : Animation frames per second 
Rotation Data   : CSV file w/ time-series satellite attitude (quaternions)
                CSV FORMAT:
                Header
                (file_id,fps,dur,omega,sun_angle)
                Header
                (q0, q1, q2, q3, t)
                - q0 is quaternion scalar component
                - q1-q3 are quaternion vector components
                - t in seconds
"""

#%% IMPORTS %%#
import bpy
import csv
import math
from mathutils import Vector, Quaternion
import time
import numpy as np
import os

#%% INITIALIZATION %%#
# Light Initialization #
sun = bpy.data.objects['Sun'];
sun.rotation_mode = 'YXZ';

# Object Initialization #
sat = bpy.data.objects['Satellite'];     # Select the Satellite
sat.rotation_mode = 'QUATERNION'         # Set Object rotation type to Quaternion
sat.animation_data_clear();              # Delete All Animation Data

# Scene Initialization #
scn = bpy.context.scene;
scn.frame_start = 0;

# Load file of Quaternion Data
file = open('P:/MA540/Project/rotation_data.csv')
type(file)
csvreader = csv.reader(file)

# File System Initialization #
renderpath = "P:\\MA540\\Project\\data_generation\\render\\";
bpy.context.scene.render.filepath = renderpath;

#%% ASSIGN KEYFRAMES %%#
sunset_angle = -10*np.pi/180;                   # Slight angle so it's "after sunset" NOTE: YXZ rotation order
i            = 0                                # Keyframe Number
j            = 0                                # Line Number
init_flag    = False;                           # Initialization Flag
prog_bar     = list("[                   ]");   # Progress bar for fun
prog_count    = 1;                              # Increments every 5%
print('****************KEYFRAME ASSIGNMENT****************');
for row in csvreader:
    # Skip Headers
    if j == 0 or j == 2:
        j+=1;
        continue;
    
    # Initialize Variables
    if j == 1:
        file_id   = row[0];                                 # File ID for saving
        fps       = float(row[1]);                          # Animation FPS
        dur       = float(row[2]);                          # Animation Duration
        sun_angle = float(row[4]);                          # Sun Direction (radians
        sun.rotation_euler = (sun_angle,sunset_angle,0);    # Set Sun Direction
        init_flag = True;
        j+=1;
        print("INITIALIZED FILE: " + file_id);
        continue;
    
    # Confirm Initialization
    if init_flag == False:
        print("FAILED TO INITIALIZE...");
        break;
    
    # Parse Rotation Data
    q0 = row[0]
    q1 = row[1]
    q2 = row[2]
    q3 = row[3]
    t  = float(row[4])
    quat = float(q0), float(q1), float(q2), float(q3)
    
    # Set Orientation and add keyframe
    sat.rotation_quaternion = quat
    time.sleep(0.1)
    
    # Insert Key Frames
    i = math.floor(t*fps);                               # Calculate Frame Number
    sat.keyframe_insert('rotation_quaternion', frame=i)  # Set Keyframe
    
    # Progress Bar
    perc = math.floor(t/dur*100);
    if perc > 5*prog_count:
        prog_bar[prog_count]="=";
        prog_count+=1;
    
    print(''.join(prog_bar) + str (perc) + "%");
    j+=1;
    
file.close()
print('KEYFRAME ASSIGNMENT COMPLETE')

#%% RENDER ANIMATION %%#
print('****************RENDERING ANIMATION****************');
print('OUTPUT TARGET: ' + renderpath);

# Remove All PNG Files from Target Folder
print("Attempting to delete image files at output target...");
files = os.listdir(renderpath);                     # List of files in render path
if files:
    kill_count = 0;
    for item in files:
        if item.endswith(".png"):                       # Sort by png files
            os.remove(os.path.join(renderpath,item))    # Delete file
            kill_count += 1;
    print(str(kill_count) + " files deleted");
else:
    print("No Files to delete")
    
scn.frame_end = i;                          # Set Number of frames to render
print("Rendering " + str(i+1) + " frames...");
bpy.ops.render.render(animation=True);      # Render with current render settings

'''

TODO:
    - Automatically Set Light Direction (Collimated light source)
    - Automate Rendering - (Render animation with current settings and set output directory for images)
    - NOTE: camera position can be changed if desired. Might be mroe convenient to put it on the x-axis or something
    
    - Call script to generate photometry then delete images

'''