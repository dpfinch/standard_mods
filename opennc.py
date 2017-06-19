##==============================================================================
##Created on: 15/07/14
##Created By: Douglas Finch
##Python 2.7
##The purpose of this module is to read in NetCDF files from GEOS-Chem and give
## a usable output
##==============================================================================
##==============================================================================
##
## Import standard modules:
import numpy as np
import scipy

def nc(filename):
    from scipy.io import netcdf

    f=netcdf.netcdf_file(filename,'r')
    var=f.variables.keys()

    d={}
    for x in range(len(var)):
        data=f.variables[var[x]]
        d[var[x]]=data[:]

    # List of all the tracer from a full chemistry run v9.02

    return d

##==============================================================================
## END OF PROGRAM
##==============================================================================
