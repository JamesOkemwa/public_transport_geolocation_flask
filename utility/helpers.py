from geopy.geocoders import Nominatim
import pandas as pd

def read_gtfs_data():
    """
    Load bus stops data into a pandas dataframe
    """
    gtfs_file_path = 'data/gtfs/stadtwerke_feed/stops.txt'
    bus_stops_df = pd.read_csv(gtfs_file_path)
    return bus_stops_df

def geocode_location(param):
    """
    Takes in a location name or address, geocodes it and returns the coordinates of the location.
    """
    geocoder = Nominatim(user_agent="Munster Public Transport")
    location_coords = geocoder.geocode(param)

    if location_coords:
        latitude, longitude = location_coords.latitude, location_coords.longitude
        return {'latitude': latitude, 'longitude': longitude}
    else:
        return None