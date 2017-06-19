from numpy import *
# import geo_constant as gc
import numpy as npy

def get_model_resolution(nx, ny):
    model_res=""
    if (nx==72 and ny== 46):
        model_res='4x5'

    elif (nx==144 and ny== 91):
        model_res='2x25'
    elif (nx==288 and ny== 181):
        model_res='1x125'
    elif (nx==360 and ny== 181):
        model_res='1x1'
    elif (nx==540 and ny== 361):
        model_res='0.5x0.666'

    return model_res

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

    else:
        ny=nlat

    dy=180.0/(ny-1)
    fmid  = 0.5*(ny + 1 )

    lat=zeros(ny, float)

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
        lat[0] = -89.875
        lat[-1] = 89.875
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
        nx=540
    else:
        nx=nlon

    dx=360.0/(nx)
    lon=zeros(nx, float)
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
        ny= 361


    else:
        ny=nlat

    dy=180.0/(ny-1)
    fmid  = 0.5*(ny + 2 )

    lat=zeros(ny+1, float)

    #  print *, 'assign value'

    for j in range(0, ny+1):
        lat[j]=dy*(j+1-fmid)


    lat[0]=-90.0
    lat[-1]=90.0


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
        nx=540
    else:
        nx=nlon

    dx=360.0/(nx)
    lon=zeros(nx+1, float)
    lon[0]=-180.0-0.5*dx

    for j in range(1, nx+1):
        lon[j]=lon[j-1]+dx


    return lon



def get_area(lon_edge, lat_edge):

    """
    calculate areas for grid box (in m2)

    Inputs:
    --------------------------------------
    1. lon_edge:<array, (nx+1,)>: edges of the X (longitude) grid boxes
    2. lat_edge:<array, (ny+1,)>: edges of the Y (latitude) grid boxes

    Returns:
    ------------------------------
    1. area:<array, (nx, ny)>: area of grid box in m^2

    """

    deg2rad=npy.pi/180.0
    # S1:  get grid egdes
    rlon=lon_edge
    rlat=lat_edge


    nx=npy.size(rlon)
    ny=npy.size(rlat)


    # S2:  dx (longitude) in RAD

    dx=npy.zeros(nx-1, float)
    dx=deg2rad*dx


    for ix in range(nx-1):
        # degree to radius
        dx[ix]=rlon[ix+1]-rlon[ix]

    dx=deg2rad*dx

    from geopy import distance
    rE = distance.EARTH_RADIUS * 1e3

    # S3:  R^2*sin(y); y=latitude

    a2=rE*rE*npy.sin(rlat*deg2rad) 

    # S4:  area=R2*dx*d(sin(y))

    area=npy.zeros([nx-1, ny-1], float)

    for ilat in range(ny-1):
        area[:, ilat]=(a2[ilat+1]-a2[ilat])*dx

    return area



def get_area_mid(lon, lat):
    import geo_constant as gc
    nlon=size(lon)
    dlon=lon[3]-lon[2]
    dlon=0.5*dlon
    rlon=zeros(nlon+1, float)
    rlon[0:nlon]=lon[0:nlon]-0.5*dlon
    rlon[nlon]=lon[nlon-1]

    nlat=size(lat)
    dlat=lat[3]-lat[2]
    dlat=0.5*dlat
    rlat=zeros(nlat+1, float)
    rlat[0:nlat]=lat[0:nlat]-0.5*dlat
    rlat[nlat]=lat[nlat-1]


    print amin(rlon), amax(rlon)
    print rlon[0:10]


    print amin(rlat), amax(rlat)
    print rlat[0:10]



    nx=size(rlon)-1
    ny=size(rlat)-1

    dx=360.0/nx



    # degree to radius
    deg2rad=pi/180.0
    dx=deg2rad*dx


    area=zeros([nx, ny], float)

    a2=gc.re*gc.re*sin(rlat*deg2rad)


    for ilat in range(ny):
        area[:, ilat]=(a2[ilat+1]-a2[ilat])*dx

    return area
