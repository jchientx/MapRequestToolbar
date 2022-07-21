using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ArcGIS.Core.CIM;
using ArcGIS.Core.Data;
using ArcGIS.Core.Geometry;
using ArcGIS.Desktop.Catalog;
using ArcGIS.Desktop.Core;
using ArcGIS.Desktop.Core.Geoprocessing;
using ArcGIS.Desktop.Editing;
using ArcGIS.Desktop.Extensions;
using ArcGIS.Desktop.Framework;
using ArcGIS.Desktop.Framework.Contracts;
using ArcGIS.Desktop.Framework.Dialogs;
using ArcGIS.Desktop.Framework.Threading.Tasks;
using ArcGIS.Desktop.Mapping;

namespace MapRequestToolbar
{
    internal class UploadMapToAGOButton : Button
    {
        protected override void OnClick()
        {
            try
            {
                // Install the toolbox locally and set path to the toolbox
                var toolPath = AutoUpdater.UpdateToolbar() + @"\UploadMaptoAGO";

                //launch script tool from gp pane
                //https://github.com/esri/arcgis-pro-sdk/wiki/ProConcepts-Geoprocessing#open-the-tool-dialog-in-the-geoprocessing-pane

                // Set value array (empty values allow user full control) and launch tool
                var projectPath = "";
                var mapName = "";
                var mapDesc = "";
                var mapTags = "";
                var mapID = "";
                var toolParams = Geoprocessing.MakeValueArray(projectPath, mapName, mapDesc, mapTags, mapID);
                Geoprocessing.OpenToolDialog(toolPath, toolParams);
            }
            catch (Exception e)
            {
                MessageBox.Show("Something went wrong " + e);
            }
        }
    }
}
