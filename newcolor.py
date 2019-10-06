import os, numpy
import netCDF4 as nc
import Ngl

dirc = Ngl.pynglpath("data")
f = nc.Dataset(os.path.join(dirc,"cdf","uv300.nc"),"r")
u = f.variables["U"][1,:,:]
lat = f.variables["lat"][:]
lon = f.variables["lon"][:]

wks_type = "x11"
wks = Ngl.open_wks(wks_type,"newcolor1")
#
#cnres = Ngl.Resources()
#cnres.cnFillOn        = True
#cnres.cnFillPalette   = "BlueYellowRed" 
#cnres.cnLinesOn       = False
#cnres.cnLineLabelsOn  = False
#
#cnres.lbOrientation   = "horizontal"
#cnres.sfXArray        = lon
#cnres.sfYArray        = lat
#
#cnres.mpFillOn               = True
#cnres.mpFillDrawOrder        = "PostDraw"
#cnres.mpLandFillColor        = "Gray"
#cnres.mpOceanFillColor       = "Transparent"
#cnres.mpInlandWaterFillColor = "Transparent"
#contour = Ngl.contour_map(wks,u,cnres)
#
#Ngl.end()

