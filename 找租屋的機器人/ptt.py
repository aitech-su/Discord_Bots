import PyPtt
import threading
import time

lock = threading.Lock()
post = None

def update_post():
    global post

    ptt = PyPtt.API()
    ptt.login('', '')
    prev_index = 0

    while True:
        time.sleep(3)

        index = ptt.get_newest_index(PyPtt.NewIndex.BOARD, 'Rent_tao')
        if prev_index == index:
            continue
        prev_index = index

        info = ptt.get_post('Rent_tao', index=index)
        text = '```' + info['title'] + '\n' + info['content'] + '```'

        if '新竹' not in text:
            continue

        if text.startswith('[徵'):
            continue

        while True:
            with lock:
                if post is None:
                    post = text
                    break