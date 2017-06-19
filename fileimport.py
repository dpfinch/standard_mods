##
##==============================================================================
##Created on: 12/02/13
##Created By: Douglas Finch
##Python 2.7
##Module with different routines to import different files
##==============================================================================
##
## File types to import:
## NASA Ames format (.na) - eg. BORTAS merge files
## NASA Ames format small (.na) - eg. P. Palmers planelog files
## GEOS-Chem planeflight (plane.log.YYYYMMDD) - eg. GEOS-Chem output
## GEOS-Chem planeflight pressure values - have to be proccessed
## Netcdf file from GEOS-Chem eg. ctm.nc (converted in IDL from ctm.bpch)
## Text files of Obvs Vs GEOS-Chem
## ESA Fire location files
## Import Photochemical Age calucalted by Mark Parrington for BORTAS
## Import binary punch files from GEOS-Chem output
## Import station data from GEOS-Chem
## Import data from CO2 sensor text file
##==============================================================================
##
## Import standard modules:
import numpy as np
import scipy
from datetime import datetime
import time
import geos_info
##==============================================================================
## NASA AMES format import starts here (BORTAS)
##==============================================================================
def nasa_ames(filename):
    
    f=open(filename)    #Open the data file
    f.seek(0)           # Find the beginning of the file
    x=f.readline()      # Read the first line of the data file (this tells us which line of
                        # the file the data starts
    f.close             # close the file
    li=int(x[0:15])      # Convert whatever number

    f=np.loadtxt(filename, skiprows=li)      # Open and read in the file, skipping to the data
    d={}                                    # Create empty dictionary

    for x in range(0, f.shape[1]):
        d[x]=f[:,x]     # Loop through the columns of the datafile, putting each one into
                        #a dictionary index

    return d

##==============================================================================
## NASA AMES small format import starts here (BORTAS)
##==============================================================================
def nasa_ames_small(filename):
    arr = [np.array(map(str, line.split())) for line in open(filename)]
    li=int(arr[0][0])

    a={}
    num=0
    for x in range(li,len(arr),2):
         a[num]=np.concatenate((arr[x],arr[x+1]))
         num=num+1

    data=np.empty((len(a),len(a[0])))
    data[:]=np.nan
    for x in range (len(a)):
        for y in range(len(a[0])):
                    data[x,y]=float(a[x][y])
    
    d={}
    for x in range(data.shape[1]):
        d[x]=data[:,x]

    return d

##==============================================================================
## GEOS-Chem planeflight format import starts here
##==============================================================================
def plane_old(filename):

    gcf=np.loadtxt(filename,skiprows=1, dtype='str')
    arr_y=gcf.shape[0]
    arr_x=gcf.shape[1]-2
    arr_shape=[arr_y,arr_x]

    gcarr=np.zeros(shape=(arr_shape))    # Create an empty array with float data type
    for x in range(gcf.shape[0]):
            for y in range(2,gcf.shape[1]):
                y_dim=y-2
                if gcf[x,y] == '*******':
                    gcarr[x,y_dim]=np.nan
                else:
                    gcarr[x,y_dim]=float(gcf[x,y])

    gcd={} # Create empty dictionary for GEOS-Chem data

    for x in range(0, gcarr.shape[1]):
        gcd[x]=gcarr[:,x]    # Loop through the columns of the datafile, putting each one into
#a dictionary index

    return gcd # RETURNS DATA FOR DATES NOT FLIGHT NO.

##==============================================================================
## GEOS-Chem planeflight format import starts here - NEW
##==============================================================================
def plane(filename, std_sim= True):

    gcf=np.loadtxt(filename, dtype='str')
    gcd={} # Create empty dictionary for GEOS-Chem data

    for x in range(len(gcf[0,:])):
        if gcf[0,x] == 'TYPE':
            gcd[gcf[0,x]] = gcf[1:,x]
        elif gcf[0,x] == 'YYYYMMDD':
            gcd[gcf[0,x]] = [datetime.strptime(i,'%Y%m%d') for i in gcf[1:,x]]
        elif gcf[0,x] == 'HHMM':
            gcd[gcf[0,x]] = [datetime.strptime(i,'%H%M') for i in gcf[1:,x]]
        elif gcf[0,x][:3] == 'TRA':
            if std_sim:
                name = geos_info.stnd_tracers()[int(gcf[0,x][-3:])-1][1]
            else:
                name = gcf[0,x]
            gcd[name] = [float(i) for i in gcf[1:,x]]
        else:
            gcd[gcf[0,x]] = [float(i) for i in gcf[1:,x]]
    
    return gcd # RETURNS DATA FOR DATES NOT FLIGHT NO.

##==============================================================================
## GEOS-Chem planeflight format import - all data 
##==============================================================================
def all_plane(filename):

    gcf=np.loadtxt(filename,dtype='str')
    d= dict((i,[]) for i in gcf[0,:]) # Create dictionary with tracers as keys

    for x in range(len(gcf[0,:])):
        if gcf[0,x] != 'TYPE' and gcf[0,x] != 'HHMM' and gcf[0,x] != 'YYYYMMDD':
            float_data=[float(y) for y in gcf[1:,x]]
            d[gcf[0,x]]=float_data
        else:
            d[gcf[0,x]] = list(gcf[1:,x])

    return d # RETURNS DICT FOR DATES NOT FLIGHT NO.


##==============================================================================
## GEOS-Chem planeflight format import starts here with pressure data
##==============================================================================
def plane_pres(filename):

    # Import just the 1st(col=0) and 7th (col=6) columns from file
    gcf=np.loadtxt(filename,skiprows=1, dtype='str', usecols=(0,6))
    pres=gcf[:,1] #  Pressure is the second column

    pres_fl=np.zeros(len(pres)) # Create empty array the same size
                   
    for x in range(0,len(pres)): # Loop through the data
	if pres[x] == '*******':
		pres_fl[x]=np.nan # If not data then input nan
	elif float(pres[x]) > 1200: # If impossible data then input nan
		pres_fl[x]=np.nan
	else:
		pres_fl[x] = float(pres[x]) #convert to float
                 
    return pres_fl
##==============================================================================
## netCDF file format import starts here
##==============================================================================
def nc(filename):
    from scipy.io import netcdf

    f=netcdf.netcdf_file(filename,'r')
    var=f.variables.keys()

    d={}
    for x in range(len(var)):
        data=f.variables[var[x]]
        d[var[x]]=data[:]

    return d
##==============================================================================
## Text file 'versus' import starts here
##==============================================================================
def versus(filename):
    f=np.loadtxt(filename)

    d={}
    d['obvs']=f[:,0]
    d['mod']=f[:,1]

    return d
##==============================================================================
## Text file 'versus' import starts here
##==============================================================================
def fire_loc(yr,mn):
    dirname='/home/s1251441/Documents/BORTAS/fire_loc/'
    if len(str(mn))==1:
        month='0'+str(mn)
    else:
        month=str(mn)
    filename=dirname+str(yr)+month+'ALGO1.FIRE'

    f=np.loadtxt(filename)

    d={}        # Create empty dictionary

    for x in range(0, f.shape[1]):
        d[x]=f[:,x]     # Loop through the columns of the datafile, putting each one into
                        #a dictionary index

    return d

##==============================================================================
## Photochemical Age import starts here
##==============================================================================
def photochem_age():
    filename='/home/s1251441/Documents/BORTAS/age_of_air/mp_chem_merged-data_faam_201107_r3_b616-b632_v01_was-time-all.na'

    f=open(filename)
    f.seek(0)
    c=0
    l={}
    for line in f:
        l[c]=line
        c+=1

    f.close()

    # Create empty data array
    data=np.zeros([8,((len(l)-34)/4)])

    it=0
    
    for n in range(34,len(l),4):
        data[0,it]=float(l[n][:16]) # Get the date
        data[1,it]=float(l[n][16:29]) # Longitude
        data[2,it]=float(l[n][29:42]) # Latitude
        data[3,it]=float(l[n][42:55]) # Altitude
        data[4,it]=float(l[n+3][30:39]) # Photochem age
        data[5,it]=float(l[n][55:]) # Ozone mixing ratio
        data[6,it]=float(l[n+3][39:]) # Plume flag
        data[7,it]=float(l[n][55:]) # Ozone enhancement ratio
        it+=1

    d={}
    d['date']=data[0,:]
    d['lon']=data[1,:]
    d['lat']=data[2,:]
    d['alt']=data[3,:]
    d['p_age']=data[4,:]
    d['o3']=data[5,:]
    d['flag']=data[6,:]
    d['o3_e']=data[7,:]
    return d

##==============================================================================
## BPCH import starts here
##==============================================================================
def bpch(fi,group,tracer):
    from bpch import bpch
##    print 'Using file: '+fi
    bc=bpch(fi)
    gr=bc.groups[str(group)]

    tracer=str(tracer)
    
    data=gr.variables[tracer]
    lat=bc.variables['latitude']
    lon=bc.variables['longitude']
    tau0 = bc.variables['tau0']
    layer = bc.variables['layer']


    return data, lat, lon, layer, tau0

##==============================================================================
## Station file import starts here
##==============================================================================
def station(filename):
    station=[]
    return station

##==============================================================================
## CO2 sensor file import starts here
##==============================================================================
def co2sensor(filename):
    from datetime import datetime
    
    f=np.loadtxt(filename,dtype=str)
    data=np.zeros([len(f),7])

    for x in range(len(f)):
        temp=f[x].split(',')
        for y in range (len(temp)):
            data[x,y]=float(temp[y])
    d={}
    d['co2']=data[:,0]
    
    date=[]
    for z in range(len(f)):
        date.append(datetime(int(data[z,1]),int(data[z,2]),int(data[z,3]),
                             int(data[z,4]),int(data[z,5]),int(data[z,6])))
    
    d['date']=date

    return d

##==============================================================================
## A updated NASA AMES format import starts here (BORTAS)
##==============================================================================
def nasa_ames_upgrade(filename):
    from itertools import islice
    
    with open(filename) as plane_file:
        head = list(islice(plane_file,10)) # Get number of variables (10th line)
    num_var = int(head[-1])
    var_line_start = int(head[0][:15]) # Get where the variables start

    # Find names of all the variables
    with open(filename) as plane_file:
        head = list(islice(plane_file,13 + num_var ))

    var_list = [head[8]] # First variable is StartTime
    var_list.extend(head[12:-1])
    
    all_vars = {} # Empty dictionary for all the variables

    f=np.loadtxt(filename, skiprows=var_line_start)      # Open and read in the file, skipping to the data                                   # Create empty dictionary

    for x,v in enumerate(var_list):
        all_vars[v.rstrip()] = f[:,x]     # Loop through the columns of the datafile, putting each one into
                        #a dictionary index

    return all_vars


##==============================================================================
## END OF PROGRAM
##==============================================================================
