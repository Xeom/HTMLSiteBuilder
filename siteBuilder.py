import os, re, json, markdown

settings = json.load(open("settings.json", "r"))

rawPath = settings['rawPath']
outPath = settings['outPath']
templatesPath = settings['templatesPath']

#parse single entry, add things like images
def parseEntry(currentEntry, entries):
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

#parse template, returns the completed html file
def makeFile(currentEntry, entries):
	currentEntry = parseEntry(currentEntry, entries)
	
	#buttons
	buttonStr = ""
	buttonTemplate = template("button")
	for entry in entries:
		if (entry['type'] == "page"):
			if (entry['slug'] == currentEntry['slug']): classMod = " current"
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
	fileName = fileName.replace("json", "html")
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
		entry = json.load(hEntry)
		hEntry.close()
		entry['fileName'] = entryFileName

		entriesSort.insert(entry['sort'], entry)

	for entry in entriesSort:
		makeFile(entry, entriesSort)
		if (entry['slug'] == settings['defaultPage']):
			entry['fileName'] = "index.html"
			makeFile(entry, entriesSort) 
main()
