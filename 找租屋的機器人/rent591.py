from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import threading
import time
import re

lock = threading.Lock()
post = None

def update_post():
    global post

    prev_texts = ['', '']
    urls = ['https://rent.591.com.tw/?region=4&rentprice=5000,7000&order=posttime&kind=2',
            'https://rent.591.com.tw/?region=5&rentprice=5000,7000&section=60,54,61&kind=2&order=posttime']

    while True:
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values':{'notifications': 2}}
        options.add_experimental_option('prefs', prefs)
        options.add_extension('ublock_origin.crx')
        driver = webdriver.Chrome(options=options)

        for i in range(500):
            driver.get(urls[i % 2])
            time.sleep(4)

            elements = driver.find_elements(By.CLASS_NAME, 'item-msg')
            if not elements or elements[0].text.startswith('仲介'):
                continue

            elements = driver.find_elements(By.CLASS_NAME, 'vue-list-rent-item')
            if elements:
                text = elements[0].text

            link = ''
            elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="//rent.591.com.tw/"]')
            for e in elements:
                ref = e.get_attribute('href')
                if ref[-8:].isdigit() and e.text == text:
                    link = ref
                
            text = '```' + text + '\n\n' + link + '```'

            lines1 = prev_texts[i % 2].split('\n')
            lines2 = text.split('\n')
            if lines1[:5] == lines2[:5]:
                continue
            prev_texts[i % 2] = text
            
            while True:
                with lock:
                    if post is None:
                        post = text
                        break
        
        driver.close()

# update_post()