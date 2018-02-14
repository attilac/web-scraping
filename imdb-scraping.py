import requests
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
import re
import os
import json
import random
from urllib.parse import urlparse
import datetime

baseUrl = 'http://www.imdb.com'
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

def removeBreaks(tag):
	breaks = tag.find_all('br')
	for f in breaks:
		f.extract()			

def cleanHtml(tag):
	tags = tag.find_all(['a', 'p', 'h2', 'h3', 'h1', 'span', 'div'])
	for t in tags:
		#print(t.name)
		if t.name == 'div':
			t.unwrap()
		del t['class']
		del t['style']	
		del t['id']
	del tag['class']
	del tag['id']
	del tag['style']

def stripEmptyParagraphs(tag):
	paragraphs = tag.find_all('p')
	for p in paragraphs:
		if p.get_text().isspace():
			p.extract()
		elif len(p.get_text()) == 0:
			p.extract()		

def getImageList(path):
	imageList = []
	try:
		for filename in os.listdir(targetPath):
				imageList.append(filename)
	except FileNotFoundError as err:
		print('FileNotFoundError error: {0}'.format(err))
	return imageList

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
print('\nProgram för att skrapa webbsida\n\n')
# url to listing site
# 1 url = 'http://www.imdb.com/chart/top?ref_=nv_mv_250_6';
# 2 url = 'http://www.imdb.com/chart/top-indian-movies?ref_=nv_mv_250_in_7';
# 3 url = 'http://www.imdb.com/movies-in-theaters/?ref_=cs_inth'
# 4 url = 'http://www.imdb.com/movies-coming-soon/?ref_=inth_cs'
url = 'http://www.imdb.com/movies-coming-soon/2018-05/'
data = []
# 1 outFileName = 'top-rated-movies-01.json'
# 2 outFileName = 'top-rated-inidan-movies-01.json'
# 3 outFileName = 'movies-in-theaters.json'
# 4 outFileName = 'movies-coming-soon.json'
outFileName = 'movies-coming-soon-02.json'
# outFileName = 'db.json'
count = 0

#url = str(input('Ange url: '))
navSoup = makeSoup(connect(url))	

pageTitle = navSoup.title.string
pageTitleTrunc = (pageTitle[:30]) if len(pageTitle) > 30 else pageTitle
print('Sidtitel: ')
print(pageTitle)	

# Follow links to detail pages
# top-rated-movies has different structure
# movieLinks = navSoup.select('.titleColumn > a')

movieLinks = navSoup.find_all('h4', itemprop='name')
#print(movieLinks)
for index, link in enumerate(movieLinks, 86):
	print('movie ' + str(index))
	# print(link)
	a = link.find('a')
	movieUrl = baseUrl + a.get('href')
	# print(movieUrl)
	soup = makeSoup(connect(movieUrl))	

	pageTitle = soup.title.string
	print('Sidtitel: ')
	print(pageTitle)

	# Movie title
	getMovieTitle = soup.find_all(itemprop='name')
	movieTitle = '' if getMovieTitle is None else getMovieTitle[0].contents[0].strip('\u00a0')
	print(movieTitle)

	# Movie year
	getTitleYear = soup.select('#titleYear > a')
	titleYear = '' if getTitleYear is None else getTitleYear[0].text
	print(titleYear)

	# Content rating
	getContentRating = soup.find('div', class_='subtext')
	contentRating = '' if getContentRating is None else getContentRating.contents[2].strip(' \t\n\r\,')
	print(contentRating)

	# Duration
	getDuration = soup.find('time', itemprop='duration')
	duration = '' if getDuration is None else soup.find('time', itemprop='duration')['datetime']
	print(duration)	

	# Original title
	getOriginalTitle = soup.find('div', class_='originalTitle')
	originalTitle = '' if getOriginalTitle is None else getOriginalTitle.contents[0]
	print(originalTitle)

	# Date published
	getDatePublished = soup.find('meta', itemprop='datePublished')
	datePublished = '' if getDatePublished is None else getDatePublished['content']
	print(datePublished)

	# Genres
	getGenres = soup.find_all('span', itemprop='genre')
	genres = []
	for genre in getGenres:
	    #print(genre.text)
	    genres.append(genre.text)
	print(genres)

	# Poster image
	getPoster = soup.find('div', class_='poster')
	posterUrl = '' if getPoster is None else baseUrl + getPoster.find('a').get('href')
	if posterUrl != '':
		posterUrlParse = urlparse(posterUrl)
		posterUrlFormat = posterUrlParse.scheme + "://" + posterUrlParse.netloc + posterUrlParse.path
		# print(posterUrlFormat)

		posterGallerySoup = makeSoup(connect(posterUrlFormat))	
		posterLgUrl = posterGallerySoup.find_all('meta', itemprop='image')[0]['content']
		# print(posterLgUrl)

		poster = setFileName(posterLgUrl)
		#poster = urlify(movieTitle) + '-poster.jpg'
		# print(poster)
	else: 
		poster = ''
		posterLgUrl = ''

	# Description
	getStoryline = soup.find('div', id='titleStoryLine')
	storylineElement = '' if getStoryline is None else getStoryline.find('div', itemprop='description')
	storyline = '' if storylineElement is None else storylineElement.text.strip(' \t\n\r')
	print(storyline)

	# Actors
	getActors = soup.find_all('span', itemprop="actors")
	actors = []
	for actor in getActors:
	    #print(actor.text)
	    actorFormat = actor.text.strip(' \t\n\r\,')
	    actors.append(actorFormat)
	print(actors)

	# IMDb rating
	getRating = soup.find('span', itemprop='ratingValue')
	rating = '' if getRating is None else float(getRating.text)
	print(rating)

	#ratings = random.sample(range(1, 11), 10)
	ratings = [random.randint(1,10) for _ in range(30)]
	print(ratings)

	movieID = str(index)
	# The structure of the JSON array
	item = {'id': movieID, 'title': movieTitle, 'year': titleYear, 'genres': genres, 'ratings': ratings, 'poster': poster, 'contentRating': contentRating, 'duration': duration, 'releaseDate': datePublished, 'averageRating': 0, 'originalTitle': originalTitle, 'storyline': storyline, 'actors': actors, 'imdbRating': rating, 'posterurl': posterLgUrl}
	data.append(item)

	count += 1
	if count == 100:
		if not continueProg('Fortsätta'):
			break
		else:	
			print('Ok!')
			count = 0

jsonData=json.dumps(data, sort_keys=False, indent=4)
print(jsonData)


with open(outFileName, 'w') as outfile:
    json.dump(data, outfile, sort_keys=False, indent=4)




