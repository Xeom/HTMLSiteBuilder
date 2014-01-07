import os, re, json, markdown

rawPath = "raw/"
outPath = "out/"

#parse single entry, add things like images
def parseEntry(entry):
	return entry

#parse template, returns the completed html file
def parseTemplate(str, entry):
	return str

def main():
	entries = os.listdir(rawPath)

	entriesArr = []
	for entry in entries:
		hEntry = open(rawPath+entry, "r")
		entry = json.load(hEntry)
		hEntry.close()

		entry = parseEntry(entry)

		entriesArr.insert(entry.sort, entry)

	for entry in entriesArr:
		print(entry)
main()
