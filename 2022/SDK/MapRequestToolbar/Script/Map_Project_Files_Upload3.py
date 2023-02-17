# ---------------------------------------------------------------------------
# MapRequest_Uploads.py
# Created: 7/24/2018 - Grace Richey, TxDOT- TPP
# Updated: 9/14/2018 - Sam Bogle, TxDOT- TPP
# Updated: 10/21/2020 - Joyce Chien, TxDOT- TPP
# Usage: ArcGIS10.3/Python 2.7.8
# Description: Copy final deliverables to T drive
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy,os

#User Parameters

# Path to the "Project_Data_Upload" Folder
# Select path for map request folder in analyst’s local drive (i.e. C:/TxDOT/123_Project/Project_Data_Upload), folder, *Required
ProjectFolder = arcpy.GetParameterAsText(0)

# Path to Pre-existing Project Folder on T-drive
# Generate a txt file listed the path of the pre-existing folder that user selected, folder, *Optional
Expath = arcpy.GetParameterAsText(1)

# Get only the folder name of a path (i.e. 123_Project)
ProjectID = os.path.basename(os.path.dirname(ProjectFolder))
#os.path.basename(ProjectFolder) # user select folder path C:/TxDOT/123_Project # Get only the last part of a path
#os.path.basename(os.path.dirname(ProjectFolder)) # user select folder path C:/TxDOT/123_Project/Project_Data_Upload

# Create a new folder in T drive with the name of the MapID_ProjectName folder
Output_Directory = 'T:/DATAMGT/MAPPING/Map Requests/'+ProjectID
arcpy.AddMessage("Copying "+ ProjectID +" folder to T drive")

pathtoU = ProjectFolder
#pathtoU = ProjectFolder + '/Project_Data_Upload'
arcpy.AddMessage(pathtoU)

arcpy.Copy_management(pathtoU,Output_Directory)

# Copy contents of Upload folder to T Drive
arcpy.Copy_management(pathtoU,Output_Directory)

# Provide a quick link to the previously related project and write in the txt file
savefile = os.path.join(Output_Directory, "Path to Previous Map Request.txt")
pathshortcut = open(savefile, "w")
pathshortcut.write(Expath)
pathshortcut.close()

arcpy.AddMessage("Files copied to " + Output_Directory)





