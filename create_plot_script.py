# The purpose of this script is to generate a 1km Bounding box from a given point.
# Takes in a point, generates a 1km box around the box, returns a 3dplot of the area from the point provided.
def generate_box(longitude, latitude):
    if longitude > 180 or longitude < -180:
        print("Longitude must be between -180 and 180")
        return
    if latitude > 90 or latitude < -90:
        print("Latitude must be between -90 and 90")
        return
    from haversine import distance

generate_box()
'''
import json
import requests
import os

bounding_box=[[52.008033, -9.757847],[52.008033,-9.728633],[51.990047,-9.757847],[51.990047,-9.728633]]

max_latitude = bounding_box[0][0]
min_latitude = bounding_box[2][0]
latitude_difference = max_latitude - min_latitude

max_longitude = bounding_box[0][1]
min_longitude = bounding_box[1][1]
longitude_difference = max_longitude - min_longitude

# Variables to store the difference in Latitude and Longitude in max and minumum value, etc.
lat_diff = (max_latitude - min_latitude) / steps
long_diff = (max_longitude - min_longitude) / steps

steps = 2

api_key = os.environ.get("GOOGLE_API_KEY")
def return_elevation(lat, lng):
    url = "https://maps.googleapis.com/maps/api/elevation/json?locations=" + str(lat) + "%2C" + str(lng) + "&key=" + str(api_key)
    response = requests.get(url)
    response_as_json = response.json()
    json_str = json.dumps(response_as_json)
    resp = json.loads(json_str)
    lat = resp['results'][0]['location']['lat']
    lng = resp['results'][0]['location']['lng']
    elev = resp['results'][0]['elevation']
    print(lat, lng, elev)

for i in range(0,steps + 1):
    for j in range (0,steps + 1):
        return_elevation(min_latitude + i * lat_diff, min_longitude + j * long_diff)
'''