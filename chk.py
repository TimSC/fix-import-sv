import fix, osmmod, urlutil
import xml.etree.ElementTree as ET

def CheckFile(fi, username = None, password = None):
	importWayIds, importRelationIds = fix.CheckFi(fi)

	print "ways", importWayIds
	print "relations", importRelationIds

	if username is None:
		username = raw_input("Username:")
	if password is None:
		password = raw_input("Password:")
	userpass = username+":"+password

	cid = None
	baseurl = "http://fosm.org/api"
	exe=1
	verbose = 0

	for wayId in importWayIds:
		print wayId
		url = baseurl+"/0.6/way/{0}/full".format(wayId)
		urlData, urlHeader = urlutil.Get(url)
		responseCode = urlutil.HeaderResponseCode(urlHeader)
		if responseCode == "HTTP/1.1 410 Gone":
			print "Way",wayId,"is gone"
			continue

		wayRoot = ET.fromstring(urlData)

		memberNodes = {}

		for dat in wayRoot:
			if dat.tag == "way":
				wayVer = int(dat.attrib["version"])
			if dat.tag == "node":
				nodeId = int(dat.attrib["id"])
				memberNodes[nodeId] = dat

		if cid is None:
			cid, status = osmmod.CreateChangeSet(userpass, {'comment':"Fix import"}, baseurl, exe=exe, verbose=verbose)
			print "Created changeset", cid
			assert cid > 0

		print "Delete way", wayId
		osmmod.DeleteWay(userpass, cid, baseurl, wayId, wayVer, exe=exe)

		nidLi, existingVersionLi, latLi, lonLi = [], [], [], []
		for nodeId in memberNodes:
			node = memberNodes[nodeId]
			print "Delete node", nodeId
			nodeVer = node.attrib["version"]
			lat = node.attrib["lat"]
			lon = node.attrib["lon"]
			nidLi.append(nodeId)
			existingVersionLi.append(nodeVer)
			latLi.append(lat)
			lonLi.append(lon)
			#osmmod.DeleteNode(userpass, cid, baseurl, nodeId, nodeVer, lat, lon, exe=exe, verbose=verbose)
		osmmod.DeleteNodes(userpass, cid, baseurl, nidLi, existingVersionLi, latLi, lonLi, exe=exe, verbose=verbose)

	for relId in importRelationIds:
		print relId
		url = baseurl+"/0.6/relation/{0}/full".format(relId)
		urlData, urlHeader = urlutil.Get(url)
		responseCode = urlutil.HeaderResponseCode(urlHeader)
		if responseCode == "HTTP/1.1 410 Gone":
			print "Relation",relId,"is gone"
			continue

		root = ET.fromstring(urlData)

		memberNodes = {}
		memberWays = {}
		relationVer = None

		for dat in root:
			if dat.tag == "relation":
				relationVer = int(dat.attrib["version"])
			if dat.tag == "way":
				objId = int(dat.attrib["id"])
				memberWays[objId] = dat
			if dat.tag == "node":
				nodeId = int(dat.attrib["id"])
				memberNodes[nodeId] = dat

		if cid is None:
			cid, status = osmmod.CreateChangeSet(userpass, {'comment':"Fix import"}, baseurl, exe=exe, verbose=verbose)
			print "Created changeset", cid
			assert cid > 0

		print "Delete relation", relId
		osmmod.DeleteRelation(userpass, cid, baseurl, relId, relationVer, exe=exe)

		for wayId in memberWays:
			wayVer = memberWays[wayId]

			print "Delete way", wayId
			osmmod.DeleteWay(userpass, cid, baseurl, wayId, wayVer, exe=exe)

		nidLi, existingVersionLi, latLi, lonLi = [], [], [], []
		for nodeId in memberNodes:
			node = memberNodes[nodeId]
			print "Delete node", nodeId
			nodeVer = node.attrib["version"]
			lat = node.attrib["lat"]
			lon = node.attrib["lon"]
			nidLi.append(nodeId)
			existingVersionLi.append(nodeVer)
			latLi.append(lat)
			lonLi.append(lon)
			#osmmod.DeleteNode(userpass, cid, baseurl, nodeId, nodeVer, lat, lon, exe=exe, verbose=verbose)
		osmmod.DeleteNodes(userpass, cid, baseurl, nidLi, existingVersionLi, latLi, lonLi, exe=exe, verbose=verbose)

	if cid is not None:
		print "Close changeset"
		osmmod.CloseChangeSet(userpass, cid, baseurl, exe=exe, verbose=verbose)


if __name__ == "__main__":

	fi = open("/home/tim/Desktop/woodmixed.osm")
	CheckFile(fi)

