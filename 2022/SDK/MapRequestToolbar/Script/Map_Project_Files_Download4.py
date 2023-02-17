# ---------------------------------------------------------------------------
# Map_Project_Files_Download3.py
# Created: 7/24/2018 - Grace Richey, TxDOT- TPP
# Updated: 9/14/2018 - Sam Bogle, TxDOT- TPP
# Updated: 10/21/2020 - Joyce Chien, TxDOT- TPP
# Usage: ArcGIS Pro/Python 2.7.8
# Description: Create folders for Map Request Project and download map templates
# ---------------------------------------------------------------------------

# Import arcpy module
import os, sys
import arcpy
import getpass # The getpass() function is used to prompt to users using the string prompt and reads the input from the user as Password.

# UserParameters
# Project Folder, folder, *Required
Dir = arcpy.GetParameterAsText(0)
# Project ID, string, *Required
MapReqID = arcpy.GetParameterAsText(1)
# NEW: Project Name, string, *Required
ProjectName = arcpy.GetParameterAsText(2)
# NEW: Existing Map or New Template, string (Value List Filter:Ex/New), *Required
ExorNew = arcpy.GetParameterAsText(3)
# NEW: Path to Existing Map, folder, optional
PathtoEx = arcpy.GetParameterAsText(4)
# NEW: Copy Old Data from Existing Map Folder or not, string (Value List Filter:Y/N), optional
CopyOldData = arcpy.GetParameterAsText(5)
# PAGX Templates checkbox, [string] multivalue, optional
PAGX_Template = arcpy.GetParameterAsText(6)

# Local variables:
MapList = [x.strip() for x in PAGX_Template.split(";")] 
OldFolderName = os.path.basename(os.path.normpath(PathtoEx)) 
OldDatatoOldDrafts = Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName + '/Misc_Data_No_Upload'

# ---------------------------------------------------------------------------
# Create Folders
# ---------------------------------------------------------------------------

def CreateNewTemplate():
    # Create Folders Structure
    # Use os.makedirs() to create directory
    if ExorNew == "New Map Request":
        os.makedirs(Dir + '/' + MapReqID + '_' + ProjectName + '/Project_Data_Upload')
        os.makedirs(Dir + '/' + MapReqID + '_' + ProjectName + '/Project_Data_Upload' + '/Deliverables')
        os.makedirs(Dir + '/' + MapReqID + '_' + ProjectName + '/Project_Data_Upload' + '/Deliverables' + '/Map_upload_to_AGO')
        os.makedirs(Dir + '/' + MapReqID + '_' + ProjectName + '/Project_Data_Upload' + '/From Client')
        os.makedirs(Dir + '/' + MapReqID + '_' + ProjectName + '/Misc_Data_No_Upload')
        arcpy.AddMessage("Creating Folders Structure for the New Map Request: "+ Dir + '/' + MapReqID + '_' + ProjectName)
def CreateExistingMap():
    if ExorNew == "Previous Map Request":
        os.makedirs(Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName + '/Project_Data_Upload')
        os.makedirs(Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName + '/Project_Data_Upload' + '/Deliverables')
        os.makedirs(Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName + '/Project_Data_Upload' + '/Deliverables' + '/Map_upload_to_AGO')
        os.makedirs(Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName + '/Project_Data_Upload' + '/From Client')
        os.makedirs(Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName + '/Misc_Data_No_Upload')
        arcpy.AddMessage("Creating Folders Structure for the Previous Map Request: "+ Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName)

# Only for CreateExistingMap() use (copy old data to OldFolderName folder)  Future:  upgrade to shortcut icon
def copyExFiles():
    if CopyOldData == "Yes":
        arcpy.TransferFiles_management(PathtoEx, OldDatatoOldDrafts)
    # Create a txt file listed the path to existing file
    elif CopyOldData == "No":
        savepath = Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName + '/Misc_Data_No_Upload'
        savefile = os.path.join(savepath, "Path to Previous Map Request.txt")
        pathshortcut = open(savefile, "w")
        pathshortcut.write(PathtoEx)
        pathshortcut.close()
    else:
        arcpy.AddMessage("No copy of existing files for the New Project...")

# Dynamic Text
def updateAprxTemplate(templateName):
    if ExorNew == "New Map Request":
        mapTemplateFolder = Dir + '/' + MapReqID + '_' + ProjectName + '/Project_Data_Upload'
    else:
        mapTemplateFolder = Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName + '/Project_Data_Upload'
    aprx = arcpy.mp.ArcGISProject(templateName)

    for lyt in aprx.listLayouts():
        #arcpy.AddMessage(lyt)
        for elm in lyt.listElements("TEXT_ELEMENT"):
        #arcpy.AddMessage(elm.text)
            # if "#ID" in str(elm.text):
            if elm.text == 'ID# 1234':
                elm.text = ('ID# ' + MapReqID)

    # getuser() displays the login name of the user; checks the environment variables LOGNAME, USER, LNAME and USERNAME, in order.
    username = getpass.getuser()
    aprx.author = username 
    aprx.save() 
    del aprx 


def copyTemplates():
    # Specify one blank aprx (or one aprx with one default layout) to import the selected PAGX files into it.
    aprx = arcpy.mp.ArcGISProject("T:/DATAMGT/MAPPING/Map Requests/_Toolbar/MapRequest.aprx")

    #arcpy.AddMessage("Selected ArcMap copies:")
    #arcpy.AddMessage(len(MapList))
    
    if len(MapList) > 0:    
        if ExorNew == "New Map Request":
            mapTemplateFolder = Dir + '/' + MapReqID + '_' + ProjectName + '/Project_Data_Upload' + '/Deliverables'
        else:
            mapTemplateFolder = Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName + '/Project_Data_Upload' + '/Deliverables'

    # For loop PAGX list and import selected PAGXs to an APRX
    for mapDoc in MapList:
        arcpy.AddMessage(MapList)
        arcpy.AddMessage("Copying " + mapDoc + " Pagx")
        pagx_path = "T:/DATAMGT/MAPPING/Map Requests/_Templates/_ARCPRO_Mapping_Templates/Templates_2020/PAGX_CURRENT"
        # aprx.importDocument(input_PAGX)
        if mapDoc == "'Template_8.5 X 11 Portrait'":
            aprx.importDocument(pagx_path + '/Template_8.5 X 11 Portrait.pagx')
            arcpy.AddMessage("Download Template_8.5 X 11 Portrait.pagx")
        if mapDoc == "Template_8.5x11_Landscape":
            aprx.importDocument(pagx_path + '/Template_8.5x11_Landscape.pagx')
            arcpy.AddMessage("Download Template_8.5x11_Landscape.pagx")
        if mapDoc == "'Template _11x11'":
            aprx.importDocument(pagx_path + '/Template _11x11.pagx')
            arcpy.AddMessage("Download Template _11x11.pagx")
        if mapDoc == "Template_Portrait_11x17":
            aprx.importDocument(pagx_path + '/Template_Portrait_11x17.pagx')
            arcpy.AddMessage("Download Template_Portrait_11x17.pagx")
        if mapDoc == "Template_Landscape_11x17":
            aprx.importDocument(pagx_path + '/Template_Landscape_11x17.pagx')
            arcpy.AddMessage("Download Template_Landscape_11x17.pagx")
        if mapDoc == "Template_Landscape_22x34":
            aprx.importDocument(pagx_path + '/Template_Landscape_22x34.pagx')
            arcpy.AddMessage("Download Template_Landscape_22x34.pagx")
        if mapDoc == "'Template _34x44_Portrait'":
            aprx.importDocument(pagx_path + '/Template _34x44_Portrait.pagx')
            arcpy.AddMessage("Download Template _34x44_Portrait.pagx")
        if mapDoc == "Template_34x44_Landscape":
            aprx.importDocument(pagx_path + '/Template_34x44_Landscape.pagx')
            arcpy.AddMessage("Download Template_34x44_Landscape.pagx")
        if mapDoc == "Template_36x36":
            aprx.importDocument(pagx_path + '/Template_36x36.pagx')
            arcpy.AddMessage("Download Template_36x36.pagx")
        if mapDoc == "PowerPoint_7.5x10":
            aprx.importDocument(pagx_path + '/PowerPoint_7.5x10.pagx')
            arcpy.AddMessage("Download PowerPoint_7.5x10.pagx")
        if mapDoc == "PowerPoint_7.5x10._NO_HEADERS":
            aprx.importDocument(pagx_path + '/PowerPoint_7.5x10._NO_HEADERS.pagx')
            arcpy.AddMessage("Download PowerPoint_7.5x10._NO_HEADERS.pagx")
        if mapDoc == "Template_Portrait_22x34":
            aprx.importDocument(pagx_path + '/Template_Portrait_22x34.pagx')
            arcpy.AddMessage("Download Template_22x34_Portrait.pagx")
        if mapDoc == "Template_42x42":
            aprx.importDocument(pagx_path + '/Template_42x42.pagx')
            arcpy.AddMessage("Download Template _42x42.pagx")
    # (mapTemplateFolder + '/ImportedPAGX.aprx')
    aprx_rename = mapTemplateFolder + '/' + MapReqID + '_' + ProjectName
    aprx.saveACopy(aprx_rename + '.aprx')
    updateAprxTemplate(aprx_rename + '.aprx')

    # Create a Default gdb in the created project folder
    aprx_new = arcpy.mp.ArcGISProject(aprx_rename + '.aprx')
    arcpy.CreateFileGDB_management(mapTemplateFolder, MapReqID + '_' + ProjectName + '.gdb')
    aprx_new.defaultGeodatabase = aprx_rename + '.gdb'
    aprx_new.save()
    arcpy.AddMessage(aprx_new.defaultGeodatabase)

def createProjectFolder():
    # Create Project Folder
    #arcpy.AddMessage("Test: " + Dir + '/' + MapReqID + '_' + ProjectName)
    #arcpy.AddMessage("Test: " + Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName)
    
    if arcpy.Exists(Dir + '/' + MapReqID + '_' + ProjectName) and arcpy.Exists(Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName):
        # If it already exists do not create folder
        arcpy.AddMessage("Project folder already exists")
    elif arcpy.Exists(Dir + '/' + MapReqID + '_' + ProjectName):
        CreateExistingMap()
        copyExFiles()
        copyTemplates()
        
    elif arcpy.Exists(Dir + '/' + MapReqID + '_' + ProjectName + '_' + OldFolderName):
        CreateNewTemplate()
        copyExFiles()
        copyTemplates()
        
    else:
        arcpy.AddMessage("Creating Project Folder")
        CreateExistingMap()
        CreateNewTemplate()
        copyExFiles()
        copyTemplates()
        
    


# ---------------------------------------------------------------------------
# Create Project Folder
# ---------------------------------------------------------------------------
createProjectFolder()









