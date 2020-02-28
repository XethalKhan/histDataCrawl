import datetime

import requests
from bs4 import BeautifulSoup

from ref import source

url = "http://www.histdata.com/download-free-forex-historical-data/?/metatrader/1-minute-bar-quotes"

f = open("hashes.txt", "w")

print(datetime.datetime.now())

for k, v in source.items():
	for i in range(v, 2020):
		r = requests.get(url + "/"+ k + "/" + str(i))
		obj= BeautifulSoup(r.text, "html.parser")
		txt = k + "," + str(i) + "," + obj.find(id="file_down").find(id="tk")["value"]
		f.write(txt + "\n")

print(datetime.datetime.now())
