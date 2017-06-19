##
##==============================================================================
##Created on: 18/02/13
##Created By: Douglas Finch
##Python 2.7
##Module hold information from GEOS-Chem
##==============================================================================
##==============================================================================
##
## Import standard modules:
import numpy as np
import pickle
##==============================================================================
# Levels from altitude input
##==============================================================================
def lev_info(km):
    info=np.loadtxt('/home/dfinch/GEOS-Chem/geos_lvls')
    info=info[::-1]

    alts=info[:,2]
    lvls=info[:,0]
    pres=info[:,3]

    # Find the nearest value
    val=min(range(len(alts)), key=lambda i: abs(alts[i]-km))

    level=lvls[val]-1

    return int(level)

##==============================================================================
# Altitude from level input
##==============================================================================
def alt_info(lev):
    info=np.loadtxt('/home/dfinch/GEOS-Chem/geos_lvls')
    info=info[::-1]

    alts=info[:,2]
    lvls=info[:,0]
    pres=info[:,3]

    altitude=alts[lev]

    return altitude

##==============================================================================
# Altitude from pressure input
##==============================================================================
def alt_pres(pressure):
    info=np.loadtxt('/home/dfinch/GEOS-Chem/geos_lvls')
    info=info[::-1]

    alts=info[:,2]
    lvls=info[:,0]
    pres=info[:,3]

    # Find the nearest value
    val=min(range(len(pres)), key=lambda i: abs(pres[i]-pressure))

    altitude=alts[val]

    return altitude

##==============================================================================
# Pressure from altitude input
##==============================================================================
def pres_alt(altitude):
    info=np.loadtxt('/home/dfinch/GEOS-Chem/geos_lvls')
    info=info[::-1]

    alts=info[:,2]
    lvls=info[:,0]
    pres=info[:,3]

    # Find the nearest value
    val=min(range(len(alts)), key=lambda i: abs(alts[i]-altitude))

    pressure=pres[val]

    return pressure

##==============================================================================
# Level from pressure input
##==============================================================================
def lvl_pres(pressure):
    info=np.loadtxt('/home/dfinch/GEOS-Chem/geos_lvls')
    info=info[::-1]

    alts=info[:,2]
    lvls=info[:,0]
    pres=info[:,3]

    # Find the nearest value
    val=min(range(len(pres)), key=lambda i: abs(pres[i]-pressure))

    level=lvls[val]

    return level

##==============================================================================
# Pressure from level input
##==============================================================================
def pres_lvl(level):
    info=np.loadtxt('/home/dfinch/GEOS-Chem/geos_lvls')
    info=info[::-1]

    alts=info[:,2]
    lvls=info[:,0]
    pres=info[:,3]

    # Find the nearest value
    val=min(range(len(lvls)), key=lambda i: abs(lvls[i]-level))

    pressure=pres[val]

    return pressure
##==============================================================================
# Grid co-ord from Latitude
##==============================================================================
def lat2grid(lat,grid):

    if grid == '2x25':
        lat_min = -90
        lat_max = 92
        res = 2

    elif grid == 'NA':
        lat_min = 10
        lat_max = 70.5
        res = 0.5

    elif grid =='4x5':
        print "This latitude grid reference could be dubious"
        lat_min = -90
        lat_max = 90
        res = 4

    elif grid =='1x1':
        lat_min = -90
        lat_max = 90
        res = 1

    elif grid == 'NAredux':
        lat_min = 34.5
        lat_max = 70
        res = 0.5
    
    lat_range=np.arange(lat_min,lat_max, res)
    grid_no=min(range(len(lat_range)), key=lambda i: abs(lat_range[i]-lat))
    # This needs to happen to make sure that the height lats (ie 90N) are at the top
    # Of the grid (ie 0).

##    grid_no = len(lat_range) - grid_no - 1
    return grid_no
##==============================================================================
# Grid co-ord from Longitude
##==============================================================================
def lon2grid(lon,grid):

    if grid == '2x25':
        lon_min = -180
        lon_max = 182.5
        res = (362.5/144.)

    elif grid == 'NA':
        lon_min = -140
        lon_max = -40 + (2/3.)
        res = (2/3.)

    elif grid == '4x5':
        lon_min = -180
        lon_max = 180
        res = 5

    elif grid == '1x1':
        lon_min = -180
        lon_max = 180
        res = 1

    elif grid == 'NAredux':
        lon_min = -100
        lon_max = -40 + (2/3.)
        res = (2/3.)

    lon_range=np.arange(lon_min,lon_max,res)
    grid_no=min(range(len(lon_range)), key=lambda i: abs(lon_range[i]-lon))
    return grid_no

##==============================================================================
# return list of standard tracers for GEOS-Chem
##==============================================================================
def stnd_tracers():
    fname = '/home/dfinch/GEOS-Chem/stnd_tracers'
    tracers = np.loadtxt(fname, dtype=str)
    return tracers
##==============================================================================
# return list of standard tracers for GEOS-Chem
##==============================================================================
def rxn_nums(tracer):
    fname = '/home/dfinch/GEOS-Chem/rxn_nums.'+tracer
    tracers = np.loadtxt(fname, dtype=str)
    return tracers

##==============================================================================
# return list of moler mass for tracers in GEOS-Chem
##==============================================================================
def mol_mass(tracer):
    if tracer == 'BC':
        tracer = 'BCPI'
    if tracer == 'OC':
        tracer = 'OCPI'
    fname = '/home/dfinch/GEOS-Chem/stnd_tracers'
    tracers = np.loadtxt(fname, dtype=str)
    species = np.where(tracers == tracer)
    no = species[0][0]
    Mmass = float(tracers[no][2])
    return Mmass
##==============================================================================
# return the chemical equation matching the smv number
##==============================================================================
def get_equation(rxn_num):
    fname = '/home/dfinch/GEOS-Chem/reaction_names.p'
    rxns = pickle.load(open(fname))
    equation = rxns[rxn_num]

    return equation

##==============================================================================
## END OF PROGRAM
##==============================================================================
