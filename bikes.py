"""Helper functions and functions that interface with the citibike API"""

import requests

_station_status_url = 'https://gbfs.citibikenyc.com/gbfs/en/station_status.json'
_station_information_url = 'https://gbfs.citibikenyc.com/gbfs/en/station_information.json'
_system_alerts_url = 'https://gbfs.citibikenyc.com/gbfs/en/system_alerts.json'

def get_stations():
    """Makes a request to the station list and returns a set of objects 
    representing the stations."""
    response = request.get(_station_information_url)
    pass

def get_station_status():
    response = request.get(_station_status_url)
    pass

def get_station_alerts():
    response = request.get(_system_alerts_url)
    pass


