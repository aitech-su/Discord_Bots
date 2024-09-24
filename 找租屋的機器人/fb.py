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

    prev_text = ''
    while True:
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values':{'notifications': 2}}
        options.add_experimental_option('prefs', prefs)
        options.add_extension('ublock_origin.crx')
        driver = webdriver.Chrome(options=options)
        driver.get('https://mbasic.facebook.com')

        account_field = driver.find_element(By.NAME, 'email')
        account_field.send_keys('')
        password_field = driver.find_element(By.NAME, 'pass')
        password_field.send_keys('')
        password_field.send_keys(Keys.RETURN)
        driver.get('https://www.facebook.com/?sk=h_chr')

        for _ in range(45):
            time.sleep(36)
            driver.refresh()

            time.sleep(2)
            buttons = driver.find_elements(By.CLASS_NAME, 'x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1sur9pj.xkrqix3.xzsf02u.x1s688f')
            for button in buttons:
                if (button.text == 'See more'):
                    button.click()
                    break
            time.sleep(2)

            elements = driver.find_elements(By.CLASS_NAME, 'html-span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs')
            group = ''
            poster = ''
            if elements:
                group = elements[0].text
                if len(elements) >= 2:
                    poster = elements[1].text.split('\n')[0]
            text = '```' + group + '\n' + poster + '\n\n'

            elements = driver.find_elements(By.CLASS_NAME, 'xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.x126k92a')
            parents = None
            if elements:
                parents = elements[0].find_elements(By.XPATH, './..')
                text += elements[0].text

            for e in driver.find_elements(By.CLASS_NAME, 'x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.xtlvy1s.x126k92a'):
                if parents and e.find_element(By.XPATH, './..') == parents[0]:
                    text += '\n' + e.text
                else:
                    break
            text += '```'

            elements = driver.find_elements(By.CLASS_NAME, 'x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x4zkp8e.x676frb.x1nxh6w3.x1sibtaa.x1s688f.xi81zsa.x2b8uid')
            if elements:
                marker = ' turned off commenting for this post.'
                if (elements[0].text.endswith(marker)):
                    name = elements[0].text.split(marker)[0]
                    if name == poster:
                        continue

            if '租' not in text and '房' not in text and '屋' not in text:
                continue

            if '求租' in text:
                continue

            maximum = 9500
            expensive = False
            lines = text.split('\n')
            for line in lines:
                cleaned_line = line.replace(',', '')
                match = re.search(r'(\d+).*/月', cleaned_line)
                if match:
                    number = match.group(1)
                    num_value = int(number[:])
                    if num_value > maximum:
                        expensive = True

                if '租金' in line or '月租' in line:
                    match = re.search(r'(\d+)(\D?)', cleaned_line)
                    if match:
                        start_index = match.start(1)
                        end_index = match.start(2)
                        number = cleaned_line[start_index:end_index]
                        num_value = int(number)
                        if num_value > maximum:
                            expensive = True
            if expensive:
                continue

            if "#尋找優質租客" in text or "感謝管理員審核～" in text:
                continue

            if prev_text == text:
                continue
            prev_text = text
            
            while True:
                with lock:
                    if post is None:
                        post = text
                        break

        driver.close()