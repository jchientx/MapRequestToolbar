using System.Data;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ArcGIS.Core.CIM;
using ArcGIS.Core.Data;
using ArcGIS.Core.Geometry;
using ArcGIS.Desktop.Catalog;
using ArcGIS.Desktop.Core;
using ArcGIS.Desktop.Editing;
using ArcGIS.Desktop.Extensions;
using ArcGIS.Desktop.Framework;
using ArcGIS.Desktop.Framework.Contracts;
using ArcGIS.Desktop.Framework.Dialogs;
using ArcGIS.Desktop.GeoProcessing;
using ArcGIS.Desktop.Framework.Threading.Tasks;
using ArcGIS.Desktop.Mapping;
using System.Windows;
using ArcGIS.Desktop.Editing.Attributes;
using ArcGIS.Desktop.Core.Geoprocessing;
using System.Threading;
using MessageBox = ArcGIS.Desktop.Framework.Dialogs.MessageBox;
using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
namespace MapRequestToolbar
{
    class AutoUpdater
    {
        public static string UpdateToolbar()
        {
            try
            {

                // Set source and local directories and get tbx file
                var sourceDir = @"T:\DATAMGT\MAPPING\Map Requests\_Toolbar\tool_and_scripts";
                var localDir = @"C:\TxDOT\MapRequestTools";
                var localPath = localDir + @"\tools_and_scripts";

                // Get name of tbx file
                var tbxName = Path
                    .GetFileName(Directory.GetFiles(sourceDir, "*.tbx").ElementAt(0));

                // Set local tbx path
                var tbxPath = localPath + @"\" + tbxName;

                // Copy tbx locally
                if (!Directory.Exists(localPath))
                {
                    System.IO.Directory.CreateDirectory(localPath);
                    File.Copy(sourceDir + @"\" + tbxName, tbxPath);
                }
                else
                {
                    File.Delete(tbxPath);
                    File.Copy(sourceDir + @"\" + tbxName, tbxPath);
                }
                // Return path to toobox
                return tbxPath;

            }
            catch (Exception e)
            {
                MessageBox.Show(e.Message);
                return null;
            }
        }
    }
}