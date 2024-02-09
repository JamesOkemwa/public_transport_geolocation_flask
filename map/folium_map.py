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
