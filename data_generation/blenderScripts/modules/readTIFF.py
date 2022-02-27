# -*- coding: utf-8 -*-
"""
TITLE:      readTIFF
DATE:       02-25-2022
AUTHOR:     MA540 Team 4
    
DESCRIPTION:
Reads pixel data from TIFF file

Assumes single IFD. Requires 16-Bit greyscale and NO compression.

Description of TIFF Format:
https://docs.fileformat.com/image/tiff/

List of IFD Tags:
https://www.loc.gov/preservation/digital/formats/content/tiff_tags.shtml

"""

import numpy as np

class TIFFreader:
    
    #%% CLASS VARIABLES %%#
    filepath     = '';      # Directory and File Name
    tiff_data    = None;    # Array of bytes from file
    lil_end      = None;    # TIFF Bytes in Little Endian Format?
    
    # IFD Entry Values
    im_width    = -1;       # Image Width
    im_height   = -1;       # Image Height
    im_depth    = -1;       # Bit Depth
    im_comp     = -1;       # Compression Type
    im_color    = -1;       # Image Color Space
    im_fill     = -1;       # Fill Order
    im_stripOff = -1;       # Strip Offset
    im_spp      = -1;       # Samples Per Pixel
    im_rps      = -1;       # Rows Per Strip
    im_sbc      = -1;       # Strip Byte Counts
    im_xRes     = -1;       # X Resolution
    im_yRes     = -1;       # Y Resolution
    im_pCon     = -1;       # Planar Configuration
    im_unit     = -1;       # Resolution Unit
    
    # Pixel Data
    im_data     = None;     # Raw Bytes
    im_pixels   = None;     # Pixel Data
    
    #%% CONSTRUCTOR %%#
    def __init__(self, filepath):
        #%% Load File %%#
        self.filepath = filepath;
        # Open File
        file = open(filepath,"rb");
        # Load File
        self.tiff_data = file.read();
        # Close File
        file.close();
        
        # Read the TIFF Data
        self.readTIFF();
        
    #%% Private Functions %%#
    
    # Return value of an array of bytes
    # arranged with MSB first (Big Endian)
    def __readBE(self,byte_array):
        byte_sum    = 0;
        place_value = 1;
        for byte in reversed(byte_array):   
            byte_sum += byte*place_value;
            place_value *= 0x100;
        return byte_sum
    
    # Return value of an array of bytes
    # arranged with LSB first (Little Endian)
    def __readLE(self,byte_array):
        byte_sum    = 0;
        place_value = 1;
        for byte in byte_array:   
            byte_sum += byte*place_value;
            place_value *= 0x100;
        return byte_sum
    
    
    #%% Public Functions %%#
    def readTIFF(self):
        #%% Read Header %%#
        # First 8 Bytes
        header = self.tiff_data[0:8]
        
        # Byte Order (II = LSB First - Little Endian, MM = MSB First - Big Endian)
        if header[0] == header[1]:
            if header[0] == 0x49:
                self.lil_end = True;
            elif header[0] == 0x4D:
                self.lil_end = False;
            else:
                raise NameError('Error reading header - Byte order not recognized');
        else:
            raise NameError('Error reading header - Byte order format error');
        
        # Check to make sure it's a TIFF
        # Arrange bytes
        if self.lil_end:
            file_check = self.__readLE(header[2:4]); 
        else:
            file_check = self.__readBE(header[2:4]);
        
        if file_check != 42:
            raise NameError('Error reading header - File check value incorrect');
           
        # Address of First IFD (Image File Directory)    
        if self.lil_end:
            IFD_address = self.__readLE(header[4:8]);    
        else:
            IFD_address = self.__readBE(header[4:8]); 
            
        #%% Read Image File Directory %%#
        # IFD Contains info about image and pointers to image data
        # Format: 2-bytes number of entries, followed by sequence of 12 byte entries,
        # followed by 4-byte offset to next IFD (or 0 if note)
        
        if self.lil_end:
            num_entries = self.__readLE(self.tiff_data[IFD_address:(IFD_address+1)]); 
        else:
            num_entries = self.__readBE(self.tiff_data[IFD_address:(IFD_address+1)]); 
    
        IFD_start = IFD_address+2;
        IFD = self.tiff_data[(IFD_start):(IFD_start+12*num_entries)];
        
        # Iterate Through IFD Entries
        for i in range(num_entries):
            # Extract Entry
            entry = IFD[i*12:i*12+12];
            
            # Extract Entry Components       
            if self.lil_end:
                e_tag   = self.__readLE(entry[0:2]);
                e_type  = self.__readLE(entry[2:4]);
                e_count = self.__readLE(entry[4:8]);
                e_val   = self.__readLE(entry[8:12]);
            else:
                e_tag   = self.__readBE(entry[0:2]);
                e_type  = self.__readBE(entry[2:4]);
                e_count = self.__readBE(entry[4:8]);
                e_val   = self.__readBE(entry[8:12]);
            
            # Decode Entries
            if e_tag == 0x0100:         # Image Width
                self.im_width = e_val;       
            if e_tag == 0x0101:         # Image Height
                self.im_height = e_val;       
            if e_tag == 0x0102:         # Bit Depth
                self.im_depth = e_val;       
            if e_tag == 0x0103:         # Compression Type
                self.im_comp = e_val;
            if e_tag == 0x0106:         # Image Color Space
                self.im_color = e_val;
            if e_tag == 0x010A:         # Fill Order
                self.im_fill = e_val; 
            if e_tag == 0x0111:         # Strip Offset
                self.im_stripOff = e_val;
            if e_tag == 0x0115:         # Samples Per Pixel
                self.im_spp = e_val;
            if e_tag == 0x0116:         # Rows Per Strip
                self.im_rps = e_val;
            if e_tag == 0x0117:         # Strip Byte Counts
                self.im_sbc = e_val;
            if e_tag == 0x011A:         # X Resolution
                self.im_xRes = e_val;
            if e_tag == 0x011B:         # Y Resolution
                self.im_yRes = e_val;
            if e_tag == 0x011C:         # Planar Configuration
                self.im_pCon = e_val;
            if e_tag == 0x0128:         # Resolution Unit
                self.im_unit = e_val;
            
            # Print Each Entry    
            #print(hex(e_tag) + " : " + str(e_val) + " : " + hex(e_count)); 
                
             
        #  Check Entries
        if self.im_depth != 16:
            raise NameError('Not 16-Bit');
        if self.im_comp != 1:
            raise NameError('Image must not have compression');
        if self.im_color != 1:
            raise NameError('Image is not greyscale');
        if self.im_fill != 1:
            raise NameError('Encountered an unexpected fill order');

        #%% Read Image Data %%#
        # Extract Image Data
        self.im_data = self.tiff_data[(self.im_stripOff):(self.im_stripOff+self.im_sbc)];
        
        # Sanity Check
        bpp = int(self.im_depth / 8);                       # Bytes Per Pixel
        expected_bytes = self.im_height*self.im_width*bpp;  # Expected Bytes of image data
        if expected_bytes != self.im_sbc:
            raise NameError('Something went wrong parsing data...');
        
        
        self.im_pixels = np.zeros([self.im_width,self.im_height]);
        
        # Iterate and Save Pixel Data
        for i in range(self.im_height):
            for j in range(self.im_width):
                # Start of Pixel Byte Array in Data
                k = (i*self.im_width + j)*bpp;
                
                # Evaluate Pixel Value
                if self.lil_end:
                    pixel = self.__readLE(self.im_data[k:(k+bpp)]);
                else:
                    pixel = self.__readBE(self.im_data[k:(k+bpp)]);  
                
                self.im_pixels[j,i] = pixel;
        
        
        
# DISPLAY IMAGE
# from matplotlib import pyplot as plt
# plt.imshow(np.transpose(a),cmap='gray',vmin=0,vmax=2**16)
        


