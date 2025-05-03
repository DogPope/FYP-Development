'''
The purpose of this script is to generate a 1km Bounding box from a given point.
Takes in a point, generates a 1km box around the box, returns a csv file of the area from the point provided.
Just for testing, the summit of carrauntoohil is used as the point - 51.9994, -9.7425
'''

# Block of validation for Longitude and Latitude.
def validate_latitude(input):
    try:
        value = float(input)
        if value > 90 or value < -90:
            return False

        decimal_places = len(input.split('.')[-1]) if '.' in input else 0
        if decimal_places > 6:
            return False

        return True
    except ValueError:
        return False

def validate_longitude(input):
    try:
        value = float(input)
        if value > 180 or value < -180:
            return False
        
        decimal_places = len(input.split('.')[-1]) if '.' in input else 0
        if decimal_places > 6:
            return False
            
        return True
    except ValueError:
        return False

point1 = input("Please enter a point as Latitude: ")
if not validate_latitude(point1):
    print("Latitude must be a number. Returning.")
    exit()
point2 = input("Please enter a point as Longitude: ")
if not validate_longitude(point2):
    print("Longitude must be a number. Returning.")
    exit()
point = [float(point1), float(point2)]
if point[0] > 180 or point[0] < -180:
    print("Longitude must be between -180 and 180. Returning.")
    exit()
if point[0] > 90 or point[1] < -90:
    print("Latitude must be between -90 and 90. Returning.")
    exit()

    
def generate_box(point):
    from haversine import inverse_haversine, Unit, Direction
    from math import sqrt

    bounding_box = []
    directions = ['NORTHWEST', 'NORTHEAST', 'SOUTHWEST', 'SOUTHEAST']
    for i in directions:
        direction_enum = getattr(Direction, i)
        bounding_box.append(inverse_haversine(point, sqrt(2), direction_enum, Unit.KILOMETERS))
    return bounding_box

bounding_box = generate_box(point)

# Generates the CSV file based on the bounding box given.
def generate_data(bounding_box):
    import requests
    import os
    max_latitude = bounding_box[0][0] # NORTHWEST
    min_latitude = bounding_box[2][0] # SOUTHWEST
    max_longitude = bounding_box[0][1] # NORTHEAST
    min_longitude = bounding_box[1][1] # NORTHWEST
    steps = 4
    latitude_difference = max_latitude - min_latitude
    longitude_difference = max_longitude - min_longitude
    lat_diff = latitude_difference / steps
    long_diff = longitude_difference / steps
    api_key = os.environ.get("GOOGLE_API_KEY")

    def return_elevation(lat, lng):
        url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat}%2C{lng}&key={api_key}"
        response = requests.get(url)
        response_as_json = response.json()
        resp = response_as_json
        lat = resp['results'][0]['location']['lat']
        lng = resp['results'][0]['location']['lng']
        elev = resp['results'][0]['elevation']
        return lat, lng, elev

    import csv
    elevation_data = []
    with open('custom_data_set.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['latitude', 'longitude', 'elevation'])
        
        for i in range(0, steps + 1):
            for j in range(0, steps + 1):
                current_lat = min_latitude + i * lat_diff
                current_lng = min_longitude + j * long_diff
                lat, lng, elev = return_elevation(current_lat, current_lng)
                lat = round(lat, 7)
                lng = round(lng, 7)
                elev = round(elev, 2)
                elevation_data.append((lat, lng, elev))
                csvwriter.writerow([lat, lng, elev])
                print(f"Added point: Lat={lat}, Lng={lng}, Elevation={elev}m")
    
    return elevation_data

# Calls function with the bounding box
elevation_points = generate_data(bounding_box)