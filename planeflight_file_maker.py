##
##==============================================================================
##Created on: 07/03/13
##Created By: Douglas Finch
##Python 2.7
##Create flight path file to input into GEOS-Chem
##Updated version of geos_flight_conv.py
##
##This program will create flight path files for each date in reqiured time
##series GEOS-Chem is running for
##Flights that span over two dates will be split into seperate files
##
##==============================================================================
##
## Import standard modules:
import numpy as np
import os.path
import fileimport
import datetime as dt
import time
from datetime import datetime
import geos_info
##==============================================================================

# Define the start date and the end date for the range of dates to be used
# Format: YYYYMMDD. (String)
start='20110714'
end='20110801'
# Define the first flight number and the last flight number
# Format: FAAM flight no. Ignoreing the 'b'. (Integer)
st_fl=618
end_fl=628

# Get the date this program is run
now=datetime.now()
year_now=now.year
month_now=now.month
day_now=now.day

# Split the dates given above into individual components
st_yr=int(start[0:4])
end_yr=int(end[0:4])
st_mn=int(start[4:6])
end_mn=int(end[4:6])
st_day=int(start[6:])
end_day=int(end[6:])

# Covert the start and end dates into date formats
st_date=dt.date(st_yr,st_mn,st_day)
end_date=dt.date(end_yr,end_mn,end_day)
# Count the date range between start and end
day_count=(end_date-st_date).days+1
##==============================================================================
# Define the variables to be used in GEOS-Chem

var = [1,2,3,4,5,6,7,8,9,10,13,14,16,19,20,21,22,54,64,65,66]
var = [str(i).zfill(3) for i in var]

##==============================================================================

# Create an empty lists to add in all the data
# Make huge arrays with all the data in different variables
all_flno=[] # Flight numbers
all_date=[] # Flight date
all_time=[] # Flight time
all_lat=[]  # Flight lats
all_lon=[]  # Flight lons
all_pres=[] # Flght pressure
all_alt=[]

# Loop through all the range of flights and the dates and check if file exisits
flights=np.arange(st_fl,end_fl+1)

for fl_no in(flights):
    for x in(st_date+dt.timedelta(n) for n in range(day_count)):
        date=x.strftime("%Y%m%d")
    
        # Define the file
        filedir='/home/s1251441/BADC/bortas_data_merge/'
        filename='merged-data_faam_'+date+'_r2_b'+str(fl_no)+'_060s.na'

        # Check if the file exists
        f_test=os.path.isfile(filedir+filename)
        # If file does exist - open it and add contents to various arrays
        if f_test == True:
            plane_fi=fileimport.nasa_ames(filedir+filename)

            for z in range(0,len(plane_fi[0])): # Loop through all points
                if plane_fi[2][z] > 86400: # If the time is over midnight then:
                    str_date=str(plane_fi[3][z]) # Change the date to string
                    yr_split=int(str_date[0:4]) # Split the date into yr, mn & day
                    mn_split=int(str_date[4:6])
                    day_split=int(str_date[6:8])
                    real_date= dt.datetime(yr_split,mn_split,day_split)
                    delta=dt.timedelta(days=1)
                    new_date=real_date+delta # Add day on if time over midnight
                    str_dt=new_date.strftime("%Y%m%d")
                    plane_fi[3][z]=int(str_dt)

                fl_type='b'+str(fl_no)
                all_flno.append(fl_type)
                all_date.append(plane_fi[3][z])
                all_time.append(plane_fi[2][z])
                all_lat.append(plane_fi[9][z])
                all_lon.append(plane_fi[10][z])
                all_pres.append(plane_fi[7][z])
                all_alt.append(plane_fi[11][z])

# Convert altitude from GPS into pressure from standard info from GC levels
# This is an assumption that the model levels are constant pressure values
# This assumption is valid due to the space between the levels - only surface
# level maybe invalid - but there is very little flight data for this
pres_alt=np.zeros(len(all_alt))

for a in range(len(all_alt)):
    pres_alt[a]=geos_info.pres_alt(all_alt[a]/1000)

##==============================================================================                        
# Split data into dates

for x in(st_date+dt.timedelta(n) for n in range(day_count)):
    date=x.strftime("%Y%m%d")
    ddmmyyyy=x.strftime("%d-%m-%Y") # Define the date
    fl_date=float(date)# Turn date into float
    
    # Name the directory and file name for the new file to be made
    new_dir='/home/s1251441/Documents/prod_loss/v9-02.std/plane_input/'
    new_file=new_dir+'Planeflight.dat.'+date

    f=open(new_file,'w') # Open file with date and add Header lines
    print>>f, 'Planeflight.dat'
    print>>f, 'Douglas Finch'
    print>>f, 'Created on: ',year_now,'-',month_now,'-',day_now
    print>>f, '-------------------------------------------------------------------------------'
    print>>f, len(var)
    print>>f, '-------------------------------------------------------------------------------'

    # Print the variables going to be outputted from the run
    for j in var:
        print>>f, 'TRA_'+j
    print>>f, '-------------------------------------------------------------------------------'
    print>>f, 'Time and Location of flight path'
    print>>f, '-------------------------------------------------------------------------------'
    print>>f, 'Point Type  DD-MM-YYYY HH:MM   LAT    LON    PRESS'

    point=0 # Set the point counter to zero


    try: # If date matches anything in the array then do the following
        st_cell=all_date.index(fl_date) # Find where first cell the date matches
        tot_cell=all_date.count(fl_date) # Find total no. cells with matching date

        for y in range(st_cell, tot_cell+st_cell):
            
            point=point+1 # Increase the point by one
            fl=all_flno[y] # Find the flight number
            #ddmmyyyy=x.strftime("%d-%m-%Y") # Define the date
            hhmm=time.strftime("%H:%M", time.gmtime(all_time[y])) # Define the time
            lat=('%.2f' %(float(all_lat[y]))) # Define the lat
            lon=('%.2f' %(float(all_lon[y]))) # Define the lon
            test_lat=float(lat) # Create 'test' variables 
            test_lon=float(lon) # To test whether the number if out of line
            if test_lat >360. or test_lat == 0. or test_lat < -360.: # if lat or lon is incorrect
                point=point-1
                continue
            if test_lon >360. or test_lon == 0.or test_lon < -360.:
                point=point-1
                continue
            #pres=('%.2f' %(float(all_pres[y]))) # Define the pressure
            pres=('%.2f' %(float(pres_alt[y]))) # Define the pressure
            # Print the values into the file
            print>>f, '{0:5d} {1:5s}'.format(point, fl), ddmmyyyy,'{0:7s}'.format(hhmm),\
                      '{0:6s}'.format(lat), '{0:6s}'.format(lon), '{0:6s}'.format(pres)
    
            # Print the closing line
        print>>f,'99999 END   0- 0- 0    0 :0    0.00   0.00   0.00'
        f.close() # Close the file
    except:
        # If no date is matched then print the closing file and continue       
        print>>f,'99999 END   0- 0- 0    0 :0    0.00   0.00   0.00'    
        f.close()
        continue
##==============================================================================
## END OF PROGRAM
##==============================================================================
