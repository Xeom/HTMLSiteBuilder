import os, re, markdown, configparser
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
			allposts_link += addArgs([
				["title", entry['title']],
				["link", entry['slug']]
			], template("link"))

	#apply to currentEntry
	currentEntry['content'] = addArgs([
		["allposts-full", allposts_full],
		["allposts-link", allposts_link]
	], currentEntry['content'])

	currentEntry['parsed'] = True
	return currentEntry

def template(path):
	hFile = open(templatesPath+path+".html", "r")
	str = hFile.read()
	hFile.close()
	return str

def addArgs(args, str):
	for arg in args:
		str = str.replace("{"+arg[0]+"}", arg[1])
	return str

def etree_to_dict(tree):
	root = tree.getroot()
	d = {}
	for child in root:
		d[child.tag] = child.text
	d["parsed"] = False
	return d

#parse template, returns the completed html file
def makeFile(currentEntry, entries):
	currentEntry = parseEntry(currentEntry, entries)
	
	#buttons
	buttonStr = ""
	buttonTemplate = template("button")
	for entry in entries:
		if (entry['type'] == "page"):
			if (entry['slug'] == currentEntry['slug']):
				classMod = " current"
			else: classMod = ""
			buttonStr += addArgs([
				["link", entry['slug']],
				["title", entry['title']],
				["current", classMod]
			], buttonTemplate)
			
	#menu
	menuStr = addArgs([
		["buttons", buttonStr],
		["siteHeader", settings['siteHeader']]
	], template("menu"))

	#content
	contentStr = addArgs([
		["post", currentEntry['content']],
		["title", currentEntry['title']]
	], template("post"))
	
	#title
	titleStr = addArgs([
		["entryTitle", currentEntry['title']],
		["siteHeader", settings['siteHeader']]
	], template("title"))

	#now put it all together
	indexStr = addArgs([
		["menu", menuStr],
		["title", titleStr],
		["content", contentStr]
	], template("index"))

	#write results to file
	fileName = currentEntry['fileName']
	fileName = fileName.replace(".xml", ".html")

	print(fileName)

	hFile = open(outPath+fileName, "w")
	hFile.write(indexStr)
	hFile.close

	#write rule to htaccess
	with open(outPath+".htaccess", "a") as htaccess:
		htaccess.write("RewriteRule ^"+currentEntry['slug']+" "+fileName+"\r\n")
		htaccess.close()

def main():
	with open(outPath+".htaccess", "w") as htaccess:
		htaccess.write("Options FollowSymLinks\r\n")
		htaccess.write("RewriteEngine On\r\n")
		htaccess.close()

	entries = os.listdir(rawPath)

	entriesSort = []
	for entryFileName in entries:
		hEntry = open(rawPath+entryFileName, "r")
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
