##
##==============================================================================
##Created on: 21/05/2016
##Created By: Douglas Finch
## Returns time zone when given a lat/lon coordinate
##==============================================================================
##
## Import standard modules:
import requests
##==============================================================================

def get_time_zone(lats,lons):

    count_good = 0 # Test to see how many time zones we actually get
    count_bad = 0
    mystery_count = 0 
    for x in range(len(lats)):
        lat = str(lats[x])
        lon = str(lons[x])
        google_api_key = 'AIzaSyALzPnkyAhEqy8qS4AqcUShUz3AtTvLp9A'

        google_map_url = 'https://maps.googleapis.com/maps/api/timezone/json?location='+lat+','+lon+'&timestamp=1458000000&key='+google_api_key
        r=requests.get(google_map_url)

        d = r.json()
        if len(d.keys()) == 1:
            count_bad += 1
        elif len(d.keys()>1):
            cound_good += 1
        else:
            mystery_count += 1

    return count_good, count_bad, mystery_count
##===============================================================================
## END OF PROGRAM
##==============================================================================
