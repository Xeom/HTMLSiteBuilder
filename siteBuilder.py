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

#parse template, returns the completed html file
def makeFile(currentEntry, entries):
	currentEntry = parseEntry(currentEntry, entries)

	#make menu
	
	#buttons:
	buttons = ""
	for entry in entries:
		if (entry['type'] == "page"):
			buttonStr = open(templatesPath+"button.html", "r").read()
			buttonStr = buttonStr.replace("{link}", entry['slug'])
			buttonStr = buttonStr.replace("{title}", entry['title'])
			if (entry['slug'] == currentEntry['slug']):
				buttonStr = buttonStr.replace("{current}", " current")
			else:
				buttonStr = buttonStr.replace("{current}", "")
			buttons += buttonStr
	#buttons made, now for the rest of the menu
	menuStr = open(templatesPath+"menu.html", "r").read()
	menuStr = menuStr.replace("{buttons}", buttons)
	menuStr = menuStr.replace("{siteHeader}", settings['siteHeader'])

	#menu made, now time for content
	contentStr = currentEntry['content']
	
	#content made, now title
	titleStr = open(templatesPath+"title.html", "r").read()
	titleStr = titleStr.replace("{entryTitle}", currentEntry['title'])
	titleStr = titleStr.replace("{siteHeader}", settings['siteHeader'])

	#title made, now put it all together
	indexStr = open(templatesPath+"index.html", "r").read()
	indexStr = indexStr.replace("{menu}", menuStr)
	indexStr = indexStr.replace("{title}", titleStr)
	indexStr = indexStr.replace("{content}", contentStr)

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
