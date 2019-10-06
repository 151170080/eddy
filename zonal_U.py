import netCDF4 as nc
import Ngl
import os, re
import numpy as np
from netCDF4 import num2date
from datetime import datetime

def nice_lat_labels(lats):
    """ Add the labels for the X axis
    """
    latstrs = []
    for lat in lats:
        if lat > 0:
            latstrs.append("{}~S~o~N~N".format(np.fabs(lat)))
        elif lat < 0:
            latstrs.append("{}~S~o~N~S".format(np.fabs(lat)))
        else:
            latstrs.append("{}~S~o~N~".format(np.fabs(lat)))
    return latstrs

def nice_lev_labels(levs):
    """ Add the labels for the Y axis
    """
    levstrs=[]
    for lev in levs:
        levstrs.append("{}".format(np.fabs(lev)))
    return levstrs

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

# read T from nc fie
data = nc.Dataset(fread_p+fname,"r")
#air_T = data.variables["air"]
U = data.variables["uwnd"]
levs = data.variables["level"][:]
lats = data.variables["lat"][:]
times = data.variables["time"]

# air[time,level,lat,lon]. Firstly mean at the time dim,and then at longitude dim.
#zonalMean_T = air_T[:,:,:,:].mean(axis=3) 
zonalMean_U = U[:,:,:,:].mean(axis=3)

# zonalMean_T[time,level,lat]
temp = {"spring":0,"summer":0,"autumn":0,"winter":0}
dates = num2date(times[:],units=times.units)
minval = {}
maxval = {}
i = 0
for k in temp:
    for time in separate_month(times)[i]:
        t_index = np.where(dates==time)
        v = temp[k]
        v = v +zonalMean_U[t_index,:,:]
        temp[k] = v 
        del v
    temp[k] = temp[k]/len(separate_month(times)[i])
    minval[k] = int(np.amin(temp[k]))
    maxval[k] = int(np.amax(temp[k]))
    i = i+1

#    Mean_T = sp_temp/len(separate_month(times)[i])
#    print(Mean_T)

inc = 5

L_lats = np.arange(-80,100,20)
L_levs = [1000,500,200,100,50,30,10]


wks_type = "png"
wks_name = "Mean_U"
wks = Ngl.open_wks(wks_type,wks_name)

res = Ngl.Resources()
#resources.nglDraw  = False      # Turn off draw for the individual plots
#resources.nglFrame = False

#res.tiMainString = "MAM Zonal Mean Temperature from 1979 to 2019 "
res.tiMainFontHeightF = 0.024
res.cnLevelSelectionMode  = "ManualLevels"

#res.cnMinLevelValF = minval
#res.cnMaxLevelValF = maxval
#res.cnLevelSpacingF       =  inc

res.cnFillOn              =  True
res.cnLineLabelsOn        =  False
res.cnInfoLabelOn         =  False
res.cnFillPalette         = "BlueWhiteOrangeRed"
res.pmLabelBarOrthogonalPosF = -0.03

res.sfXArray              = lats
res.sfYArray              = levs

res.trYReverse            = True          #-- reverse the Y axis
res.nglYAxisType          = "LogAxis"     #-- y axis log
res.tiYAxisString         = "pressure (hPa)"
res.nglPointTickmarksOutward = True       #-- point tickmarks out

res.tmYLMode              = "Explicit"
res.tmXBMode              = "Explicit"
res.tmYLValues            = L_levs
res.tmXBValues            = L_lats
res.tmYLLabels            = nice_lev_labels(L_levs)
res.tmXBLabels            = nice_lat_labels(L_lats)

res.vpWidthF = 0.8                       # Set width and height of plot.
res.vpHeightF = 0.4
res.tmYROn = False            # Turn off right tickmarks.
res.tmXTOn = False            # Turn off top tickmarks.

res.tmXBLabelFontHeightF  = 0.015        # - make font smaller
res.tmYLLabelFontHeightF  = 0.015

# for MAM
res.tiMainString = "MAM Zonal Mean U from 1979 to 2019"
res.cnMinLevelValF = minval["spring"]
res.cnMaxLevelValF = maxval["spring"]
res.cnLevelSpacingF       =  inc

plot1 = Ngl.contour(wks,temp["spring"][0,0,:,:],res)

# for JJA
res.tiMainString = "JJA Zonal Mean U from 1979 to 2019"
res.cnMinLevelValF = minval["summer"]
res.cnMaxLevelValF = maxval["summer"]
res.cnLevelSpacingF       =  inc

plot2 = Ngl.contour(wks,temp["summer"][0,0,:,:],res)

# for SON
res.tiMainString = "SON Zonal Mean U from 1979 to 2019"
res.cnMinLevelValF = minval["autumn"]
res.cnMaxLevelValF = maxval["autumn"]
res.cnLevelSpacingF       =  inc

plot3 = Ngl.contour(wks,temp["autumn"][0,0,:,:],res)

# for DJF
res.tiMainString = "DJF Zonal Mean U from 1979 to 2019"
res.cnMinLevelValF = minval["winter"]
res.cnMaxLevelValF = maxval["winter"]
res.cnLevelSpacingF       =  inc

plot4 = Ngl.contour(wks,temp["winter"][0,0,:,:],res)


Ngl.end()
