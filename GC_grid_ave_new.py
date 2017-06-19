##==============================================================================
## Created by: Douglas Finch
## Created on: 24/03/2016
## Python 2.7
## A new Program to average out observational flight data to GEOS-Chem resolution
##==============================================================================
## Import Relevant Modules
import numpy as np
import datetime as dt
from datetime import datetime, timedelta
import geos_info
import math
##==============================================================================
## Grid average nested run
##==============================================================================

def fl_05x0666(vari,vari_name,lat,lon, debug = False):

    no_ave_list = ['YYYYMMDD','HHMM','LAT','LON','TYPE','PRESS']
    if vari_name in no_ave_list:
        return vari
    else:
    
        vari = np.asarray(vari)
        vari[np.where(vari<0)] = np.nan
        # Define GEOS-Chem Grid:
        gc_lat=np.arange(10,70.5,.5) # 121 grid points
        gc_lon=np.arange(-140,-39.4,(2./3.)) # 151 grid points

        # Make all fields into one array
        all_data=np.zeros([len(vari),3])
        all_data[:,0]=lat
        all_data[:,1]=lon
        all_data[:,2]=vari

        vari_dict={} # Create emtpy dictionary for the variable to go in
        vari_count=0

        count_arr = np.zeros([len(gc_lat),len(gc_lon)])
        tracer_arr = np.zeros([len(gc_lat),len(gc_lon)])

        for r in range(len(vari)):
            if math.isnan(vari[r]):
                continue
            
            lat_grid = geos_info.lat2grid(lat[r],'NA')
            lon_grid = geos_info.lon2grid(lon[r],'NA')

            count_arr[lat_grid,lon_grid] += 1
            tracer_arr[lat_grid,lon_grid] += vari[r]

        avg_tracer = []
        for r in range(len(vari)):
            if math.isnan(vari[r]):
                avg_tracer.append(np.nan)
            else:
                lat_grid = geos_info.lat2grid(lat[r],'NA')
                lon_grid = geos_info.lon2grid(lon[r],'NA')

                avg_tracer.append(tracer_arr[lat_grid,lon_grid]/count_arr[lat_grid,lon_grid])

        return avg_tracer

def fl_2x25(vari,vari_name,lat,lon, debug = False):

    no_ave_list = ['YYYYMMDD','HHMM','LAT','LON','TYPE','PRESS']
    if vari_name in no_ave_list:
        return vari
    else:
    
        vari = np.asarray(vari)
        vari[np.where(vari<0)] = np.nan
        # Define GEOS-Chem Grid:
        gc_lat=np.arange(-90,92,2) # 121 grid points
        gc_lon=np.arange(-180,180,2.5) # 151 grid points

        # Make all fields into one array
        all_data=np.zeros([len(vari),3])
        all_data[:,0]=lat
        all_data[:,1]=lon
        all_data[:,2]=vari

        vari_dict={} # Create emtpy dictionary for the variable to go in
        vari_count=0

        count_arr = np.zeros([len(gc_lat),len(gc_lon)])
        tracer_arr = np.zeros([len(gc_lat),len(gc_lon)])

        for r in range(len(vari)):
            if math.isnan(vari[r]):
                continue
            
            lat_grid = geos_info.lat2grid(lat[r],'2x25')
            lon_grid = geos_info.lon2grid(lon[r],'2x25')

            count_arr[lat_grid,lon_grid] += 1
            tracer_arr[lat_grid,lon_grid] += vari[r]

        avg_tracer = []
        for r in range(len(vari)):
            if math.isnan(vari[r]):
                avg_tracer.append(np.nan)
            else:
                lat_grid = geos_info.lat2grid(lat[r],'2x25')
                lon_grid = geos_info.lon2grid(lon[r],'2x25')

                avg_tracer.append(tracer_arr[lat_grid,lon_grid]/count_arr[lat_grid,lon_grid])

        return avg_tracer
     
##        for yy in range(1,len(gc_lat)):
##            for xx in range(1,len(gc_lon)):
##                iteration=0
##                temp_index=np.zeros(len(all_data[:,0]))
##
##                for r in range(len(all_data[:,0])):
##
##                    if all_data[r,0] >= gc_lat[yy-1] and all_data[r,0] < gc_lat[yy] and all_data[r,1] >= gc_lon[xx-1] and all_data[r,1] < gc_lon[xx]:
##                        temp_index[iteration]=1
##
##                    else:
##                        temp_index[iteration]=0
##                    iteration += 1
##                
##                if sum(temp_index)>0:
##                    vari_temp=all_data[:,2]
##                    temp_index=np.where(temp_index==1)
##                    vari_dict[vari_count]=vari_temp[temp_index[0]]
##                    vari_count +=1
##                else:
##                    continue
##
##        avg_data=[]
##
##        for a in vari_dict.keys():
##            temp_ave=vari_dict[a]
##
##            temp_ave=np.nanmean(temp_ave)
##            vari_dict[a][:]=temp_ave
##
##            temp_data=vari_dict[a].tolist()
##            avg_data.extend(temp_data)
##
##        # Insert nans where the lat/lon was buggered
##        out_array = np.zeros(len(lon))
##        out_array[:] = np.nan
##        avg_data_index = 0
##        x = 0 
##        while x < len(lon):
##            if lon[x] > -40:
##                x += 1
##            else:
##                out_array[x] = avg_data[avg_data_index]
##                x += 1
##                avg_data_index += 1
##
##        if debug:
##            return avg_data, vari, vari_dict,temp_data,all_data, lon, lat, out_array
##        else:
##            return out_array
