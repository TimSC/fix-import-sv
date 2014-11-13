import xml.etree.ElementTree as ET
import urlutil

def CheckWays(objMap):

	importWayIds = []

	#Find woods at version 1 by me (ways)
	for objId in objMap["way"]:
		way = objMap["way"][objId]

		#print objId, way.attrib["version"]
		if int(way.attrib["version"]) != 1: continue
		if way.attrib["user"] != "TimSCStreetViewImport": continue
		#print way.attrib

		woodTagFound = False
		for wayDat in way:
			if wayDat.tag != "tag": continue
			if wayDat.attrib["k"] != "natural": continue
			if wayDat.attrib["v"] == "wood": woodTagFound = True

		if not woodTagFound:
			continue
	
		#print objId

		#Check nodes are version 1
		highVerNodeFound = False
		for wayDat in way:
			if wayDat.tag != "nd": continue
			nodeId = int(wayDat.attrib["ref"])
			node = objMap["node"][nodeId]
			nodeVer = int(node.attrib["version"])
			if nodeVer > 1:
				highVerNodeFound = True

		if highVerNodeFound:
			continue

		importWayIds.append(objId)

	return importWayIds

def CheckRelation(objMap):

	importWayIds = []

	#Find woods at version 1 by me (ways)
	for objId in objMap["relation"]:
		relation = objMap["relation"][objId]

		#print objId, way.attrib["version"]
		if int(relation.attrib["version"]) != 1: continue
		if relation.attrib["user"] != "TimSCStreetViewImport": continue
		#print relation.attrib

		woodTagFound = False
		for dat in relation:
			if dat.tag != "tag": continue
			if dat.attrib["k"] != "natural": continue
			if dat.attrib["v"] == "wood": woodTagFound = True

		if not woodTagFound:
			continue
	
		#print objId

		#Check members are version 1
		highVerNodeFound = False
		for dat in relation:
			if dat.tag != "member": continue
			if dat.attrib["type"] != "way": continue
			memId = int(dat.attrib["ref"])

			url = "http://fosm.org/api/0.6/way/{0}/full".format(memId)
			urlData, urlHeader = urlutil.Get(url)
			wayRoot = ET.fromstring(urlData)

			for wayData in wayRoot:
				objVer = int(wayData.attrib["version"])

				if objVer > 1:
					highVerNodeFound = True

		if highVerNodeFound:
			continue

		importWayIds.append(objId)

	return importWayIds

def CheckFi(fi):
	#Sort into types
	objMap = {'node':{}, 'way': {}, 'relation': {}}
	bounds = []

	root = ET.fromstring(fi.read())
	for el in root:
		if el.tag == "bounds": 
			bounds.append(el)
			continue

		objId = int(el.attrib['id'])
		#print el.tag, objId
		objTy = str(el.tag)
		objMap[objTy][objId] = el

	importWayIds = CheckWays(objMap)

	importRelationIds = CheckRelation(objMap)
	return importWayIds, importRelationIds

if __name__ == "__main__":

	fi = open("/home/tim/Desktop/woodmixed.osm")

	username = "mapping@sheerman-chase.org.uk" #raw_input("Username:")
	password = raw_input("Password:")

	importWayIds, importRelationIds = CheckFi(fi, username=username, password=password)

	print "ways", importWayIds
	print "relations", importRelationIds



