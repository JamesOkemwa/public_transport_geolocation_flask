import geopandas as gpd
import pandas as pd

def read_gtfs_data():
    """
    Load bus stops data into a pandas dataframe
    """
    gtfs_file_path = 'data/gtfs/stadtwerke_feed/stops.txt'
    bus_stops_df = pd.read_csv(gtfs_file_path)
    return bus_stops_df