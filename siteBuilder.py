import os, re, markdown, configparser, codecs
import xml.etree.ElementTree as elementTree

settings = configparser.ConfigParser()
settings.read("settings.cfg")
settings = settings['DEFAULT']

rawPath = settings['rawPath']
outPath = settings['outPath']
templatesPath = settings['templatesPath']

#parse single entry, add things like images
def parseEntry(currentEntry, entries):
	if (currentEntry['parsed']):
		return currentEntry

	currentEntry['content'] = markdown.markdown(currentEntry['content'])

	#allposts
	allposts_full = ""
	allposts_link = ""
	for entry in entries:
		if (entry['type'] == "post"):
			entryStr = addArgs({
				"title": entry['title'],
				"link": getLink(entry)
			}, template("link"))

			entryStr = addArgs({
				"content": entryStr
			}, template("listEntry"))

			allposts_link += entryStr

	allposts_link = addArgs({
		"content": allposts_link
	}, template("list"))
			

	#apply to currentEntry
	currentEntry['content'] = addArgs({
		"allposts-full": allposts_full,
		"allposts-link": allposts_link
	}, currentEntry['content'])

	currentEntry['parsed'] = True
	return currentEntry

def template(path):
	hFile = open(templatesPath+path+".html", "r")
	str = hFile.read()
	hFile.close()
	return str

def addArgs(args, str):
	for key, val in args.items():
		str = str.replace("{"+key+"}", val)
	return str

def etree_to_dict(tree):
	root = tree.getroot()
	d = {}
	for child in root:
		d[child.tag] = child.text
	d["parsed"] = False
	return d

def getLink(entry):
	if (settings['mod_rewrite'] == "true"):
		return entry['slug']
	else:
		return entry['slug']+".html"

#parse template, returns the completed html file
def makeFile(currentEntry, entries):
	currentEntry = parseEntry(currentEntry, entries)
	
	#buttons
	buttonStr = ""
	for entry in entries:
		if (entry['type'] == "page"):
			if (entry['slug'] == currentEntry['slug']): classMod = " current"
			else: classMod = ""
			buttonStr += addArgs({
				"link": getLink(currentEntry),
				"title": entry['title'],
				"current": classMod
			}, template("button"))
			
	#menu
	menuStr = addArgs({
		"buttons": buttonStr,
		"siteHeader": settings['siteHeader']
	}, template("menu"))

	#content
	contentStr = addArgs({
		"post": currentEntry['content'],
		"title": addArgs({
			"link": getLink(currentEntry),
			"title": currentEntry['title']
		}, template("link"))
	}, template("post"))
	
	#title
	titleStr = addArgs({
		"entryTitle": currentEntry['title'],
		"siteHeader": settings['siteHeader']
	}, template("title"))

	#now put it all together
	indexStr = addArgs({
		"menu": menuStr,
		"title": titleStr,
		"content": contentStr
	}, template("index"))

	#write results to file
	fileName = currentEntry['fileName']
	fileName = fileName.replace(".xml", ".html")

	hFile = open(outPath+fileName, "w")
	hFile.write(indexStr)
	hFile.close

	#write rule to htaccess
	if (settings['mod_rewrite'] == "true"):
		with open(outPath+".htaccess", "a") as htaccess:
			htaccess.write("RewriteRule ^"+currentEntry['slug']+" "+fileName+"\r\n")
			htaccess.close()

def main():
	if (settings['mod_rewrite'] == "true"):
		with open(outPath+".htaccess", "w") as htaccess:
			htaccess.write("Options FollowSymLinks\r\n")
			htaccess.write("RewriteEngine On\r\n")
			htaccess.close()

	entries = os.listdir(rawPath)

	entriesSort = []
	for entryFileName in entries:
		print("doing "+entryFileName)
		hEntry = codecs.open(rawPath+entryFileName, "r", encoding="utf-8")
		entry = etree_to_dict(elementTree.parse(hEntry))
		hEntry.close()
		entry['fileName'] = entryFileName

		entriesSort.insert(int(entry['sort']), entry)

	for entry in entriesSort:
		makeFile(entry, entriesSort)
		if (entry['slug'] == settings['defaultPage']):
			entry['fileName'] = "index.html"
			makeFile(entry, entriesSort) 

	#theme
	themeFiles = os.listdir(settings['themesPath']+settings['theme'])
	hStyleFile = open(settings['outPath']+"style.css", "w")
	for themeFile in themeFiles:
		hStyleFile.write(open(settings['themesPath']+settings['theme']+"/"+themeFile, "r").read())
	hStyleFile.close()
main()
