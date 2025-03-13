import requests
import os
class Geocoding:
    API_KEY = os.getenv('geocode')
    
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    #Creating constructor for all of the variables needed in the class
    def __init__(self, address='1600 Pennsylvania Avenue NW, Washington, DC',place_id='ChIJ0SvEag7uLogRhsBvcb7vTO0'):
        self.address = address
        self.place_id=place_id
        self.coordpair = [0, 0]
        self.params = {
            'key': self.API_KEY,
            'address': self.address
        }
        self.idparams={'key': self.API_KEY,
                       'place_id': self.place_id}

    #creating setter methods to set necessary Parameters in OOP
    def setParams(self, address):
        self.params['address'] = address
    def setIdParams(self,place_id):
        self.idparams={'key':self.API_KEY,
                       'place_id':place_id}

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
        print(self.idparams)
        if idresponse['status']=='OK':
            print(idresponse['results'][0]['formatted_address'])
            print(idresponse['results'][0]['geometry']['location'])
        else:
            print("Error:", idresponse['status'])
            return None


class Main:
    Alex = Geocoding()
    Alex.get_coord()
    Alex.get_placeidtocoord()