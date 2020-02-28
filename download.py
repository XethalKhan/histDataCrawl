import requests
import datetime

f = open("hashes.txt", "r")

start = datetime.datetime.now()

print("Start " + str(start))

for line in f:

	params = line.strip().split(",")

	send={"tk": params[2], "date": params[1], "datemonth": params[1], "platform": "MT", "timeframe": "M1", "fxpair": params[0]}

	headers = {
		#"Sec-Fetch-Dest": "iframe", 
		#"Sec-Fetch-Mode": "navigate",
		#"Sec-Fetch-Site": "same-origin",
		#"Sec-Fetch-User": "?1",
		"Referer": "no-referrer-when-downgrade"#behind proxy
	}

	r = requests.post(
		"http://www.histdata.com/get.php", 
		data = send,
		headers = headers)

	name = params[0] + "_" + params[1]

	with open("data/" + name + ".zip", "wb") as fd:
	    for chunk in r.iter_content(chunk_size=128):
	        fd.write(chunk)
	    fd.close()

print("End " + str(datetime.datetime.now()))