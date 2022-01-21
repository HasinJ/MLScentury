import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from dateutil.relativedelta import relativedelta
import datetime
import time
import sys
import pandas as pd
import regex as re
import requests
import json
import random
import functools
from fake_useragent import UserAgent

class Parser():

    def __init__(self, url, headerBase):
        self.__headerBase = headerBase
        self.__html = self.requestHouseInfo(url)
        self.__extractions = {}

    def requestHouseInfo(self, url):
        time.sleep(random.randint(3,6))
        self.__headerBase['user-agent'] = UserAgent().random
        with requests.Session() as s:
            r=s.get(url,headers=self.__headerBase)
            return r.content

    def transform(self, test=False):
        soup = BeautifulSoup(self.__html, 'html.parser')
        #self.printSoup(soup)

        #address
        address = soup.find("div", {"itemprop" : re.compile(r'^streetAddress')})
        if not address:
            print("No address found")
            return False
        address = self.__transformAddress(address.contents, test)

        #details
        details = self.__transformDetails(soup, test)


        self.__extractions = {
            'address': address,
            'details': details,
        }
        return True

    def __transformAddress(self, address, test):
        street = address[0].strip()
        city = address[1].contents[0].strip()
        state = address[3].contents[0].strip()
        postal = address[5].contents[0].strip()

        if test: print(address)
        if test: print(f"{street}\n{city}\n{state}\n{postal}\n")

        return {
            'street': street,
            'city': city,
            'state': state,
            'postal': postal,
        }

    def __transformDetails(self, soup, test=False):
        details = {'listing': '', 'acres': 0, 'price': 0, 'tax': 0, 'baths': 0, 'beds': 0, 'halfbaths': 0}



        taxes = soup.find(id='mt_propertyTax')
        taxes = self.__cleanPrice(taxes['value'])
        if test: print(f'tax: {taxes}')

        price = soup.find("meta", {"itemprop" : re.compile(r'^price')})
        price = self.__cleanPrice(price['content'])
        if test: print(f'price: {price}')

        listType = soup.find("div", {"class" : re.compile(r'^property-image-flag')})
        if not listType: listType='old_listed'
        else: listType = listType.contents[0].strip().replace(" ", '_').lower()
        if test: print(f'listing type: {listType}')

        details['tax'], details['price'], details['listing'] = taxes, price, listType

        info = soup.find("div", {"class" : re.compile(r'^pdp-info-bbsa')}).find_all("span", {"class": "pdp-info-bbsa-element"})
        for content in info:
            if content.contents[1].strip() in ['bath', 'baths']:
                details['baths'] = content.contents[0].contents[0]
            elif content.contents[1].strip() in ['bed', 'beds']:
                details['beds'] = content.contents[0].contents[0]
            elif content.contents[1].strip() in ['half bath', 'half baths']:
                details['halfbaths'] = content.contents[0].contents[0]
            elif content.contents[1].strip() in ['sq. ft.']:
                details['acres'] = content.contents[0].contents[0].replace(',','')
        #if test: print(f"baths, beds, and halfbaths: {details['baths']}, {details['beds']}, {details['halfbaths']}")
        if test: print(details)
        return details

    def __cleanPrice(self, string): return string.replace('$','').replace(',','')

    def saveHTML(self, dir):
        html_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), dir)
        with open(html_file, 'wb') as f:
            f.write(self.__html)

    def printSoup(self, soup):
        print(soup.prettify())

    def getExtractions(self): return self.__extractions

    #def setExtractions(self, extr): self.__extractions=extr
