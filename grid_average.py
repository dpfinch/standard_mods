##==============================================================================
## Created by: Douglas Finch
## Created on: 06/02/2014
## Python 2.7
## Program to average out observational flight data to GEOS-Chem resolution
##==============================================================================
## Import Relevant Modules
import numpy as np
import fileimport
import nan_mod
import datetime as dt
from datetime import datetime, timedelta
import geos_info
##==============================================================================

def regrid_obvs(vari,lat,lon,alt,grid):

    # Set the grid size dependant on the resolution (must be string)

    if grid == '2x25':
        i = 91
        j = 144
        l = 47
    if grid == 'NA':
        i = 121
        j = 151
        l = 47

    # Make two arrays of the same size 
    obs  =  np.zeros([i,j,l])
    count = np.zeros([i,j,l])

    ave = np.zeros(len(vari))

    for x in range(len(vari)):
        if vari[x] == np.nan:
            continue
        
        ii = geos_info.lat2grid(lat[x],grid)
        jj = geos_info.lon2grid(lon[x],grid)
        ll = geos_info.lev_info(alt[x]/1000)

        obs[ii,jj,ll] += vari[x]
        count[ii,jj,ll] += 1

    for y in range(len(vari)):
        if vari[y] == np.nan:
            ave[y] == np.nan
            continue
        
        ii = geos_info.lat2grid(lat[y],grid)
        jj = geos_info.lon2grid(lon[y],grid)
        ll = geos_info.lev_info(alt[y]/1000)

        if count[ii,jj,ll] < 2:
            ave[y] == np.nan
            continue  
        
        ave[y] = obs[ii,jj,ll]/count[ii,jj,ll]

    return ave
            
            
