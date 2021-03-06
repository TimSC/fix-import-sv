import urlutil
import xml.etree.ElementTree as ET
import xml.sax.saxutils as saxutils

def CreateChangeSet(userpass, tags, baseurl, verbose=0, exe=1):
	#Create a changeset
	createChangeset = "<?xml version='1.0' encoding='UTF-8'?>\n" +\
	"<osm version='0.6' generator='py'>\n" +\
	"  <changeset>\n"
	for k in tags:
		createChangeset += '<tag k="{0}" v="{1}"/>\n'.format(saxutils.escape(k), saxutils.escape(tags[k])).encode('utf-8')
	createChangeset += "  </changeset>\n" +\
	"</osm>\n"

	if verbose >= 2:
		print createChangeset

	if exe:
		response = urlutil.Put(baseurl+"/0.6/changeset/create",createChangeset,userpass)
		if verbose >= 1: print response
		if len(response[0]) == 0:
			print response
			return (0,"Error creating changeset")
		try:
			cid = int(response[0])
		except:
			cid = None
		if urlutil.HeaderResponseCode(response[1]) != "HTTP/1.1 200 OK": 
			print response
			return (0,"Error creating changeset")
	else:
		cid = 1001
	return (cid, "Done")

def CloseChangeSet(userpass, cid, baseurl, verbose=0, exe=1):
	#Close the changeset
	if exe:
		response = urlutil.Put(baseurl+"/0.6/changeset/"+str(cid)+"/close","",userpass)
		if verbose >= 1: print response
		if urlutil.HeaderResponseCode(response[1]) != "HTTP/1.1 200 OK": return (0,"Error closing changeset")

def CreateNode(userpass, cid, baseurl, lat, lon, tags, verbose=0, exe=1):

	xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
	xml += '<osmChange version="0.6" generator="py">\n<create>\n<node id="-1" lat="{0}" lon="{1}" changeset="{2}">\n'.format(lat, lon, cid)
	for k in tags:
		xml += '<tag k="{0}" v="{1}"/>\n'.format(saxutils.scape(k), saxutils.escape(tags[k])).encode('utf-8')
	xml += '</node>\n</create>\n</osmChange>\n'
	if verbose >= 2: print xml
	newId = None
	newVersion = None

	if exe:
		response = urlutil.Post(baseurl+"/0.6/changeset/"+str(cid)+"/upload",xml,userpass)
		if verbose >= 1: print response
		if urlutil.HeaderResponseCode(response[1]) != "HTTP/1.1 200 OK": return None

		respRoot = ET.fromstring(response[0])
		for obj in respRoot:
			newId = obj.attrib['new_id']
			newVersion = obj.attrib['new_version']

	return int(newId), int(newVersion)

def ModifyNode(userpass, nid, cid, baseurl, lat, lon, tags, existingVersion, verbose=0, exe=1):

	xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
	xml += '<osmChange version="0.6" generator="py">\n<modify>\n<node id="{4}" lat="{0}" lon="{1}" changeset="{2}" version="{3}">\n'.format(lat, lon, cid, existingVersion, nid)
	for k in tags:
		xml += '<tag k="{0}" v="{1}"/>\n'.format(saxutils.escape(k), saxutils.escape(tags[k])).encode('utf-8')
	xml += '</node>\n</modify>\n</osmChange>\n'
	if verbose >= 2: print xml
	newVersion = None

	if exe:
		response = urlutil.Post(baseurl+"/0.6/changeset/"+str(cid)+"/upload",xml,userpass)
		if verbose >= 1: print response
		if urlutil.HeaderResponseCode(response[1]) != "HTTP/1.1 200 OK": return (0,"Error modifying node")

		respRoot = ET.fromstring(response[0])
		for obj in respRoot:
			newVersion = obj.attrib['new_version']

	return int(newVersion)

def CreateWay(userpass, cid, baseurl, nodeIds, tags, verbose=0, exe=1):

	xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
	xml += '<osmChange version="0.6" generator="py">\n<create>\n<way id="-1" changeset="{0}">\n'.format(cid)
	for nid in nodeIds:
		xml += '<nd ref="{0}"/>\n'.format(nid)
	for k in tags:
		xml += '<tag k="{0}" v="{1}"/>\n'.format(saxutils.escape(k), saxutils.escape(tags[k])).encode('utf-8')
	xml += '</way>\n</create>\n</osmChange>\n'
	if verbose >= 2: print xml
	newId = None
	newVersion = None

	if exe:
		response = urlutil.Post(baseurl+"/0.6/changeset/"+str(cid)+"/upload",xml,userpass)
		if verbose >= 1: print response
		if urlutil.HeaderResponseCode(response[1]) != "HTTP/1.1 200 OK": return None

		respRoot = ET.fromstring(response[0])
		for obj in respRoot:
			newId = obj.attrib['new_id']
			newVersion = obj.attrib['new_version']

	return int(newId), int(newVersion)

def ModifiedWay(userpass, cid, baseurl, nodeIds, tags, wid, existingVersion, verbose=0, exe=1):

	xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
	xml += '<osmChange version="0.6" generator="py">\n<modify>\n<way id="{0}" changeset="{1}" version="{2}">\n'.format(wid, cid, existingVersion)
	for nid in nodeIds:
		xml += '<nd ref="{0}"/>\n'.format(nid)
	for k in tags:
		xml += '<tag k="{0}" v="{1}"/>\n'.format(saxutils.escape(k), saxutils.escape(tags[k])).encode('utf-8')
	xml += '</way>\n</modify>\n</osmChange>\n'
	if verbose >= 2: print xml
	newId = None
	newVersion = None

	if exe:
		response = urlutil.Post(baseurl+"/0.6/changeset/"+str(cid)+"/upload",xml,userpass)
		if verbose >= 1: print response
		if urlutil.HeaderResponseCode(response[1]) != "HTTP/1.1 200 OK": return None

		respRoot = ET.fromstring(response[0])
		for obj in respRoot:
			newId = obj.attrib['new_id']
			newVersion = obj.attrib['new_version']

	return int(newId), int(newVersion)

def DeleteWay(userpass, cid, baseurl, wid, existingVersion, verbose=0, exe=1):

	xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
	xml += '<osmChange version="0.6" generator="py">\n<delete>\n<way id="{0}" changeset="{1}" version="{2}">\n'.format(wid, cid, existingVersion)
	xml += '</way>\n</delete>\n</osmChange>\n'
	if verbose >= 2: print xml
	newId = None
	newVersion = None

	if exe:
		response = urlutil.Post(baseurl+"/0.6/changeset/"+str(cid)+"/upload",xml,userpass)
		if verbose >= 1: print response
		if urlutil.HeaderResponseCode(response[1]) != "HTTP/1.1 200 OK": return None

	return newId, newVersion

def DeleteRelation(userpass, cid, baseurl, rid, existingVersion, verbose=0, exe=1):

	xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
	xml += '<osmChange version="0.6" generator="py">\n<delete>\n<relation id="{0}" changeset="{1}" version="{2}">\n'.format(rid, cid, existingVersion)
	xml += '</relation>\n</delete>\n</osmChange>\n'
	if verbose >= 2: print xml
	newId = None
	newVersion = None

	if exe:
		response = urlutil.Post(baseurl+"/0.6/changeset/"+str(cid)+"/upload",xml,userpass)
		if verbose >= 1: print response
		if urlutil.HeaderResponseCode(response[1]) != "HTTP/1.1 200 OK": return None

	return newId, newVersion

def DeleteNode(userpass, cid, baseurl, nid, existingVersion, lat, lon, verbose=0, exe=1):

	xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
	xml += '<osmChange version="0.6" generator="py">\n<delete>\n<node id="{0}" changeset="{1}" version="{2}" lat="{3}" lon="{4}">\n'.format(nid, cid, existingVersion, lat, lon)
	xml += '</node>\n</delete>\n</osmChange>\n'
	if verbose >= 2: print xml
	newId = None
	newVersion = None

	if exe:
		response = urlutil.Post(baseurl+"/0.6/changeset/"+str(cid)+"/upload",xml,userpass)
		if verbose >= 1: print response
		if urlutil.HeaderResponseCode(response[1]) != "HTTP/1.1 200 OK": return None

	return newId, newVersion

def DeleteNodes(userpass, cid, baseurl, nidLi, existingVersionLi, latLi, lonLi, verbose=0, exe=1):

	xml = "<?xml version='1.0' encoding='UTF-8'?>\n"
	xml += '<osmChange version="0.6" generator="py">\n<delete>\n'
	for nid, existingVersion, lat, lon in zip(nidLi, existingVersionLi, latLi, lonLi):
		xml += '<node id="{0}" changeset="{1}" version="{2}" lat="{3}" lon="{4}">\n'.format(nid, cid, existingVersion, lat, lon)
		xml += '</node>\n'
	xml += '</delete>\n</osmChange>\n'
	if verbose >= 2: print xml
	newId = None
	newVersion = None

	if exe:
		response = urlutil.Post(baseurl+"/0.6/changeset/"+str(cid)+"/upload",xml,userpass)
		if verbose >= 1: print response
		if urlutil.HeaderResponseCode(response[1]) != "HTTP/1.1 200 OK": return None

	return newId, newVersion

if __name__=="__main__":

	#url = "http://api.openstreetmap.org/api"
	url = "http://fosm.org/api"
	#url = "http://kinatomic/m/microcosm.php"
	username = "mapping@sheerman-chase.org.uk" #raw_input("Username:")
	password = raw_input("Password:")
	userpass = username+":"+password

	cid, status = CreateChangeSet(userpass, {'comment':"Api Tests"}, url)
	print "Created changeset", cid
	assert cid > 0

	ret = CreateNode(userpass, cid, url, 51.0, -1.0, {}, 2)
	print ret
	assert ret is not None
	ndId, nvVer = ret

	ret = CreateNode(userpass, cid, url, 51.0, -1.00001, {}, 2)
	print ret
	assert ret is not None
	ndId2, nvVer2 = ret

	wayRet = CreateWay(userpass, cid, url, [ndId, ndId2], {'testk':'val1'})
	print wayRet

	wayRet2 = ModifiedWay(userpass, cid, url, [ndId, ndId2], {'testk':'val2'}, wayRet[0], wayRet[1])
	print wayRet2

	CloseChangeSet(userpass, cid, url)
	print "Closed changeset", cid

