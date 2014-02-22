#!/usr/bin/env python

"""

Dies ist alles doku...



Usage:
	server.py  
	server.py -t

--vdr-host=<vdrhost>	hostname of the svdrp server.
--vdr-port=<vdrport>	port of the svdrp server [default: 6419].

"""

from flask import Flask, render_template, request
from docopt import docopt
from telnetlib import Telnet
from pprint import pprint
import json
import string
import sys
from collections import namedtuple

app = Flask(__name__)

Channel = namedtuple('Channel', ['id', 'name'])

def getchannellist(host="192.168.1.23", port=6419):
	t = Telnet(host, port)
	t.write("LSTC\nQUIT\n")
	lines = t.read_all().split("\r\n")
	lines = filter(lambda s: s.startswith("250"), lines)
	items = map(lambda s: Channel(*s[4:].split(";")[0].split(" ",1)), lines)
	return items

CHANNELS = getchannellist()
HOST="192.168.1.23"
PORT=6419

@app.route("/")
def index():
	return render_template("main.html", channels=CHANNELS)

@app.route("/debug")
def debug():
	print request.args
	return ""

@app.route("/switchStation")
def switchStation():
	sendCommand("CHAN "+request.args.get("station"))
	return json.dumps(dict(result=True))


def sendCommand(command):
	t = Telnet(HOST, PORT)
	t.write(str(command)+"\nQUIT\n")
	t.read_all()
	t.close()
	return ""


if __name__ == '__main__':
	options = docopt(__doc__)
	print options
	if options.get('-t'):
		getchannellist()
		sys.exit(1)

	app.debug = True
	app.run(host="0.0.0.0", port=8080)
	


