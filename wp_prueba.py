# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.options import Options

# opts = Options
# opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"+"AppleWebKit/537.36 (KHTML, like Gecko)"+"Chrome/87.0.4280.141 Safari/537.36")

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader

class labels(Item):
    laber = Field()

class loginLabels(Spider):
    name = "Spider de Prueba"
    start_urls = ['http://192.168.101.1/admin/login.asp']

    def parse(self, response):
        sel = Selector(response)
        labels = sel.xpath('///font[@size="4"]')
