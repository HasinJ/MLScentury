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
import csv
from fake_useragent import UserAgent

#my imports
from parsers import Parser
from queries import Queries

#https://www.century21.com/real-estate/new-jersey/LSNJ/

class Scraper():

    def __init__(self, driver):
        self.driver = driver
        self.urlbase = "https://www.century21.com/"
        self.headerBase = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent': UserAgent().random
        }
        self.mainSoup = None
        self.count = 0

    def start(self, startingUrl, test=False):
        r=None
        with requests.Session() as s:
            r=s.get(startingUrl,headers=self.headerBase)
        self.mainSoup = BeautifulSoup(r.content, 'html.parser')
        self.maxItems = int(self.mainSoup.find("div", {"class" : re.compile(r'^results-label')})['data-count'])
        print(f'max items: {self.maxItems}')

    def extract(self):
        hrefs = self.mainSoup.find_all("a", {"href" : re.compile(r'^/property/')})
        for href in hrefs:
            href = href['href']
            print(f"\n{href}")
            self.count+=1

            parser = Parser(self.urlbase + href, self.headerBase)
            #parser.saveHTML(fr"data\html\html{self.count}.html")
            if not parser.transform(): continue

            queries = Queries(parser.getExtractions())
            queries.loadAddress()
            queries.loadRef(href)
            queries.loadDetails()
            queries.cursor.close()

            del(parser, queries)
            #if(counter==1): return
            print("\n")
            if(test.count>=test.maxItems): return
            time.sleep(random.randint(3,6))
        print(self.count)

    def testOneHouse(self, url):
        print(url)
        parser = Parser(url, self.headerBase)
        parser.saveHTML(fr"data\html\TEST.html")
        if not parser.transform(test=True): return

        href = url.split("/property/")[-1]

        queries = Queries(parser.getExtractions())
        queries.loadAddress(test=True)
        queries.loadRef(href, test=True)
        queries.loadDetails(test=True)
        queries.cursor.close()

        del(parser, queries)

    def printSoup(self, soup):
        print(soup.prettify())

    def setDriver(self, driver): self.driver=driver


if __name__ == '__main__':
    test = Scraper(None)
    url = 'https://www.century21.com/real-estate/new-jersey/LSNJ'
    test.start(url)
    """
    pageCount = 1
    while(test.count<test.maxItems):
        print(f"\n\nPAGE: {pageCount}\n")
        if pageCount!=1: test.start(url + f"/?p={pageCount}")
        test.extract()
        #if pageCount==2: break
        pageCount+=1
        time.sleep(random.randint(3,6))
    """

    #test.start("https://www.century21.com/real-estate/new-jersey/LSNJ/?p=1", test=True)
    test.testOneHouse("https://www.century21.com/property/21-poplar-avenue-whitestown-ny-13492-ERA50288494")
