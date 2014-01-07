import os, re, json, markdown

rawPath = "raw/"
outPath = "out/"
templatesPath = "templates/"

settings = {
	'siteHeader': "Mort's Ramblings"
}

#parse single entry, add things like images
def parseEntry(currentEntry, entries):
	return currentEntry

def addArgs(args, str):
	for arg in args:
		str = str.replace("{"+arg[0]+"}", arg[1])
	return str

#parse template, returns the completed html file
def makeFile(currentEntry, entries):
	currentEntry = parseEntry(currentEntry, entries)
	
	#buttons
	buttonStr = ""
	buttonTemplate = open(templatesPath+"button.html", "r").read()
	for entry in entries:
		if (entry['type'] == "page"):
			if (entry['slug'] == currentEntry['slug']): classMod = " current"
			else: classMod = ""
			buttonStr += addArgs([
				["link", entry['slug']],
				["title", entry['title']],
				["current", classMod]
			], buttonTemplate)
			
	#rest of the menu
	menuStr = addArgs([
		["buttons", buttonStr],
		["siteHeader", settings['siteHeader']]
	], open(templatesPath+"menu.html", "r").read())

	#content
	contentStr = currentEntry['content']
	
	#title
	titleStr = addArgs([
		["entryTitle", currentEntry['title']],
		["siteHeader", settings['siteHeader']]
	], open(templatesPath+"title.html", "r").read())

	#title made, now put it all together
	indexStr = addArgs([
		["menu", menuStr],
		["title", titleStr],
		["content", contentStr]
	], open(templatesPath+"index.html", "r").read())

	#write results to file
	fileName = outPath+currentEntry['fileName']
	fileName = fileName.replace("json", "html")
	hFile = open(fileName, "w")
	hFile.write(indexStr)
	hFile.close

def main():
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
main()
