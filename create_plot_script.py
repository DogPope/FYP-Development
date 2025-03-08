# The purpose of this script is to generate a 1km Bounding box from a given point.
# Takes in a point, generates a 1km box around the box, returns a 3dplot of the area from the point provided.
import sys
point1 = input("Please enter a point as Latitude: ")
point2 = input("Please enter a point as Longitude: ")
point = [float(point1), float(point2)]
if point[0] > 180 or point[0] < -180:
    print("Longitude must be between -180 and 180. Returning.")
    exit()
if point[0] > 90 or point[1] < -90:
    print("Latitude must be between -90 and 90. Returning.")
    exit()
def generate_box(point):
    #create_plot_script = sys.argv[0]
    from haversine import inverse_haversine, Unit, Direction
    from math import sqrt

    bounding_box = []
    # Generate a 1km box around the point. Directions should correspond to the directions given in the old bounding box.
    directions = ['NORTHWEST', 'NORTHEAST', 'SOUTHWEST', 'SOUTHEAST']
    for i in directions:
        direction_enum = getattr(Direction, i)  # Convert string to Direction enum
        bounding_box.append(inverse_haversine(point, sqrt(2), direction_enum, Unit.KILOMETERS))
    return bounding_box

bounding_box = generate_box(point)

def generate_data(bounding_box): # Not currently calling this.
    import json
    import requests
    import os
    max_latitude = bounding_box[0][0] # NORTHWEST
    min_latitude = bounding_box[2][0] # SOUTHWEST
    max_longitude = bounding_box[0][1] # NORTHEAST
    min_longitude = bounding_box[1][1] # NORTHWEST
    steps = 5
    latitude_difference = max_latitude - min_latitude
    longitude_difference = max_longitude - min_longitude
    lat_diff = latitude_difference / steps
    long_diff = longitude_difference / steps
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

        for i in range(0, steps + 1):
            for j in range(0, steps + 1):
                return_elevation(min_latitude + i * lat_diff, min_longitude + j * long_diff)

generate_data(bounding_box)