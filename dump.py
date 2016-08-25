import os
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver

languageDict = {
	'sanskrit' : "sa",
	'iast' : "iast",
	'bengali' : "bn",
	'gujarati' : "gu",
	'punjabi' : "pa",
	'kannada' : "kn",
	'malayalam' : "ml",
	'odia' : "or",
	'tamil' : "ta",
	'telugu' : "te",
	'hindi' : "hi",
	'itrans' : "en-IN"
}
ashTotraDict = {}	#dict with name as name of ashtotra and value as corresponding URL

for i in languageDict.keys():
	os.system("mkdir "+ i)

link = "http://sanskritdocuments.org/itrans/by-category/ashtottarashatanamavali.php"
page = urllib2.urlopen(link)	#open URL
soup = BeautifulSoup(page, "html.parser") #parse the link with html parser
div = soup.find("div", class_='index-content')	#get to div that has to be scraped
li = div.findAll("li")	#all elements reside in <li> tags
for i in li:
	#get name and URL from each li item and make a key value pair
	name = i.contents[3].find("em").string
	url = "http://sanskritdocuments.org/"+i.contents[3].get("href")[1:]
	ashTotraDict[name] = url

#link to page
for lang in languageDict.keys():
	print ("Getting "+ lang +" Files")
	#open a file and store all obtained data in a readable format
	filename = lang + " ashtotra list.txt"
	with open(filename, 'w') as fileObj:
		for i, key in enumerate(ashTotraDict.keys()):
			line = str(i+1) + ": " + key + " : " + ashTotraDict[key] + "\n"
			fileObj.write (line.encode('utf-8'))

	for i, key in enumerate(ashTotraDict.keys()):
		link = ashTotraDict[key][:ashTotraDict[key].index("=")+1]+languageDict[lang]
		#using phantomJS as it avoids opening and closing browser
		browser = webdriver.PhantomJS() 
		#optionally you can use chromedriver as follows -
		#browser = webdriver.Chrome('./chromedriver')
		browser.get(link)	#opens page after rendered by js
		soup = BeautifulSoup(browser.page_source, "html.parser") #parse html parser
		browser.quit()
		try:
			stotra = soup.find("pre", class_='stotra').contents[0]
		except AttributeError: #one of the ashtotras in page has a different class
			stotra = soup.find("pre", class_='namavali').contents[0]
		ashTotrafile = lang+"/"+ str(i+1) +". "+key+".txt" #frame a filepath
		with open(ashTotrafile, 'w') as fileObj:
			fileObj.write(stotra.encode('utf-8'))	#write to file
			print ("   file : ", key, " - written successfully to disk")
	print (lang + "Files Obtained")
