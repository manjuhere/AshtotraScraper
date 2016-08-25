"""
Removes extra lines and english content in indic content file
ignore itrans and iast folders as it has main content in english
"""
import re
import string

languageDict = {
	'sanskrit' : "sa",
	'bengali' : "bn",
	'gujarati' : "gu",
	'punjabi' : "pa",
	'kannada' : "kn",
	'malayalam' : "ml",
	'odia' : "or",
	'tamil' : "ta",
	'telugu' : "te",
	'hindi' : "hi"
}
pattern = r"[a-zA-Z]+"
prog = re.compile(pattern)
files = 0

for lang in languageDict.keys():
	print "processing "+lang+" folder"
	#open the ashtotra list file in each directory to get file list
	ashList = lang+"/"+lang+" ashtotra list.txt"
	ashtotras = []
	try:
		with open(ashList, 'r') as fileObj:
			lines = fileObj.readlines()
			for line in lines:
				path = line[:line.index(" : ")]
				path = path.replace(':', '.')
				ashtotras.append(path)
	except IOError:
		print "\n\n\t\t!!! File :"+ ashList +" Does Not Exist !!!"
		print "\n\n\t\t!!! EXECUTE dump.py initially to create required files!!!\n\n"
		exit()	

	#open each file in directory and perform our operation
	for i, ashtotra in enumerate(ashtotras):
		newData = ""
		filename = "./"+lang+"/"+ashtotra+".txt"
		try:
			with open(filename, 'r') as fileObj:
				lines = fileObj.readlines()
				for line in lines:
					match = re.search(pattern, line)
					if match:
						continue
					elif line == '\n':
						continue
					else:
						newData += line
			#open the same file in write mode and write processed data
			with open(filename, 'w') as fileObj:
				fileObj.write(newData)
		except IOError:
			print "\n\n\t\t!!! File :"+ filename +" Does Not Exist !!!"
			print "\n\n\t\t!!! EXECUTE dump.py initially to create required files!!!\n\n"
			exit()	
		
		files = i
	print str(files+1)+" file processed in "+lang+" folder"