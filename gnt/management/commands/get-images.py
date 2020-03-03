from django.core.management.base import BaseCommand, CommandError
from gnt.models import Drinks, Drink_names
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from django.conf import settings
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os
import argparse
import requests
import urllib
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import time

class Command(BaseCommand):

    def _get_image(self, browser, drink):
        d_name, d_id = drink['names'][0], drink['id']
        if '&' in d_name:
            d_name = d_name.replace('&', '%26')
        searchurl = f'https://www.google.com/search?q={d_name} cocktail&source=lnms&tbm=isch'
        result_dir = f'gnt/static/data/drink_images/{d_id}'
        if not os.path.exists(result_dir):
            if drink['picture'] == 'images/placeholder.jpg':
                result_dir = f'gnt/static/data/drink_images/00000000from_google/{d_id}'
                os.mkdir(result_dir)
                browser.get(searchurl)
                time.sleep(1)
                page_source = browser.page_source
                soup = BeautifulSoup(page_source, 'lxml')
                images = soup.find_all('img')
                urls = []
                for image in images:
                    try:
                        url = image['data-src']
                        if not url.find('https://'):
                            urls.append(url)
                    except:
                        try:
                            url = image['src']
                            if not url.find('https://'):
                                urls.append(image['src'])
                        except Exception as e:
                            print(f'No found image sources.')
                            print(e)
                count = 0
                if urls:
                    for url in urls:
                        try:
                            res = requests.get(url, verify=False, stream=True)
                            rawdata = res.raw.read()
                            with open(os.path.join(result_dir, 'img_' + d_id + '__' + str(count) + '.jpg'), 'wb') as f:
                                f.write(rawdata)
                                count += 1
                        except Exception as e:
                            print('Failed to write rawdata.')
                            print(e)
                return f'SAVED {count} IMAGES FOR {d_id}'
            else:
                os.mkdir(result_dir)
                try:
                    res = requests.get(drink['picture'], verify=False, stream=True)
                    rawdata = res.raw.read()
                    with open(os.path.join(result_dir, 'img_' + d_id + '.jpg'), 'wb') as f:
                        f.write(rawdata)
                except Exception as e:
                    print('Failed to write rawdata.')
                    print(e)
                return f'SAVED A SINGLE IMAGE FOR {d_id}'
        else:
            return f'IMAGES ALREADY SAVED FOR {d_id}'

    def handle(self, *args, **options):
        urllib3.disable_warnings(InsecureRequestWarning)
        chromedriver = 'C:/Program Files/chromedriver/chromedriver/chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        try:
            browser = webdriver.Chrome(chromedriver, options=options)
        except Exception as e:
            print(f'No found chromedriver in this environment.')
            print(f'Install on your machine. exception: {e}')
        browser.set_window_size(1280, 1024)
        environment_id = 'b7d1486c-2fdc-40c5-a2ce-2d78ec48fa76'
        collection_id = '7c11f329-5f31-4e59-aa63-fde1e91ff681'
        authenticator = IAMAuthenticator(getattr(settings, 'WATSON_DISCOVERY_API_KEY', None))
        discovery = DiscoveryV1(version='2019-04-30',authenticator=authenticator)
        discovery.set_service_url('https://api.us-south.discovery.watson.cloud.ibm.com/')
        response = discovery.query(environment_id, collection_id, _return=['id','names', 'picture'], count='1000').result['results']
        for i in response:
            result = self._get_image(browser, i)
            print(result)
        browser.close()
        