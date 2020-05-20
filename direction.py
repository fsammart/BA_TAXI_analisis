import requests
import json
import csv
import shutil
import csv
import time
from tempfile import NamedTemporaryFile


ORIGIN_LNG = 5
ORIGIN_LAT = 6
DEST_LNG = 7
DEST_LAT = 8
ORIGIN_NEIGHBORNHOOD = 10
DEST_NEIGHBORNHOOD = 11


class GoogleApi:

    API_KEY = '__API_KEY__'

    def get(self, url, params):
        params.update({'key': self.API_KEY})
        response = requests.get(url = url, params=params)
        return json.loads(response.content)


class GeoCoding(GoogleApi):

    class GeoCodingAddress:
        
        addresses = None

        def __init__(self, addresses):
            self.addresses = addresses
        
        def get_neighborhood(self):
            for address in self.addresses:
                components = address.get('address_components')
                for component in components:
                    component_types = component.get('types')
                    if 'sublocality_level_1' in component_types:
                        return component.get('long_name')
                
            return ''

    url = 'https://maps.googleapis.com/maps/api/geocode/json'

    def get_address(self, lat, lng):
        params = {'latlng': f'{lat},{lng}'}
        resposne = self.get(self.url, params)
        address = self.GeoCodingAddress(resposne.get('results'))
        neighborhood = address.get_neighborhood()
        return neighborhood


class DistanceMatrix(GoogleApi):

    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'

    UNITS = 'metric'

    class DistanceMatrixTrip:
        
        trip = None

        def __init__(self, trip):
            self.trip = trip
        
        def get_distance(self):
            distance = self.trip.get('rows')[0].get('elements')[0].get('distance').get('value')
            return distance

    def get_distance(self, origin_lat, origin_lng, dest_lat, dest_lng):
        params = {
            'units': self.UNITS,
            'origins': f'{origin_lat},{origin_lng}',
            'destinations': f'{dest_lat},{dest_lng}'
        }
        trip = self.DistanceMatrixTrip(self.get(self.url, params))
        distance = trip.get_distance()
        return distance


def main():

    geo_coding_api = GeoCoding()
    distance_matrix_api = DistanceMatrix()

    filename = 'bataxi.csv'
    tempfile = 'bataxi_en1.csv'
    start_row = 18990
    with open(filename, 'r') as csvFile, open(tempfile, 'w') as tempfile:
        reader = csv.reader(csvFile, delimiter=',')
        writer = csv.writer(tempfile, delimiter=',', )
        i = 0
        for row in reader:
            # First row is for headers
            i += 1
            if i < start_row:
                writer.writerow(row)
                continue
            origin_lng = row[ORIGIN_LNG].title()
            origin_lat = row[ORIGIN_LAT].title()
            dest_lng = row[DEST_LNG].title()
            dest_lat = row[DEST_LAT].title()
            origin_neighbornhood = geo_coding_api.get_address(origin_lat, origin_lng)
            dest_neighbornhood = geo_coding_api.get_address(dest_lat, dest_lng)
            distance = distance_matrix_api.get_distance(
                origin_lat, 
                origin_lng, 
                dest_lat, 
                dest_lng
            )
            row.append(origin_neighbornhood)
            row.append(dest_neighbornhood)
            row.append(distance)
            writer.writerow(row)
            print(i)
main()