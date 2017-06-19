##==============================================================================
## Created on: 15/03/2017
## Created By: Douglas Finch
## Python 2.7
## Find the area of grid squares in a lat lon grid
##==============================================================================
import numpy as np
import math
from geopy import distance
##==============================================================================
def area(lat,lon):
    # Return area of grid box in m2 - using the same method as GEOS-Chem
    # Method found in GeosUtil/global_grid_mod.F90
    area_grid = np.zeros([len(lat),len(lon)])
    resolution = lat[1] - lat[0]
    edge_dist = resolution / 2.
    # Earth Radius from km to m
    Re = distance.EARTH_RADIUS * 1e3

    for ll in range(len(lat)):
        area = (2 * np.pi * (Re**2) / len(lon)) * (np.sin(math.radians(lat[ll] + edge_dist)) - np.sin(math.radians(lat[ll] - edge_dist)))
        area_grid[ll,:] = area

    global_surface = 5.101e14 # m^2
    limit = 1e12 # 1% buffer
    if global_surface + limit < np.sum(area_grid) < global_surface - limit:
        print "WARNING - global surface area not a good match"
        print "Calculated area to be %r not %r" % (np.sum(area_grid),global_surface)
    return area_grid


##### Horrendous code copied from Liang, does the job perhaps.
def get_model_lat(model_res=None,nlat=0):

    if (model_res=='4x5'):
        ny=46
    elif (model_res=='2x25'):
        ny=91
    elif (model_res=='1x125'):
        ny=181
    elif (model_res=='1x1'):
        ny=181
    elif (model_res=='0.5x0.666'):
        ny=361
    elif (model_res=='0.25x0.3125'):
        ny=721
    else:
        ny=nlat

    dy=180.0/(ny-1)
    fmid  = 0.5*(ny + 1 )

    lat=np.zeros(ny, float)

    #  print *, 'assign value'

    for j in range(0, ny):
        lat[j]=dy*(j+1-fmid)


    if (model_res=='4x5'):
        lat[0] = -88.0
        lat[-1] = 88.0

    elif (model_res=='2x25'):

        lat[0] = -89.5
        lat[-1] = 89.5
    elif (model_res=='1x125'):
        lat[0] = -89.75
        lat[-1] = 89.75

    elif (model_res=='1x1'):
        lat[0] = -89.75
        lat[-1] = 89.75


    elif (model_res=='0.5x0.666'):
        lat[0] = -90+0.5*0.5
        lat[-1] = 90-0.5*0.5


    elif (model_res=='0.25x0.3125'):
        lat[0] = -90+0.5*0.25
        lat[-1] = 90-0.5*0.25



    else:
        pass

    return lat

def get_model_lon(model_res=None,nlon=0):

    if (model_res=='4x5'):
        nx=72
    elif (model_res=='2x25'):
        nx=144
    elif (model_res=='1x125'):
        nx=288
    elif (model_res=='1x1'):
        nx=360

    elif (model_res=='0.5x0.666'):
        nx=3*360/2
    elif (model_res=='0.25x0.3125'):

        nx=int(360./0.3125)

    else:
        nx=nlon

    dx=360.0/(nx)
    lon=np.zeros(nx, float)
    lon[0]=-180.0


    for j in range(1, nx):
        lon[j]=lon[j-1]+dx


    return lon

def get_model_lat_edge(model_res=None,nlat=0):

    if (model_res=='4x5'):
        ny=46
    elif (model_res=='2x25'):
        ny=91
    elif (model_res=='1x125'):
        ny=181
    elif (model_res=='1x1'):
        ny=181

    elif (model_res=='0.5x0.666'):
        ny=361
    elif (model_res=='0.25x0.3125'):
        ny=721

    else:
        ny=nlat

    dy=180.0/(ny-1)

    fedge  = 0.5*(ny + 2 )

    lat=np.zeros(ny+1, float)

    #  print *, 'assign value'

    for j in range(0, ny):
        lat[j]=dy*(j+1-fedge)

    lat[0] = -90.0
    lat[-1] = 90.0

    return lat

def get_model_lon_edge(model_res=None,nlon=0):

    if (model_res=='4x5'):
        nx=72
    elif (model_res=='2x25'):
        nx=144
    elif (model_res=='1x125'):
        nx=288
    elif (model_res=='1x1'):
        nx=360

    elif (model_res=='0.5x0.666'):
        nx=2*360
    elif (model_res=='0.25x0.3125'):
        nx=4*360

    else:
        nx=nlon

    dx=360.0/(nx)
    lon=np.zeros(nx+1, float)

    lon[0]=-180.0  -0.5*dx



    for j in range(1, nx+1):
        lon[j]=lon[j-1]+dx


    return lon


## =============================================================================
## END OF PROGRAM
## =============================================================================
