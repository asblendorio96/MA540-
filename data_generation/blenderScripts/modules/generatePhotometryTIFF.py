"""
TITLE:      generatePhotometry
DATE:       02-03-2022
AUTHOR:     MA540 Team 4
    
DESCRIPTION:
This script loads 16-bit greyscale TIFF's from the specified directory and
generates time-series photometry data by computing the average value of all
pixels in each image.

The script expects the files to be named using Blender's default naming scheme
for png outputs. (i.e. '0001.tif', '0002.tif', etc.)

INPUTS:

numImages   : Number of images in directory
imDir       : File path to directory
frameRate   : Frames-per-second for the animation (from Blender)
showImage   : Setting to 'True' will display each image  

REQUIREMENTS:

readTIFF.py

"""
import readTIFF as rt
import numpy as np
import math

def generatePhotometry(imDir,frameRate,numImages):
    # Number of place values for zero padding
    num_places = 4;#math.floor(math.log10(numImages))+1;
    
    ## Photometry Array ##
    photometry = np.empty(shape=(numImages,1))
    normFac  = 2**16;       # Normalizing Factor
    
    #%% Iterate Through All Images %%#
    for k in range(numImages):
        ## File Name ##
        # Image Name
        imName = str(k).zfill(num_places) + '.tif'
        
        # File Path for this Image     
        imPath = imDir + imName
        print("Processing Image: ",imPath)
        
        ## Load Image Data ##
        # Load Image
        reader = rt.TIFFreader(imPath);
        image  = reader.im_pixels;
        
        # Image Data
        numPixels = image.size
        imgWidth  = image.shape[1]
        imgHeight = image.shape[0]
        
        ## Process Image ##
        pixelSum = 0;           
        
        # Loop Through Image
        for i in range(imgHeight):
            for j in range(imgWidth):
                pixelSum += image[i][j]/normFac;
        
        # Normalize Pixel Sum
        brightness = pixelSum/numPixels;
        
        # Save Photometry Data
        photometry[k] = brightness;
    
    #%% Save Photometry Data %%#
    
    # Generate Time Space
    dur = numImages/frameRate;                          # Animation Duration
    t   = np.array([np.linspace(0,dur,numImages)]).T;   # Time Vector

    #phot_data = np.array([photometry,t],dtype='float');
    phot_data = np.column_stack((photometry,t));
    
    return phot_data
    
    # Plot stuff
    #import matplotlib.pyplot as plt
    #plt.plot(t,photometry,'.');
    #plt.xlabel('Time [s]');
    #plt.ylabel('Brightness');
    #plt.title('Satellite Photometry');


#DEBUG
#generatePhotometry('./render/',24,5);