import json
import urllib.parse

class URLBuilder:
    def __init__(self):
        self.PROVINCES_JSON = json.load(open('./assets/data/italyProvinces.json'))
        self.REGIONS_JSON = json.load(open('./assets/data/italyRegions.json'))

    def __parsePlace(self, place):
        return place.replace(' ', '-').replace('\'', '-').lower()

    def __getProvinces(self):
        return [self.__parsePlace(d["nome"]) for d in self.PROVINCES_JSON if "nome" in d]

    def __getRegions(self):
        return [self.__parsePlace(d) for d in self.REGIONS_JSON]

    def __getProvincesFromRegion(self, region):
        return [self.__parsePlace(d["nome"]) for d in self.PROVINCES_JSON if self.__parsePlace(d["regione"]) == self.__parsePlace(region)]

    def __getRegionFromProvince(self, province):
        return [self.__parsePlace(d["regione"]) for d in self.PROVINCES_JSON if self.__parsePlace(d["nome"]) == self.__parsePlace(province)][0]


    def buildUrl(self, query: str, place: str, category: str = 'usato', municipalityOnly: bool = False, shippingOnly: bool = False, titleOnly: bool = False):
        domain = 'https://www.subito.it/'
        query = urllib.parse.quote_plus(query)
        
        place = self.__parsePlace(place)
            
        if place in self.__getProvinces(): 
            province = place
            region = self.__getRegionFromProvince(place)
            
        elif place in self.__getRegions():
            province = ''
            region = place
        
        else:
            raise ValueError(f'Place argument ({place}) is not a valid argument!')
            

        # TODO: usato should be a category, query not right
        return (f'{domain}annunci-{region}/vendita/{category}/{province}/?q={query}')
            