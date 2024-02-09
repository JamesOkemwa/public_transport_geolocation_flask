import folium
from flask import Flask, render_template, request, jsonify
from map.folium_map import FoliumMapManager
from utility.helpers import read_gtfs_data

app = Flask(__name__)

map_manager = FoliumMapManager()
munster_map = map_manager.create_map()

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