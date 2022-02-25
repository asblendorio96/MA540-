TITLE:      README
DATE:       02-25-2022
AUTHOR:     MA540 Team 4

This directory contains all files necessary to automatically generate simulated photometry data.
Here's the process:

REQUIREMENTS:
- blender
- python (with numpy, matplotlib, etc....)

1. Generate Attitude Data
	- Open "generateAttitudeData.py"
	- Under USER INPUT select the number of files to generate
	- Run the script
	- Note the creation of CSV files in ./rotation_data
	
2. Modify Blender Scene/Script As Desired
	- Open the "satellite.blend" file
	- If you want to use a different satellite than what's in there, replace it
		NOTE: Ensure that object origin is set to its center of mass (this can be easily done in blender)
	- In the blender script (inside the editor in blender) change the file paths and satellite name
		NOTE: The photometry, render, and rotation_data directories are already in this folder. Use those!

3. Run the Script in Blender
	- This will iterate through all CSV files in the selected "rotation_data" directory and generate photoemtry for the given satellite
	- Individual images will no be saved for all runs. Only the most recent run will leave images in the selected "render" directory
	- The script will generate a CSV file for each photometry curve and save it to the selected "photoemtry" directory
	
4. Process and View Data (OPTIONAL)
	- If you want to view photometry plots, or need a place to start for data processing:
	- Open "readPhotometryCSV.py"
	- Change the filename and file path as desired
	- Run the script to see a photometry plot of the selected file
	- Photometry and time vectors are saved as "phot" and "t" respectively in the python environment.