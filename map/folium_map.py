import folium
from folium.plugins import MarkerCluster
from utility.helpers import read_gtfs_data


class FoliumMapManager:
    """
    Used to create a folium map instance that is accessible in the wole application
    """

    def __init__(self):
        self.munster_coordinates = [51.96, 7.62]
        self.map_instance = None
        self.user_location_marker = None

    def create_map(self):
        """
        Create folium map centered on Münster and add markers for all bus stops
        """
        if self.map_instance is None:
            self.map_instance = folium.Map(location=self.munster_coordinates, tiles="cartodb positron", zoom_start=12)

            marker_cluster = MarkerCluster(
                name='bus stops',
                overlay=True,
                control=False,
                icon_create_function=None
            )

            stops_df = read_gtfs_data()
            for index, bus_stop in stops_df.iterrows():
                bus_stop_coords = [bus_stop['stop_lat'], bus_stop['stop_lon']]
                marker = folium.Marker(location=bus_stop_coords, popup=bus_stop['stop_name'])
                marker_cluster.add_child(marker)

            marker_cluster.add_to(self.map_instance)

        return self.map_instance
    
    def add_user_location_marker(self, lat, long):
        """
        Takes the latitude and longitude of the user location as parameters and adds a marker at that location on the map
        """
        if self.user_location_marker is not None:
            self.clear_map()

        self.user_location_marker = folium.Marker(location=[lat, long], popup='You are here', icon=folium.Icon(color='red'))
        self.user_location_marker.add_to(self.map_instance)

    def clear_map(self):
        """
        Clear all markers on the map
        """
        if self.map_instance is not None:
            self.map_instance = self.create_map()

    def get_map_html(self):
        """
        Returns the html represenation of the updated map instance
        """
        return self.map_instance._repr_html_()