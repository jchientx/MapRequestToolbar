# ---------------------------------------------------------------------------
# Upload Maps to AGO Map Gallery3.py
# Created: 8/17/2018 - Sam Bogle, TxDOT- TPP
# Updated: 10/21/2020 - Joyce Chien, TxDOT- TPP
# Usage: ArcGIS Pro/Python 3
# Description: Copy final maps to AGO and share to TPP Data Management Map Gallery group
# ---------------------------------------------------------------------------

# Import arcpy module
from arcgis.gis import GIS
import glob, os, arcpy

# Credentials
# Access AGO with enterprise account
gis = GIS("http://txdot.maps.arcgis.com")
gis = GIS("pro")

# UserParameters
# For users to select the PNG/JPG/PDF file to upload to AGO and assign the title, description, and tags
ProjectFolder = arcpy.GetParameterAsText(0)
MapTitle = arcpy.GetParameterAsText(1)
MapDesc = arcpy.GetParameterAsText(2)
MapTags = arcpy.GetParameterAsText(3)
# If you type "Test" in the tool, it will catch all items with the title contains "test"
MapID = arcpy.GetParameterAsText(4)

# Create list of paths
dir = ProjectFolder
dirlist = []

taglist = [MapTags, MapID]

# Before you run this for loop, print so you can see the dir path
arcpy.AddMessage(os.listdir(ProjectFolder))

# Add the files of the dir path to dirlist
for file in os.listdir(ProjectFolder):
  if file.endswith(".png"):
    dirlist.append(os.path.join(dir,file))
  elif file.endswith(".pdf"):
    dirlist.append(os.path.join(dir,file))
  elif file.endswith(".jpg"):
    dirlist.append(os.path.join(dir,file))

# Assign metadata to the upload PNG in AGO
map_properties = {'title': MapTitle,
                 'description': MapDesc,
                 'tags': taglist, #MapTags,
                 'type':'Image'}

# Add item to AGOL
i = 0
count = 0
while i < len(dirlist):
   # Add item to AGOL
   UploadMap = gis.content.add(map_properties,dirlist[i])
   # gis.content.add({'type':'PNG'},dirlist[i])
   UploadMap
   i += 1
   print (i)
   if i >= len(dirlist):
     break

arcpy.AddMessage(len(dirlist))
arcpy.AddMessage("Adding a file to my content")
'''
for x in dirlist:
  # Add item to AGOL
  arcpy.AddMessage("I'm adding a file to my content")
  gis.content.add({'type': 'PNG'}, x)
'''

# Search for content that equals to MapTitle using content.search
# Search for items owned by the logged-in user
ql = f'title:{MapTitle}' + ' AND owner:'+ gis.users.me.username
arcpy.AddMessage(ql)
# search_result_map = gis.content.search(query=ql)

search_result_map = []
is_good = False
while is_good is False:
    arcpy.AddMessage("Please wait a second until the file uploaded to AGO...")
    search_result_map = gis.content.search(query=ql)
    # Check the search result with the exact title equals to MapTitle
    for search in search_result_map:
        arcpy.AddMessage("Double check search result...")
        if search["title"] == MapTitle:
            search_result_map[0] = search
            is_good = True
            arcpy.AddMessage("Got the right result!")
            break

arcpy.AddMessage(search_result_map)


# Get the itemid of first item from previous query
first_item = search_result_map[0]
known_item_id = first_item.id
arcpy.AddMessage(f"The item ID is: {known_item_id}")

# Get the item you want to work on, use the get() to access this item
item1 = gis.content.get(known_item_id)
arcpy.AddMessage(f"The item is: {item1}")
# Upload PNG/PDF/JPG files to the specific group named "TPP Data Management Map Gallery" on AGO
group = gis.groups.search('title: TPP Data Management Map Gallery','')
arcpy.AddMessage(group[0])
SharetoGroup = item1.share(groups=group)
SharetoGroup

arcpy.AddMessage("The file is shared with TPP Data Management Map Gallery")
arcpy.AddMessage("Finished")

# Future version goals: 1. Fix "Test" title search issue (OK) 2. Assign to specified group categories 3. Overwrite the same file existed in AGO
# 4. Write instruction to remind users do not upload the same file name as the item already existed in AGO content, or the script will share wrong item!
