import netCDF4 as nc
import Ngl
import os, re
import numpy as np
from netCDF4 import num2date
from datetime import datetime
import numpy

# set resources common for contour plots
def set_common_resources():
    res                        = Ngl.Resources()

    res.cnFillOn               = True
    res.cnFillPalette          = "BlueYellowRed"

    res.cnLinesOn              = False
    res.cnLineLabelsOn         = False
    res.cnInfoLabelOn          = False

    res.lbOrientation          = "Horizontal"

    return(res)

def separate_month(times):
    """differ the seasons
    """
    dates = num2date(times[:],units=times.units)
    spring = []
    summer = []
    autumn = []
    winter = []
    for date in dates[:]:
        if date.strftime("%Y-%m").split('-')[1] in ["06","07","08"] :
            summer.append(date)
        elif date.strftime("%Y-%m").split('-')[1] in ["12","01","02"] :
            winter.append(date)
        elif date.strftime("%Y-%m").split('-')[1] in ["03","04","05"] :
            spring.append(date)
        else :
            autumn.append(date)
    return (tuple(spring),tuple(summer),tuple(autumn),tuple(winter))

fread_p = "/Users/zjkang/python_program/eddy/"
#fname = "air.mon.mean.nc"
fname = "uwnd.mon.mean.nc"

# read T from nc file
data = nc.Dataset(fread_p+fname, "r")
#air_T = data.variables["air"][:,:,:,:]
U = data.variables["uwnd"][:,:,:,:]
lats = data.variables["lat"]
lons = data.variables["lon"]
times = data.variables["time"]

# air has 4 dims:time,level,lat,lon.

temp = {"spring":0,"summer":0,"autumn":0,"winter":0}
dates = num2date(times[:],units=times.units)
minval = {}
maxval = {}
i = 0
for k in temp:
    for time in separate_month(times)[i]:
        t_index = np.where(dates==time)
        v = temp[k]
        v = v + U[t_index,:,:,:]
        temp[k] = v
        del v

    temp[k] = temp[k]/len(separate_month(times)[i])
    minval[k] = int(np.amin(temp[k]))
    maxval[k] = int(np.amax(temp[k]))
    i = i + 1

wks_type = "png"
wks = Ngl.open_wks(wks_type,"U_winter")

res = set_common_resources()

# set resource for the base plot
bres = set_common_resources()
bres.mpFillOn          = False 
bres.tiMainFontHeightF = 0.018
bres.cnFillOpacityF    = 0.5 

# for 850 hPa in spring
U_850,lonnew = Ngl.add_cyclic(temp["winter"][0,0,2,:,:],lons[:])
bres.tiMainString      = "DJF Mean U Wind (m/s) at 850 hPa from 1979 to 2009"

bres.sfXArray          = lonnew[:]
bres.sfYArray          = lats[:]
bres.cnMinLevelValF = minval["winter"]
bres.cnMaxLevelValF = maxval["winter"]
bres.cnLevelSpacingF       =  3

plot1 = Ngl.contour_map(wks,U_850,bres)

#for 500 hPa
U_500,lonnew = Ngl.add_cyclic(temp["winter"][0,0,5,:,:],lons[:])
bres.tiMainString      = "DJF Mean U Wind (m/s) at 500 hPa from 1979 to 2009"
bres.cnLevelSpacingF       =  3
plot2 = Ngl.contour_map(wks,U_500,bres)

# for 100 hPa
T_100,lonnew = Ngl.add_cyclic(temp["winter"][0,0,11,:,:],lons[:])
bres.tiMainString      = "DJF Mean U Wind (m/s) at 100 hPa from 1979 to 2009"
bres.cnLevelSpacingF       =  3
plot3 = Ngl.contour_map(wks,T_100,bres)

# for 1000 hPa
#T_1000,lonnew = Ngl.add_cyclic(temp["autumn"][0,0,0,:,:],lons[:])
#bres.tiMainString      = "DJF Mean Temperature (K) at 1000 hPa from 1979 to 2009"
#bres.cnLevelSpacingF       =  5
#plot4 = Ngl.contour_map(wks,T_1000,bres)
Ngl.end()
