import requests
import os
class Geocoding:
    API_KEY = os.getenv('geocode')
    
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

    def __init__(self, address='1600 Pennsylvania Avenue NW, Washington, DC',places_id='aaaaaa'):
        self.address = address
        self.places_id=places_id
        self.coordpair = [0, 0]
        self.params = {
            'key': self.API_KEY,
            'address': self.address
        }
        self.idparams={'key': self.API_KEY,
                       'places_id': self.places_id}


    def setParams(self, address):
        self.params['address'] = address
    def setIdParams(self,places_id):
        self.idparams={'key':self.API_KEY,
                       'places_id':self.places_id}

    def get_coord(self):
        response = requests.get(self.base_url, params=self.params).json()
        if response['status'] == 'OK':
            location = response['results'][0]['geometry']['location']
            lat = location['lat']
            lng = location['lng']
            print(lat, lng)
            self.coordpair[0] = lat
            self.coordpair[1] = lng
            return self.coordpair
        else:
            print("Error:", response['status'])
            return None
    def get_placeidtocoord(self):
        idresponse=requests.get(self.base_url,params=self.idparams).json()
        if idresponse['status']=='OK':
            print(idresponse['results'])
        else:
            print("Error:", response['status'])
            return None


class Main:
    Alex = Geocoding()
    Alex.get_coord()