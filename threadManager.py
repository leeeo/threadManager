import requests
import json
from queue import Queue
import time
import threading

URL = "https://eai.mrcamel.co.kr/devops"
que = Queue(100)

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
            que.put(params['body']['value'])
            totalCount.plus(que.get())

if __name__ == '__main__':
    global totalCount
    round = 1

    print('회차 누적값 소요시간(ms)')

    totalCount = ThreadVariable()
    start = time.time()

    for _ in range(100):
        timerThread = CounterThread()
        timerThread.start()

    mainThread = threading.currentThread()
    for thread in threading.enumerate():
        if thread is not mainThread:
            thread.join()

    end = time.time()
    print(f'{round} ' + str(totalCount.lockedValue) + f' {int((end-start)*1000)}')
    
