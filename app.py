import folium
from folium.plugins import MarkerCluster
from flask import Flask, render_template, request, jsonify
from utility.helpers import read_gtfs_data

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('map.html', folium_map=munster_map._repr_html_())

@app.route('/update_user_location', methods=['POST'])
def update_user_location():
    """
    Receives the user location coordinates from the browser
    """
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Add a marker for the user's location
    user_location_marker = folium.Marker(location=[latitude, longitude], popup='You are here', icon=folium.Icon(color='red'))
    user_location_marker.add_to(munster_map)
    munster_map.position = [latitude, longitude]

    updated_map_html = munster_map._repr_html_()

    return jsonify({'message': 'User location updated successfully', 'updated_map_html': updated_map_html})

@app.route('/search_destination', methods=['POST'])
def search_destination():
    """
    Receives the search parameter from the search bar on the map
    """
    data = request.get_json()
    search_param = data.get('search_param')
    return jsonify({'message': 'Search parameter received', 'search_param': search_param})

if __name__ == '__main__':
    app.run(debug=True)