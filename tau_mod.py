## =============================================================================
## TAU calculations
## Created on : 1/10/2014
## Created by: Douglas Finch
## =============================================================================
## Description:
## This program covert GEOS-Chem TAU measurements into dates that normal
## people will understand.
## =============================================================================
## Import relevant modules
import datetime as dt
from datetime import datetime
import sys
## =============================================================================

def int2tau(time_and_date):
    try:
        start_time = datetime(1985,01,01,00,00,00)
        date = str(time_and_date)
        if len(date) == 6:
            YYYY = int(date[0:4])
            MM = int(date[4:6])
            DD = 1
            date_new = datetime(YYYY,MM,DD)
        elif len(date) == 8:
            YYYY = int(date[0:4])
            MM = int(date[4:6])
            DD = int(date[6:8])
            date_new = datetime(YYYY,MM,DD)
        elif len(date) == 10:
            YYYY = int(date[0:4])
            MM = int(date[4:6])
            DD = int(date[6:8])
            HH= int(date[8:10])
            date_new = datetime(YYYY,MM,DD,HH)
        else:
            print 'Invalid date format. Use YYYYMM or YYYYMMDD or YYYYMMDDHH'
            sys.exit() 
        
        tau_new = date_new - start_time
        tau = tau_new.total_seconds()/3600
    
    except (TypeError, IndexError):
        print 'Invalid date format. Use YYYYMM or YYYYMMDD or YYYYMMDDHH '
        sys.exit()
    return tau

def datetime2tau(datetime_format):
    start_time = datetime(1985,01,01,00,00,00)
    tau_new = time_and_date - start_time
    tau = tau_new.total_seconds()/3600
    return tau

def tau2time(tau):
    start_time = datetime(1985,01,01,00,00,00)
    new_time = start_time + dt.timedelta(hours = tau)
    return new_time


## =============================================================================
## END OF PROGRAM
## =============================================================================
