# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 13:29:42 2023

@author: Sean
"""

import googlemaps
import requests

# Replace with your Google Maps API key
api_key = 'AIzaSyBToJhU5VDk0V8UA9Gf_tQB_2acbud3W2k'

gmaps = googlemaps.Client(key=api_key)

def get_elevation(lat, lng):
    # Make a request to the Elevation API
    url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lng}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    if 'results' in data:
        return data['results'][0]['elevation']
    return None

def is_slope_above_20_degrees(start, end):
    elevation_start = get_elevation(start[0], start[1])
    elevation_end = get_elevation(end[0], end[1])

    if elevation_start is not None and elevation_end is not None:
        delta_elevation = elevation_end - elevation_start
        distance = ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
        slope = (delta_elevation / distance) * 180 / 3.14159265  # Convert to degrees

        return slope > 20
    return False

def find_walking_route(origin, destination):
    # Request walking directions
    directions = gmaps.directions(origin, destination, mode='walking')

    # Filter out uphill segments
    filtered_directions = [directions[0]['legs'][0]['steps'][0]]
    for step in directions[0]['legs'][0]['steps'][1:]:
        start = (filtered_directions[-1]['end_location']['lat'], filtered_directions[-1]['end_location']['lng'])
        end = (step['end_location']['lat'], step['end_location']['lng'])

        if not is_slope_above_20_degrees(start, end):
            filtered_directions.append(step)

    return filtered_directions

if __name__ == '__main__':
    origin = '1175 Boylston St, Boston, MA 02215 United State'
    destination = '820 Commonwealth Ave, Brookline, MA 02446 United State'

    route = find_walking_route(origin, destination)
    for step in route:
        print(step['html_instructions'])
