# ---------------------------------------------------------------------------
# Program Name: shielding.py
#
# Arguments
#   wsdem  - the input watershed DEM
#   shield - the output shield raster
#   az_interval - the interval of Azimuth
#   el_interval - the interval of Altitude
#   z_factor    - the z-factor
#
# Created by: Yingkui Li
#             Department of Geography
#             University of Tennessee, Knoxville, TN 65211
#             5/2010 - 6/2010
# Usage: shielding <wsdem> <shield> <az_interval> <el_interval> <z_factor>
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, arcgisscripting

# Create the Geoprocessor object
gp = arcgisscripting.create()

# Check out any necessary licenses
gp.CheckOutExtension("spatial")
# Load required toolboxes...
#gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Spatial Analyst Tools.tbx")
#gp.AddToolbox("C:/Program Files/ArcGIS/ArcToolbox/Toolboxes/Data Management Tools.tbx")


# Obtain arguments...
wsdem = sys.argv[1]
#wsdem = "c:\\temp\\demtest\\demsam"
shield = sys.argv[2]
#shield = "c:\\temp\\demtest\\demsam7"

az_interval = sys.argv[3]
if az_interval == '#':
    az_interval = "5" # provide a default value if unspecified
#az_interval = "90" # provide a default value if unspecified

# create the az list 0-360
az_list = range (0,360,int(az_interval))

el_interval = sys.argv[4]
if el_interval == '#':
    el_interval = "5" # provide a default value if unspecified
#el_interval = "20" # provide a default value if unspecified

# create the el list 0-90 including 90
el_list = range(0,100,int(el_interval))

z_factor = sys.argv[5]
if z_factor == '#':
    z_factor = "1" # provide a default value if unspecified
#z_factor = "1" # provide a default value if unspecified


# check the exist of wsdem
try:
    if not gp.Exists(wsdem):
        raise "input nonexist"
    if gp.Exists(shield):
        raise "output exist"

    # allowing overwrite intermidiate datasets
    gp.overwriteoutput = 1
    tmppath = os.path.dirname(wsdem)

    #set up gp_extent
    tempEnvironment0 = gp.extent
    gp.extent = wsdem
    #gp.AddMessage ("set gp.extent pass")
    
    # intermidiate rasters... need to determine the path of the wsdem
    xxxhsxxx = tmppath + "\\xxxhsxxx"
    xxxshield0xxx = tmppath + "\\xxxshield0xxx"
    xxxshieldxxx = tmppath + "\\xxxshieldxxx"
    xxtmpsedxx = tmppath + "\\xxtmpsedxx"
    xxtmpsed0xx = tmppath + "\\xxtmpsed0xx"
    #xxtmpsed1xx = tmppath + "\\xxtmpsed1xx"

    #Zero_raster = "0"    
    #gp.Times_sa(wsdem, Zero_raster, xxxshield0xxx)
    gp.CreateConstantRaster_sa(xxxshield0xxx, "0", "INTEGER", wsdem, gp.extent)
    #gp.AddMessage ("set gp.extent pass 2")
    for az in az_list:
        #gp.Times_sa(Zero_raster, wsdem, xxtmpsed0xx)
        gp.CreateConstantRaster_sa(xxtmpsed0xx, "0", "INTEGER", wsdem, gp.extent)
        #gp.Times_sa(Zero_raster, wsdem, xxtmpsedxx)
        gp.CreateConstantRaster_sa(xxtmpsedxx, "0", "INTEGER", wsdem, gp.extent)
        for el in el_list:
            gp.HillShade_sa(wsdem, xxxhsxxx, az, el, "SHADOWS", z_factor)
            zmin = gp.GetRasterProperties_management(xxxhsxxx, "MINIMUM")
            if zmin > 0 : #if zmin > 0, then break the loop
                #print "break"
                break
            else :
                InExpression = xxtmpsed0xx + " + (" + xxxhsxxx + " == 0)"
                gp.SingleOutputMapAlgebra_sa(InExpression, xxtmpsedxx)
                #gp.LessThanEqual_sa(xxxhsxxx, Zero_raster, xxtmpsed1xx)
                #gp.Plus_sa(xxtmpsed0xx, xxtmpsed1xx, xxtmpsedxx)
                InExpression = xxtmpsedxx
                gp.SingleOutputMapAlgebra_sa(InExpression, xxtmpsed0xx)
                #gp.CopyRaster_management(xxtmpsedxx, xxtmpsed0xx, "", "", "", "NONE", "NONE", "")

        #calculate the shielding for the az with different el loop
        InExpression = xxxshield0xxx + " + pow(sin(" + xxtmpsedxx + " * " + el_interval + " * 0.0174532922),3.3)"
        gp.SingleOutputMapAlgebra_sa(InExpression, xxxshieldxxx)
        #gp.CopyRaster_management(xxxshieldxxx, xxxshield0xxx, "", "", "", "NONE", "NONE", "")
        InExpression = xxxshieldxxx
        gp.SingleOutputMapAlgebra_sa(InExpression, xxxshield0xxx)
        #print az
        gp.AddMessage("Finish Azimuth  " + str(az))

    #Calcualte total shielding raster
    az_loop = int(360 / int(az_interval))
    InExpression = "1 - " + xxxshieldxxx + " / " + str(az_loop)
    gp.SingleOutputMapAlgebra_sa(InExpression, shield)

    #kill intermidiate data
    gp.delete_management(xxxhsxxx)
    gp.delete_management(xxxshield0xxx)
    gp.delete_management(xxxshieldxxx)
    gp.delete_management(xxtmpsed0xx)
    #gp.delete_management(xxtmpsed1xx)
    gp.delete_management(xxtmpsedxx)
    #print "kill sucessful"
    gp.AddMessage("Finish shielding calculation!")
    #restore the gp.extent
    gp.extent = tempEnvironment0
except "input nonexist":
    # The input has no features
    #print wsdem + " does not exist!"
    gp.AddMessage(wsdem + " does not exist!")

except "output exist":
    # The input has no features
    #print shield + " already exist!"
    gp.AddMessage(shield + " already exist!")

except:
    # By default any other errors will be caught here
    #print gp.getmessage(2)
    gp.AddMessage(gp.getmessage(2))

#end of the script

