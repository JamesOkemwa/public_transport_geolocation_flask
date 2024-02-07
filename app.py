import folium
from folium.plugins import MarkerCluster
from flask import Flask, render_template
from utility.helpers import read_gtfs_data

app = Flask(__name__)

@app.route('/')
def index():
    # Create a folium map centered in Munster
    munster_coordinates = [51.96, 7.62]
    munster_map = folium.Map(location=munster_coordinates, tiles="cartodb positron", zoom_start=12)

    marker_cluster = MarkerCluster(
        name='bus stops',
        overlay=True,
        control=False,
        icon_create_function=None
    )

    # add bus stops markers to the map
    stops_df = read_gtfs_data()
    for index, bus_stop in stops_df.iterrows():
        bus_stop_coords = [bus_stop['stop_lat'], bus_stop['stop_lon']]
        marker = folium.Marker(location=bus_stop_coords, popup=bus_stop['stop_name'])
        marker_cluster.add_child(marker)

    marker_cluster.add_to(munster_map)

    map_file_path = 'templates/map.html'
    munster_map.save(map_file_path)

    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)