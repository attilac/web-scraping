import requests
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
import re
import os
import json
import mimetypes

baseUrl = 'http://www.koket.se'
basePath = ''

def connect(url):
	'''Skrapa en sida från url'''
	r = requests.get(url)
	if r.status_code == 200:
		return r.content
	else:
		return False	

def makeSoup(html):
	''' '''
	return BeautifulSoup(html, 'lxml')

def urlify(s):
	s = s.strip()
	s = s.replace('/', '')
	s = re.sub('\s+', '-', s)
	return s.lower()

def numberify(num):
	temp = ''
	for n in list(num): 
		#print(p + '\n')
		if n.isdigit():
			temp += n
	return int(temp)				

def writeImgFile(url, destPath, destName):
	''' Hämtar bild som data och sparar den till disk'''
	r = requests.get(url)
	contentType = r.headers['content-type']
	if r.status_code == 200:
		if r.headers['Content-Type'] == 'image/jpeg':
			print(r.headers['Content-Type'])
			#extension = mimetypes.guess_all_extensions(contentType)[2]
			with open(destPath + destName, 'wb') as imgfile: 
				imgfile.write(r.content)	
				imgfile.close()	

def setFileName(url):
	''' Returnerar filnamnet från en url'''
	return url.split('/')[-1].split('#')[0].split('?')[0]	

def continueProg(question):
    '''Frågar om användaren vill fortsätta.
    Returnerar sant eller falskt
    '''
    while True:
        choice = input('\n%s [y/n]?\n' % question)
        try:
            if choice == 'y':
                return True
            elif choice == 'n':
                return False
            else:
                raise ValueError()
            break
        except ValueError:
            print('Vänligen svara med \'y\' or \'n\'.')
        continue	
			
#Setup
print('\nProgram för att hämta bilder från en webbsida\n\n')
folderPath = '/Users/attilacederbygd/code/pylab/movie-database/images/'

#jsonFile = 'top-rated-movies-02.json'
#jsonFile = 'top-rated-inidan-movies-01.json'
#jsonFile = 'movies-in-theaters.json'
jsonFile = 'movies-coming-soon.json'
# jsonFile = 'db.json'

count = 0
with open(jsonFile) as dataFile:    
	jsonObject = json.load(dataFile)

for image in jsonObject:
	#print(str(image['posterurl']))
	imgSrc = image['posterurl']
	#imgName = urlify(image['title'] + '-poster')
	imgName = image['poster']
	#print(setFileName(imgSrc))
	try:
		writeImgFile(imgSrc, folderPath, imgName)	
	except:
		pass

'''
	count += 1
	if count == 30:
		if not continueProg('Fortsätta'):
			break
		else:	
			print('Ok!')
			count = 0
'''