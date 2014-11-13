import chk, urlutil, StringIO
from ostn02python import OSGB
from ostn02python import OSTN02
def FixSmallArea(lats, lons, username = None, password = None):

	url = "http://fosm.org/api/0.6/map?bbox={0},{1},{2},{3}".format(min(lons), min(lats), max(lons), max(lats))

	body, header = urlutil.Get(url)
	bodyStr = StringIO.StringIO(body)
	chk.CheckFile(bodyStr, username=username, password=password)

def TryTransform(x, y, lats, lons):
	try:
		(xa,ya,ha) = OSTN02.OSGB36_to_ETRS89 (x, y)
		(gla1, glo1) = OSGB.grid_to_ll(xa, ya)

		lats.append(gla1)
		lons.append(glo1)
	except:
		pass

if __name__=="__main__":

	#lats = [50.7595692, 50.7724678]	
	#lons = [-3.7165585, -3.6989885]

	username = "mapping@sheerman-chase.org.uk" #raw_input("Username:")
	password = raw_input("Password:")

	xin, yin = OSGB.parse_grid("SX", 00000, 00000)
	xin2, yin2 = OSGB.parse_grid("ST", 00000, 00000)


	#print xin, yin
	#print xin2, yin2

	for x in range(xin, xin2, 1000):
		for y in range(yin, yin2, 1000):

			lats, lons = [], []
			
			TryTransform(x, y, lats, lons)
			TryTransform(x+1000, y, lats, lons)
			TryTransform(x, y+1000, lats, lons)
			TryTransform(x+1000, y+1000, lats, lons)
			
			if len(lats) == 0: continue

			print x, y, lats, lons
			FixSmallArea(lats, lons, username=username, password=password)

