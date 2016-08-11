from bs4 import BeautifulSoup
from urllib.request import urlopen

from selenium import webdriver

import os

class meta_tag_extractor():
    def __init__(self):
        self.chromedriver = None
        self.driver = None

    def init_webdriver(self):
        self.driver = webdriver.Chrome(self.chromedriver)

    def close_webdriver(self):
        self.driver.quit()

    def set_chrome_driver(self, driver_location):
        self.chromedriver = driver_location
        os.environ["webdriver.chrome.driver"] = self.chromedriver

    def get_tags(self, f):
        r = {}
        soup3 = BeautifulSoup(f, 'lxml')

        desc = soup3.findAll('title')
        try:
            r.update({'title': desc[0].get_text()})
        except IndexError:
            pass

        desc = soup3.findAll(attrs={"name": "description"})
        try:
            r.update({'description': desc[0]['content']})
        except IndexError:
            pass

        desc = soup3.findAll(attrs={"name": "keywords"})
        try:
            r.update({'keywords': desc[0]['content']})
        except IndexError:
            pass

        return r

    def extract_tags_using_urllib(self, url):

        f = urlopen(url).read()
        r = self.get_tags(f)

        return r

    def extract_tags_using_chrome(self, url):
        if self.driver == None:self.init_webdriver()

        driver = self.driver

        driver.get(url)
        f = driver.page_source
        r = self.get_tags(f)

        return r


if __name__ == '__main__':
    meta_tag_extractor = meta_tag_extractor()
    meta_tag_extractor.set_chrome_driver("c:/temp/chromedriver.exe")
    print(meta_tag_extractor.extract_tags_using_urllib("http://www.buybuybaby.com/"))
    print(meta_tag_extractor.extract_tags_using_chrome("http://www.buybuybaby.com/"))
    meta_tag_extractor.close_webdriver()
