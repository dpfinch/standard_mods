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
import photo_QC
##==============================================================================

def fl_2x25(filename, var_no):
    
    # Define GEOS-Chem Grid:
    gc_lat=np.arange(-90,92,2) # 91 grid points
    gc_lon=np.arange(-180,180,(360/2.5)) # 144 grid points
    
    d=fileimport.nasa_ames(filename) # Import dictionary from file

    # Define GEOS-Chem Grid:
    gc_lat=np.arange(-90,92,2) # 91 grid points
    gc_lon=np.arange(-180,180,2.5) # 144 grid points

    vari=d[var_no]
    time=d[1]
    time=time/60 # Convert seconds to minutes
    lat=d[9]
    lon=d[10]
    
    # Quality check the original variable:
    lon_index1=np.where(lon ==0)
    lon_index2=np.where(lon>360)
    lat_index1=np.where(lat==0)
    lat_index2=np.where(lat>180)

    lon[lon_index2]=np.nan
    lon[lat_index1]=np.nan
    lon[lat_index2]=np.nan

    lat[lon_index1]=np.nan
    lat[lon_index2]=np.nan
    lat[lat_index2]=np.nan

    vari[lon_index1]=np.nan
    vari[lon_index2]=np.nan

    vari[lat_index1]=np.nan
    vari[lat_index2]=np.nan
    
    time[lon_index1]=np.nan
    time[lon_index2]=np.nan

    time[lat_index1]=np.nan
    time[lat_index2]=np.nan
    
    vari=nan_mod.remove(vari)
    lat=nan_mod.remove(lat)
    lon=nan_mod.remove(lon)
    time=nan_mod.remove(time)

    vari[vari<0]=np.nan

    # Make all fields into one array
    all_data=np.zeros([len(vari),4])
    all_data[:,0]=time
    all_data[:,1]=lat
    all_data[:,2]=lon
    all_data[:,3]=vari

    # Set time fields

    time_step=15
    first_time=time[0]-(time[0]%time_step)
    time_count=0
    time_split={}
    ind0=0
    
    for x in range(len(time)):
        if time[x] >= first_time and time[x]< first_time+time_step:
            ind1=x+1
            time_split[time_count]=all_data[ind0:ind1,:]
        else:
            time_count += 1
            ind0=x
            first_time=time[x]

    vari={} # Create emtpy dictionary for the variable to go in
    vari_count=0
 
    for v in time_split.keys():
        
        for yy in range(1,len(gc_lat)+1):
            for xx in range(1,len(gc_lon)+1):
                iteration=0
                temp_index=np.zeros(len(time_split[v]))
                
                for r in time_split[v]:

                    if r[1] >= gc_lat[yy-1] and r[1] < gc_lat[yy] and r[2] >= gc_lon[xx-1] and r[2] < gc_lon[xx]:
                        temp_index[iteration]=1

                    else:
                        temp_index[iteration]=0
                    iteration += 1
                    
                if sum(temp_index)>0:
                    vari_temp=time_split[v][:,3]
                    temp_index=np.where(temp_index==1)
                    vari[vari_count]=vari_temp[temp_index[0]]
                    vari_count +=1
                else:
                    continue

    all_data=[]
    for a in vari.keys():
        temp_ave=vari[a]
##        for n in range(len(temp_ave)):
##            if temp_ave[n] < 0:
##                temp_ave[n] = np.nan
        temp_ave=nan_mod.mean(temp_ave)
        vari[a][:]=temp_ave

        temp_data=vari[a].tolist()
        all_data.extend(temp_data)

    return all_data

##==============================================================================
## Grid-Ave photochemical age
##==============================================================================

           
def photo_age():
    
    # Define GEOS-Chem Grid:
    gc_lat=np.arange(-90,92,2) # 91 grid points
    gc_lon=np.arange(-180,180,(360/2.5)) # 144 grid points

    d=photo_QC.photo_QC()
    st_date=datetime(2010,12,31)

    vari=d['vari']
    time=d['time']
    lat=d['lat']
    lon=d['lon']
    flag=d['flag']

    # Make all fields into one array
    all_data=np.zeros([len(vari),4])
    all_data[:,0]=time
    all_data[:,1]=lat
    all_data[:,2]=lon
    all_data[:,3]=vari

    # Set time fields

    time_step=timedelta(minutes=15)
    temp_time=timedelta(days=time[0])
    t=st_date+temp_time
    t -= timedelta(minutes=t.minute % 15, seconds=t.second, microseconds=t.microsecond)
    first_time = t
    time_count=0
    time_split={}
    ind0=0
    
    for x in range(len(time)):
        times=timedelta(days=time[x])
        times=st_date+times
        
        if times >= first_time and times < first_time+time_step:
            ind1=x+1
            time_split[time_count]=all_data[ind0:ind1,:]
        else:
            time_count += 1               
            ind0=ind1
            first_time=times
            if x == len(time)-1:
                time_split[time_count]=all_data[ind0:ind1+1,:]
      
    vari={} # Create emtpy dictionary for the variable to go in
    vari_count=0
 
    for v in time_split.keys():
        
        for yy in range(1,len(gc_lat)+1):
            for xx in range(1,len(gc_lon)+1):
                iteration=0
                temp_index=np.zeros(len(time_split[v]))
                
                for r in time_split[v]:

                    if r[1] >= gc_lat[yy-1] and r[1] < gc_lat[yy] and r[2] >= gc_lon[xx-1] and r[2] < gc_lon[xx]:
                        temp_index[iteration]=1

                    else:
                        temp_index[iteration]=0
                    iteration += 1 
                if sum(temp_index)>0:
                    vari_temp=time_split[v][:,3]
                    temp_index=np.where(temp_index==1)
                    vari[vari_count]=vari_temp[temp_index[0]]
                    vari_count +=1
                else:
                    continue

    all_data=[]
    for a in vari.keys():
        temp_ave=vari[a]
##        for n in range(len(temp_ave)):
##            if temp_ave[n] < 0:
##                temp_ave[n] = np.nan
        temp_ave=nan_mod.mean(temp_ave)
        vari[a][:]=temp_ave

        temp_data=vari[a].tolist()
        all_data.extend(temp_data)

    d={}
    d['date']=time
    d['p_age']=all_data
    d['flag']=flag

    return d     

##==============================================================================
## Grid average nested run
##==============================================================================

def fl_05x0667(filename, var_no):
    
    # Define GEOS-Chem Grid:
    gc_lat=np.arange(10,70.5,.5) # 91 grid points
    gc_lon=np.arange(-140,-39.4,(2./3.)) # 144 grid points
    
    d=fileimport.nasa_ames(filename) # Import dictionary from file

    vari=d[var_no]
    time=d[1]
    time=time/60 # Convert seconds to minutes
    lat=d[9]
    lon=d[10]
    
    # Quality check the original variable:
    lon_index1=np.where(lon ==0)
    lon_index2=np.where(lon>360)
    lat_index1=np.where(lat==0)
    lat_index2=np.where(lat>180)

    lon[lon_index2]=np.nan
    lon[lat_index1]=np.nan
    lon[lat_index2]=np.nan


    lat[lon_index1]=np.nan
    lat[lon_index2]=np.nan
    lat[lat_index2]=np.nan

    vari[lon_index1]=np.nan
    vari[lon_index2]=np.nan

    vari[lat_index1]=np.nan
    vari[lat_index2]=np.nan
    
    time[lon_index1]=np.nan
    time[lon_index2]=np.nan

    time[lat_index1]=np.nan
    time[lat_index2]=np.nan
    
    vari=nan_mod.remove(vari)
    lat=nan_mod.remove(lat)
    lon=nan_mod.remove(lon)
    time=nan_mod.remove(time)

    vari[vari<0]=np.nan

    # Make all fields into one array
    all_data=np.zeros([len(vari),4])
    all_data[:,0]=time
    all_data[:,1]=lat
    all_data[:,2]=lon
    all_data[:,3]=vari

    # Set time fields

    time_step=10
    first_time=time[0]-(time[0]%time_step)
    time_count=0
    time_split={}
    ind0=0
    
    for x in range(len(time)):
        if time[x] >= first_time and time[x]< first_time+time_step:
            ind1=x+1
            time_split[time_count]=all_data[ind0:ind1,:]
        else:
            time_count += 1
            ind0=x
            first_time=time[x]

    vari={} # Create emtpy dictionary for the variable to go in
    vari_count=0
 
    for v in time_split.keys():
        
        for yy in range(1,len(gc_lat)):
            for xx in range(1,len(gc_lon)):
                iteration=0
                temp_index=np.zeros(len(time_split[v]))
                
                for r in time_split[v]:

                    if r[1] >= gc_lat[yy-1] and r[1] < gc_lat[yy] and r[2] >= gc_lon[xx-1] and r[2] < gc_lon[xx]:
                        temp_index[iteration]=1

                    else:
                        temp_index[iteration]=0
                    iteration += 1
                    
                if sum(temp_index)>0:
                    vari_temp=time_split[v][:,3]
                    temp_index=np.where(temp_index==1)
                    vari[vari_count]=vari_temp[temp_index[0]]
                    vari_count +=1
                else:
                    continue

    all_data=[]
    for a in vari.keys():
        temp_ave=vari[a]
##        for n in range(len(temp_ave)):
##            if temp_ave[n] < 0:
##                temp_ave[n] = np.nan
        temp_ave=nan_mod.mean(temp_ave)

        vari[a][:]=temp_ave

        temp_data=vari[a].tolist()
        all_data.extend(temp_data)

    return all_data
##==============================================================================
## Grid average nested run
##==============================================================================

def fl_05x0667_median(filename, var_no):
    
    # Define GEOS-Chem Grid:
    gc_lat=np.arange(10,70.5,.5) # 91 grid points
    gc_lon=np.arange(-140,-39.4,(2./3.)) # 144 grid points
    
    d=fileimport.nasa_ames(filename) # Import dictionary from file

    vari=d[var_no]
    time=d[1]
    time=time/60 # Convert seconds to minutes
    lat=d[9]
    lon=d[10]
    
    # Quality check the original variable:
    lon_index1=np.where(lon ==0)
    lon_index2=np.where(lon>360)
    lat_index1=np.where(lat==0)
    lat_index2=np.where(lat>180)

    lon[lon_index2]=np.nan
    lon[lat_index1]=np.nan
    lon[lat_index2]=np.nan


    lat[lon_index1]=np.nan
    lat[lon_index2]=np.nan
    lat[lat_index2]=np.nan

    vari[lon_index1]=np.nan
    vari[lon_index2]=np.nan

    vari[lat_index1]=np.nan
    vari[lat_index2]=np.nan
    
    time[lon_index1]=np.nan
    time[lon_index2]=np.nan

    time[lat_index1]=np.nan
    time[lat_index2]=np.nan
    
    vari=nan_mod.remove(vari)
    lat=nan_mod.remove(lat)
    lon=nan_mod.remove(lon)
    time=nan_mod.remove(time)

    vari[vari<0]=np.nan

    # Make all fields into one array
    all_data=np.zeros([len(vari),4])
    all_data[:,0]=time
    all_data[:,1]=lat
    all_data[:,2]=lon
    all_data[:,3]=vari

    # Set time fields

    time_step=10
    first_time=time[0]-(time[0]%time_step)
    time_count=0
    time_split={}
    ind0=0
    
    for x in range(len(time)):
        if time[x] >= first_time and time[x]< first_time+time_step:
            ind1=x+1
            time_split[time_count]=all_data[ind0:ind1,:]
        else:
            time_count += 1
            ind0=x
            first_time=time[x]

    vari={} # Create emtpy dictionary for the variable to go in
    vari_count=0
 
    for v in time_split.keys():
        
        for yy in range(1,len(gc_lat)):
            for xx in range(1,len(gc_lon)):
                iteration=0
                temp_index=np.zeros(len(time_split[v]))
                
                for r in time_split[v]:

                    if r[1] >= gc_lat[yy-1] and r[1] < gc_lat[yy] and r[2] >= gc_lon[xx-1] and r[2] < gc_lon[xx]:
                        temp_index[iteration]=1

                    else:
                        temp_index[iteration]=0
                    iteration += 1
                    
                if sum(temp_index)>0:
                    vari_temp=time_split[v][:,3]
                    temp_index=np.where(temp_index==1)
                    vari[vari_count]=vari_temp[temp_index[0]]
                    vari_count +=1
                else:
                    continue

    all_data=[]
    for a in vari.keys():
        temp_ave=vari[a]

        temp_ave=nan_mod.median(temp_ave)
        vari[a][:]=temp_ave

        temp_data=vari[a].tolist()
        all_data.extend(temp_data)

    return all_data

##==============================================================================
## Grid average nested run just over a flight - no time averaging
##==============================================================================

def fl_05x0667_no_time(filename, var_no):
    
    # Define GEOS-Chem Grid:
    gc_lat=np.arange(10,70.5,.5) # 91 grid points
    gc_lon=np.arange(-140,-39.4,(2./3.)) # 144 grid points
    
    d=fileimport.nasa_ames(filename) # Import dictionary from file

    vari=d[var_no]
    lat=d[9]
    lon=d[10]
    
    # Quality check the original variable:
    lon_index1=np.where(lon ==0)
    lon_index2=np.where(lon>360)
    lat_index1=np.where(lat==0)
    lat_index2=np.where(lat>180)

    lon[lon_index2]=np.nan
    lon[lat_index1]=np.nan
    lon[lat_index2]=np.nan


    lat[lon_index1]=np.nan
    lat[lon_index2]=np.nan
    lat[lat_index2]=np.nan

    vari[lon_index1]=np.nan
    vari[lon_index2]=np.nan

    vari[lat_index1]=np.nan
    vari[lat_index2]=np.nan
    
    vari=nan_mod.remove(vari)
    lat=nan_mod.remove(lat)
    lon=nan_mod.remove(lon)

    vari[vari<0]=np.nan

    # Make all fields into one array
    all_data=np.zeros([len(vari),3])
    all_data[:,0]=lat
    all_data[:,1]=lon
    all_data[:,2]=vari

    vari={} # Create emtpy dictionary for the variable to go in
    vari_count=0
        
    for yy in range(1,len(gc_lat)):
        for xx in range(1,len(gc_lon)):
            iteration=0
            temp_index=np.zeros(len(all_data[:,0]))

            for r in range(len(all_data[:,0])):

                if all_data[r,0] >= gc_lat[yy-1] and all_data[r,0] < gc_lat[yy] and all_data[r,1] >= gc_lon[xx-1] and all_data[r,1] < gc_lon[xx]:
                    temp_index[iteration]=1

                else:
                    temp_index[iteration]=0
                iteration += 1
            
            if sum(temp_index)>0:
                vari_temp=all_data[:,2]
                temp_index=np.where(temp_index==1)
                vari[vari_count]=vari_temp[temp_index[0]]
                vari_count +=1
            else:
                continue

    all_data=[]
    for a in vari.keys():
        temp_ave=vari[a]

        temp_ave=nan_mod.median(temp_ave)
        vari[a][:]=temp_ave

        temp_data=vari[a].tolist()
        all_data.extend(temp_data)

    return all_data

##==============================================================================
## Return data that has no averaging but does have NaNs removed
##==============================================================================

def no_ave_nested(filename, var_no):
# Define GEOS-Chem Grid:
    gc_lat=np.arange(10,70.5,.5) # 91 grid points
    gc_lon=np.arange(-140,-39.4,(2./3.)) # 144 grid points
    
    d=fileimport.nasa_ames(filename) # Import dictionary from file

    vari=d[var_no]
    time=d[1]
    time=time/60 # Convert seconds to minutes
    lat=d[9]
    lon=d[10]
    
    # Quality check the original variable:
    lon_index1=np.where(lon ==0)
    lon_index2=np.where(lon>360)
    lat_index1=np.where(lat==0)
    lat_index2=np.where(lat>180)

    lon[lon_index2]=np.nan
    lon[lat_index1]=np.nan
    lon[lat_index2]=np.nan


    lat[lon_index1]=np.nan
    lat[lon_index2]=np.nan
    lat[lat_index2]=np.nan

    vari[lon_index1]=np.nan
    vari[lon_index2]=np.nan

    vari[lat_index1]=np.nan
    vari[lat_index2]=np.nan
    
    time[lon_index1]=np.nan
    time[lon_index2]=np.nan

    time[lat_index1]=np.nan
    time[lat_index2]=np.nan
    
    vari=nan_mod.remove(vari)
    lat=nan_mod.remove(lat)
    lon=nan_mod.remove(lon)
    time=nan_mod.remove(time)

    return vari

##==============================================================================
## END OF PROGRAM
##==============================================================================
