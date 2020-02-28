import threading
import datetime
import os
from time import sleep

import requests
from bs4 import BeautifulSoup

from ref import source

#https://www.tutorialspoint.com/python/python_multithreading.htm
class preprocessThread(threading.Thread):

	def __init__(self, curr, year):
		threading.Thread.__init__(self)
		self.curr = curr
		self.year = year

	def run(self):

		global threadLock, f

		r = requests.get("http://www.histdata.com/download-free-forex-historical-data/?/metatrader/1-minute-bar-quotes/"+ k + "/" + str(i))

		if(r.status_code == 200):

			obj= BeautifulSoup(r.text, "html.parser")
			file_hash = obj.find(id="file_down").find(id="tk")["value"]
			txt = self.curr + "," + str(self.year) + "," + file_hash

			threadLock.acquire()
			f.write(txt + "\n")
			threadLock.release()

		else:
			print("Error currency pair = " + self.curr + ", year = " + str(self.year))

print("Preparing hashes.csv file")
start = datetime.datetime.now()

if os.path.exists("hashes.csv"):
    os.remove("hashes.csv")

threads = []
threadLock = threading.Lock()
f = open("hashes.csv", "a")

for k, v in source.items():
	pause = 1
	for i in range(v, 2020):
		if pause > 8:
			sleep(0.2)	#Added because on to many requests per second www.histdata.com returns 500 (database down)
			pause = 1
		pause+=1
		t = preprocessThread(k, i)
		t.start()
		threads.append(t)

for z in threads:
    z.join()

end = datetime.datetime.now()
print("End processing, duration: " + str(end - start))



