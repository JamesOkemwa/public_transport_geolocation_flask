import folium
from flask import Flask, render_template, request, jsonify
from map.folium_map import FoliumMapManager
from utility.helpers import read_gtfs_data, geocode_location

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
    map_manager.add_user_location_marker(latitude, longitude)

    return jsonify({'message': 'User location updated successfully', 'updated_map_html': map_manager.get_map_html()})

@app.route('/search_destination', methods=['POST'])
def search_destination():
    """
    Receives the search parameter from the search bar on the map, geocodes it adds the location on the map
    """
    data = request.get_json()
    search_param = data.get('search_param')

    destination_coords = geocode_location(search_param)

    # add a marker for the destination on the map
    if destination_coords:
        map_manager.add_destination_marker(destination_coords.get('latitude'), destination_coords.get('longitude'))
    
    return jsonify({'message': 'Search parameter received', 'updated_map_html': map_manager.get_map_html()})

if __name__ == '__main__':
    app.run(debug=True)