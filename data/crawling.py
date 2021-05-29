#-*- coding: utf-8 -*-

import pandas as pd
from pandas import Series, DataFrame
from datetime import datetime, timedelta
import requests
import re
from bs4 import BeautifulSoup

#ALL USER
class Crawling():

    def __init__(self):
        self.naverURL = 'https://finance.naver.com/item/main.nhn?code={}'
        self.kospiCode = []
        self.kospiName = []
        self.kosdaqCode = []
        self.kosdaqName = []

    def loadKospi(self):
        return None

    def loadKosdaq(self):
        return None

    def updateKospiKosdaq(self):
        return None

    def companyInfo(self, company):
        return None

    def priceTimer(self, company, time):
        return None

    def targetPriceCheck(self, company, targetPrice):
        return None

    def getPrice(self, company):
        if company.isdigit() == False:
            return  None
        url = self.naverURL.format(company)
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        
        no_today = bs_obj.find("p", {"class" : "no_today"})
        blind = no_today.find("span", {"class" : "blind"})
        price = blind.text
        return price


if __name__ == '__main__':
    craw = Crawling()
    print(craw.getPrice('005930'))
    print(craw.getPrice('삼성전자'))
