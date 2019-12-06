# coding: utf-8

"""French address geolocalizer API
"""

import argparse
import slumber
import sys

class Address(object):
    def factory(api):
        if api == 'geodatagouv': return GeoDataGouv()
        if api == 'nominatim': return Nominatim()
        assert 0, "Bad address creation: " + api
    factory = staticmethod(factory)

class GeoDataGouv(Address):
    URL = "http://api-adresse.data.gouv.fr"

    def __init__(self):
        self.api = slumber.API(self.URL)


    def coordinate(self, address):
        """Get lon/lat coordinate from an address

        address: str

        Return (longitude, latitde)
        """
        resources = self.api.search.get(q=address, format='json')
        if len(resources['features']) == 0:
            return {"lon": None,
                    "lat": None,
                    'address': None}
        lon, lat = self.lonlat(resources["features"][0])
        return {"lon": lon,
                "lat": lat,
                "address": self.retrieve_address(resources["features"][0])}


    def retrieve_address(self, feature):
        """Retrieve the address from a feature
        """
        return feature["properties"]["label"]


    def lonlat(self, feature):
        """Longitude and latitude from a GeoJSON feature
        """
        return feature["geometry"]["coordinates"]

class Nominatim(Address):
    URL = "https://nominatim.openstreetmap.org"

    def __init__(self):
        self.api = slumber.API(self.URL)


    def coordinate(self, address):
        """Get lon/lat coordinate from an address

        address: str

        Return (longitude, latitde)
        """
        resources = self.api.search.get(q=address, format='json')
        if len(resources) == 0:
            return {"lon": None,
                    "lat": None,
                    'address': None}
        lon, lat = self.lonlat(resources[0])
        return {"lon": lon,
                "lat": lat,
                "address": self.retrieve_address(resources[0])}


    def retrieve_address(self, feature):
        """Retrieve the address from a feature
        """
        return feature["display_name"]


    def lonlat(self, feature):
        """Longitude and latitude from a GeoJSON feature
        """
        return (feature['lon'], feature['lat'])

def main(argv):
    parser = argparse.ArgumentParser(description='Retrieve address coordinates')
    parser.add_argument('-a', '--api', default='geodatagouv',
            help="The api to use [geodatagouv|nominatim]. Default to geodatagouv")
    parser.add_argument('-v', dest='verbose', action='store_true')
    parser.add_argument('q', nargs="?", help="The address to look for",
            default="place des quinconces borrdeaux")
    args = parser.parse_args()

    address = Address.factory(args.api)
    res = address.coordinate(args.q)
    if args.verbose:
        print(res)

if __name__ == '__main__':
    main(sys.argv[1:])
