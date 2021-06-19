#! /usr/bin/env python3

import time
import requests
import bs4

class StockCheck():
  def __init__(self, url):
    self.url = url

  def checkStock(self):
    '''Check if item is in stock.'''
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
    res = requests.get(self.url, headers=headers)

    res.raise_for_status()
    noStarchSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    buttons = noStarchSoup.select('button')
    divs = noStarchSoup.select('div')

    if 'sold out' in str(buttons).lower() or 'not available' in str(buttons).lower():
      print(f"{time.ctime()} Out of stock at {self.url}")
      return False
    else:
      print(f"{time.ctime()} Stock available at {self.url}")
      return True

  def getUrl(self):
    return self.url