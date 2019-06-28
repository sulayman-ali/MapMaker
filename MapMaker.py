# coding: utf-8
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from math import *
import requests
import cartopy.io.shapereader as shpreader
import time
import itertools
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from googlemaps import Client
from geopy.geocoders import GoogleV3
key= "YOUR_API_KEY"
locations = pd.read_excel('YOUR_LOCATIONS') 
separator = ", "
locations["google"] = locations["Street Address"].map(str) + separator + locations["City"]
#combines street address and city columns with a comma and space in between

def getcoordinates(locations):
    """
    input is list of addresses
    """
    latgc = []
    lnggc = []
    for address in locations['google']:
            #print(address)
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={key}".format(query=address, key = key)
            response = requests.get(url).text
            res = json.loads(response)
            if res['status'] == "ZERO_RESULTS":             
                continue
            rc = res['results'][0]['geometry']['location']
            latgc.append(rc['lat'])
            lnggc.append(rc['lng'])

    return list(zip(lnggc,latgc))
#test = (getcoordinates(locations))

def make_map(listOfTuples)
    fig=plt.figure(figsize=(18, 16))
    fig.set_canvas(plt.gcf().canvas)
    ax = plt.axes(projection=ccrs.PlateCarree())
    plt.figure(figsize=(20,20))
    plt.rcParams['figure.dpi'] = 200
    ax.set_extent([-150,60,-25,60])
    shpf = shpreader.natural_earth(resolution='110m', category='cultural', name='admin_0_countries')

    reader = shpreader.Reader(shpf)
    countries = reader.records()

    fig.set_size_inches(15,15)
    for country in countries:
        ax.add_geometries(country.geometry, ccrs.PlateCarree(), facecolor='#00A8C7', linewidth=0.5, edgecolor='white', 
                          label=country.attributes['ADM0_A3'])
    for item in listOfTuples:
         ax.scatter(item[0],item[1], c = '#F99136', edgecolors = '#00526F',zorder=10)

    fig.savefig("final_image_with_locs.png", format='png', dpi=200)

#make_map(test)
