#!/usr/bin/env python3

import argparse
import requests
import json

API = 'https://api.corona-zahlen.org/vaccinations'

class ImpfungUpdate:

    def __init__(self):
        self.prefix = ''
        result = requests.get(API)
        self.data = result.json()["data"]

    def get_vac_data(self,area, key, isSecond=False):
        area_data = []
        if area == '':
            area_data = self.data
        else:
            area_data = self.data["states"][area]
        if isSecond:
            return area_data["secondVaccination"][key]
        else:
            return area_data[key]

    def get_vac_all(self, area):
        return self.get_vac_data(area,"administeredVaccinations")                   
    
    def get_vac_all_delta(self, area):
        return int(self.get_vac_first_delta(area)) + int(self.get_vac_second_delta(area))

    def get_vac_first(self, area):
        return self.get_vac_data(area,"vaccinated")                   

    def get_vac_second(self,area):
        return self.get_vac_data(area,"vaccinated",True)

    def get_vac_first_delta(self, area):
        return self.get_vac_data(area,"delta")

    def get_vac_second_delta(self,area):
        return self.get_vac_data(area,"delta",True)

    def get_vac_quote(self, area):
        return self.get_vac_data(area,"quote")

    def get_vac_by_brand(self,area,brand):
        return self.get_vac_data(area,"vaccination")[brand]

    def get_all_vac_brands(self,area):
        return self.get_vac_data(area,"vaccination")

    def all_areas(self):
        abb = self.data["states"].keys()
        for key in abb:
            print("{key} for {name}".format(key=key,name=self.data["states"][key]["name"]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-bl", "--bundesland", help="Information about a Bundesland in germany")
    parser.add_argument("-a","--all",help="All accinaations in a specific area", action="store_true")
    parser.add_argument("-la","--listareas", help="Lists all available areas", action="store_true")
    parser.add_argument("-p", "--prefix", help="Print given prefix as string before the actual number. Example: -p 'Bayern Vaccinations' -bl Bayern -a")
    parser.add_argument("-d", "--difference", help="Difference in vaccinations to the day before for all vaccination", action="store_true")
    parser.add_argument("-df", "--differencefirst", help="Difference in vaccinations to the day before for the first vaccination", action="store_true")
    parser.add_argument("-ds", "--differencesecond", help="Difference in vaccinations to the day before for the second vaccination", action="store_true")
    parser.add_argument("-q", "--quote", help="Vaccinations quote", action="store_true")
    parser.add_argument("-vf", "--vaccinationfirst", help="Number of people who recived their first vaccination", action="store_true")
    parser.add_argument("-vs", "--vaccinationsecond", help="Number of people who recived their second vaccination", action="store_true")
    parser.add_argument("-vb","--vaccinebrand",help="Number of vaccinations for a specified vaccine")
    parser.add_argument("-lvb","--listvaccinebrand",help="Lists all available vaccine brands and the amount of times they were being used", action="store_true")
    args = parser.parse_args()
    
    iu = ImpfungUpdate()
    area = ''
    if args.prefix:
        iu.prefix = args.prefix
    if args.bundesland:
        area = args.bundesland.upper()
    if args.all:
        print(iu.prefix + f"{iu.get_vac_all(area):,}")
    elif args.listareas:
        iu.all_areas()
    elif args.difference:
        print(iu.prefix + f"{iu.get_vac_all_delta(area):,}")
    elif args.differencefirst:
        print(iu.prefix + f"{iu.get_vac_first_delta(area):,}")
    elif args.differencesecond:
        print(iu.prefix + f"{iu.get_vac_second_delta(area):,}")
    elif args.quote:
        print(iu.prefix + str(iu.get_vac_quote(area)))
    elif args.vaccinationfirst:
        print(iu.prefix + f"{iu.get_vac_first(area):,}")
    elif args.vaccinationsecond:
        print(iu.prefix + f"{iu.get_vac_second(area):,}")
    elif args.vaccinebrand:
        print(iu.prefix + f"{iu.get_vac_by_brand(area,args.vaccinebrand):,}")
    elif args.listvaccinebrand:
        print(iu.prefix + json.dumps(iu.get_all_vac_brands(area),indent=4))
    else:
        print("Please use help to see your options (--help)")
