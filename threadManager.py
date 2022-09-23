import requests
import json
import time
import threading

URL = "url"

class ThreadVariable():
    def __init__(self):
        self.lock = threading.Lock()
        self.lockedValue = 0
 
    def plus(self, value):
        self.lock.acquire()
        try:
            if self.lockedValue <= 5000:
                self.lockedValue += value
        finally:
            self.lock.release()

class CounterThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
 
    def run(self):
        global totalCount
 
        for _ in range(10):
            response = requests.post(URL)
            params = json.loads(response.text)
            totalCount.plus(params['body']['value'])

if __name__ == '__main__':
    global totalCount
    round = 1

    print('회차 누적값 소요시간(ms)')

    for _ in range(5):
        start = time.time()
        totalCount = ThreadVariable()

        for _ in range(100):
            timerThread = CounterThread()
            timerThread.start()

        mainThread = threading.currentThread()
        for thread in threading.enumerate():
            if thread is not mainThread:
                thread.join()

        end = time.time()
        print(f'{round} ' + str(totalCount.lockedValue) + f' {int((end-start)*1000)}')
        round += 1
        time.sleep(1000)
