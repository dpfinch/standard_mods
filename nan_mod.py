#Module for dealing with NaNs in code
import numpy as np

def mean(x): 
    x=x[np.logical_not(np.isnan(x))]
    if sum(x) == 0:
        return np.nan
    else:
        mean_x=sum(x)/len(x)
        return mean_x

def remove(x):
    x=x[np.logical_not(np.isnan(x))]
    return x

def median(x):
    x=x[np.logical_not(np.isnan(x))]
    x=np.median(x)
    return x

def remove_pairs(x,y):
    if len(x) != len(y):
        return 'Both arrays must contain the same number of values'
    else:
        a=np.array([x,y])
        a=np.transpose(a)
        a=a[~np.isnan(a).any(1)]
        x=a[:,0]
        y=a[:,1]
        return x,y

def std(x): 
    x=x[np.logical_not(np.isnan(x))]
    if sum(x) == 0:
        return np.nan
    else:
        std_x=np.std(x)
        return std_x

def median(x):
    x=x[np.logical_not(np.isnan(x))]
    if sum(x) == 0:
        return np.nan
    else:
        med = np.median(x)
        return med
