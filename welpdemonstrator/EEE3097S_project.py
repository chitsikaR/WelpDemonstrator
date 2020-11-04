"""Main module."""
'''Python 3 API for the SN01 GPs module from XinaBox'''
'''Authors: Laurentia Naidu and Rachel Chitsika'''

'''import relevant packages'''
import pandas as pd
import geopandas as gpd
import json
import requests
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
import plotly_express as px
import tqdm
from tqdm._tqdm_notebook import tqdm_notebook
from firebase import firebase
from time import sleep
import pigpio
import pynmea2

'''initialise local and global variables'''
pi = pigpio.pi()
addr = 0x42
bus = 1
len = 0xFD
getdata = 0xFF
global currentTime
global currentLat
global currentLong
global loc
firebase = firebase.FirebaseApplication('https://welp-2b4f8.firebaseio.com/', None)

# Alamanac token available at: http://www.u-blox.com/services-form.html
token="MLh4BcS6kU2BLgO-MeLYHQ"

# download GNSS almanac
def getAlamanac():
    '''download a GNSS almanac to severely reduce Time-To-First-Fix'''

    almanac_url = f"http://online-live1.services.u-blox.com/GetOnlineData.ashx?token={token};gnss=gps;datatype=eph,alm,aux,pos;filteronpos;format=aid"
    request_url = requests.get(almanac_url)
    handle = pi.i2c_open(bus, addr)
    pi.i2c_write_device(handle, request_url.content)
    pi.i2c_close(handle)


# get location data from GPS module
# adapted from https://github.com/xinabox/Python-SN01.git
def getSN01_data():
    '''reads in and processes GPS data received by SN01 GPS module '''

    readline = 0
    handle = pi.i2c_open(bus, addr)
    try:
        dl = pi.i2c_read_word_data(handle, len)//256
        if dl>0:
            (readline, data) = pi.i2c_zip(handle,[4, addr, 7, 1, getdata, 6, dl, 0])
    except:
        pass
    pi.i2c_close(handle)
    if readline>0:
        return data.decode(encoding='UTF-8',errors='ignore').splitlines()
    return None


# post GPS data to database
def postGPSDatatoDB(latitude_test, longitude_test):
    '''Takes in GPS coordinates and posts to remote databse'''

    gps = firebase.post('/Latitude', latitude_test)
    gps2 = firebase.post ('/Longitute', longitude_test)
    global loc
    loc = (str(latitude_test) +  ' ' + str(longitude_test))
    gpsLocation = firebase.post('/Location', loc)


# gets the current location of the user as (lat, long)
def getCurrentLocation():
    '''Retrieve most recent location entry in database'''

    location_ = firebase.get('/Location', '')
    return (location_)


# get last 20 locations from database
def getMostRecentLocations():
    '''Retrieves a list of the last 24 logged locations i.e the last 2 hours'''

    recent_list = firebase.get('/Location', '')
    return (location_)


# generate message as string
def getTextMessage():
    '''Compiles a string message with the relevant data'''

    # User can enter their own name
    global currentLat
    global currentLong
    global currentTime
    text_message = '***DISTRESS SIGNAL*** \n'
    text_message = text_message + 'Laurentia is in danger now at:\n'
    text_message = text_message + getAddress() + '\n'
    text_message = text_message + ('Lat: ' + '{:.2f}'.format(currentLat) +' Long: ' + '{:.2f}'.format(currentLong))
    return text_message


# use lat and long to get address
def getAddress():
    '''Convert the current location to a nearby street address'''

    locator = Nominatim(user_agent='myGeocoder')
    currentCoordinates = getCurrentLocation()
    location = locator.reverse(currentCoordinates)
    location.raw
    return (location.address)


# while startFlag is true, data is collected
def formatData():
    '''Collects GPS data while the application is running'''

    global currentTime
    global currentLat
    global currentLong

    while(True):
        data = getSN01_data()
        if data:
            for i in data:
                try:
                    message = pynmea2.parse(i, check=True)
                    currentTime = message.timestamp
                    currentLat = message.latitude
                    currentLong = message.longitude
                    postGPSDatatoDB(currentLat, currentLong)
                except:
                    pass

        sleep(300) # read data every 5 minutes

if __name__ == "__main__":
    getAlamanac()
