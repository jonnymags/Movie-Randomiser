# A programme that returns a random film title, plot, and rating, and then if the 
# film is a good choice, returns the URL of the projectfreetv location or the 
# torrent location.

from bs4 import BeautifulSoup
import requests
import random
import time
import csv

def main():

	print "Welcome to the Movie Randomiser 1.0"
	scrape_choice = raw_input("Should I scrape the site for new listings? (Y/N): ").lower()
	again = 'y'

	while again == 'y':
		if scrape_choice == 'y':
			print "Ok, scraping..."
			movie_scraper()
			movie_checker()
			again = raw_input("How's this one? Do you want another one? (Y/N): ").lower()
		else:
			print "I'll just pick something from the current list..."
			movie_checker()
			again = raw_input("How's this one? Do you want another one? (Y/N): ").lower()



def movie_scraper():

	for i in range(1, 6):
		base_url = 'http://instantwatcher.com/genres/485/{}'.format(i)
		print base_url
		r = requests.get(base_url)
		soup = BeautifulSoup(r.text)
		movie_list = []
		with open('films.csv', 'a') as f:
			for line in soup.find(id='titles').find_all(class_='title-list-item '):
				name = line.find('a').get_text()
				movies = {'Title: ': name}
				movie_list.append(movies)
			fields = movie_list[0].keys()
			dfile = csv.DictWriter(f, fieldnames=fields, delimiter='|')
			dfile.writerows(movie_list)
		time.sleep(1)



def movie_checker():

	film_list = []
	with open('films.csv') as f:
		read_file = csv.reader(f)
		for row in read_file:
			film_list.append(''.join(row))

	random_film = random.choice(film_list)
	url_params = {'t': random_film}
	r = requests.get('http://www.omdbapi.com/?', params=url_params)
	movie_selection = r.json()
	print 'Title: ', movie_selection['Title']
	print 'Plot: ', movie_selection['Plot']
	print 'Rating: ', movie_selection['imdbRating']
	


main()










