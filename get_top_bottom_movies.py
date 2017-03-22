#!/usr/bin/env python
# Zihan Ye
# 2017.03.17
# This script scrape user reviews from top250 movies in IMDB

import sys
from bs4 import BeautifulSoup
import requests
import io

# Import the IMDbPY package.
try:
    import imdb
except ImportError:
    print 'You bad boy!  You need to install the IMDbPY package!'
    sys.exit(1)


if len(sys.argv) != 1:
    print 'No arguments are required.'
    sys.exit(2)

i = imdb.IMDb()

filename = "test.txt"

target = io.open(filename, 'w', encoding='utf8')
top250 = i.get_top250_movies()
bottom100 = i.get_bottom100_movies()

out_encoding = sys.stdout.encoding or sys.getdefaultencoding()

for label, ml in [('top 10', top250[:1]), ('bottom 10', bottom100[:0])]:
    print ''
    print '%s movies' % label
    for movie in ml:
	url = i.get_imdbURL(movie)+ 'reviews?start='
	for index in range(0,91,10):#change page
		urlpage = url + str(index)
		r = requests.get(urlpage)
		bs = BeautifulSoup(r.text, "lxml")
		div = bs.find(id="tn15content")
		for p in div.find_all('p'):
			target.write(p.get_text())
			#print(count)
			#print(p.get_text())

target.close()

