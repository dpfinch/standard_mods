##
##==============================================================================
##Created on: 05/02/2015
##Created By: Douglas Finch
##Python 2.7
## Calculate mixing ratio from yeild and air density
##==============================================================================
## Import standard modules:
import numpy as np
import scipy as sp
import geos_info
import time
import glob
import fileimport
import tau_mod
##==============================================================================

def calc_mixing_ratio(yeild,air_dens):
    '''
    This function gets the air density and the yeild as a list and calculates the
    mixing ratio of the chosen gas.
    '''

    #rate in molec/cm3/s
    yeild_per_hour = yeild * 3600
    #yeild in molec/cm3
    yeild_per_meter = yeild# * 1e6

    mixing_ratio = yeild_per_meter / air_dens

    return mixing_ratio    
            

##==============================================================================
## END OF PROGRAM
##==============================================================================
