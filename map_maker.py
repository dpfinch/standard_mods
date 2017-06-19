##
##==============================================================================
##Created on: 30/10/13
##Created By: Douglas Finch
##Python 2.7
##Plot fire locations on a map
##==============================================================================
## Import standard modules:
import numpy as np
import scipy
import matplotlib
import matplotlib.cm as cm
from matplotlib import pyplot as plt
plt.style.use('classic')
import matplotlib as mpl
plt.rcParams['font.size'] = 22
plt.rcParams['axes.labelsize'] = 24
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 22
plt.rcParams['ytick.labelsize'] = 22
plt.rcParams['legend.fontsize'] = 22
plt.rcParams['figure.titlesize'] = 24
plt.rcParams['axes.facecolor']= 'white'
from pylab import *
import fileimport
import datetime as dt
from datetime import datetime
import mpl_toolkits
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PathCollection
from matplotlib.path import Path
##==============================================================================
#matplotlib.rcParams.update({'font.size': 6})

# MPL searches for ne_10m_land.shp in the directory 'D:\\ne_10m_land'
##    m = Basemap(projection='robin',lon_0=0,resolution='c')
m = Basemap(projection='cyl',llcrnrlat=-10,urcrnrlat=70,\
        llcrnrlon=-140,urcrnrlon=-40,resolution='c')
shp_info = m.readshapefile('/home/s1251441/Python/landfile/land/ne_10m_land_scale_rank', 'scalerank', drawbounds=True)
ax = plt.gca()
ax.cla()

paths = []
for line in shp_info[4]._paths:
    paths.append(Path(line.vertices, codes=line.codes))

coll = PathCollection(paths, linewidths=0.5,zorder=0,facecolors='black', color='grey')

##    m = Basemap(projection='robin',lon_0=0,resolution='c')
##    m = Basemap(projection='ortho',lon_0=-90,lat_0=90,resolution='c')
m = Basemap(projection='cyl',llcrnrlat=20,urcrnrlat=80,\
        llcrnrlon=-160,urcrnrlon=-40,resolution='c')
# drawing something seems necessary to 'initiate' the map properly
m.drawcoastlines(color='black', zorder=0, linewidth= 0)
m.drawcountries(color='black',zorder=0, linewidth= 0)
m.drawparallels(np.arange(-90.,90.,10.),linewidth=0.5, labels=[1,1,0,0])
m.drawmeridians(np.arange(0.,360.,20.),linewidth=0.5,labels=[0,0,1,1])
##
##m.bluemarble()
ax = plt.gca()
ax.add_collection(coll)

##plt.savefig('/home/s1251441/Documents/BORTAS/global_map',dpi=(500))
plt.show()

##==============================================================================
## END OF PROGRAM
##==============================================================================
