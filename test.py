from telnetlib import Telnet
from pprint import pprint

def getchannellist(host="192.168.1.23", port=6419):
	t = Telnet(host, port)
	t.write("LSTE\nQUIT\n")
	items = t.read_all().split("\r\n")
	#lines = filter(lambda s: s.startswith("250"), lines)
#	items = map(lambda s: s[4:].split(":"), lines)
	return items


#pprint(getchannellist())
