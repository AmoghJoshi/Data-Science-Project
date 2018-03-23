#!/usr/bin/env
from bs4 import BeautifulSoup
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

BASE_URL = 'https://www.amazon.com'
MAIN_URL_1 = 'https://www.amazon.com/s/ref=sr_st_date-desc-rank?fst=as%3Aoff&rh=n%3A283155%2Cn%3A!1000%2Cn%3A25%2Cn%3A16272%2Cn%3A271585011%2Cp_n_condition-type%3A1294423011%2Cp_n_feature_browse-bin%3A2656022011&qid=1521345320&bbn=271585011&sort=date-desc-rank'
MAIN_URL_2 = 'https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A25%2Cn%3A16190%2Cn%3A9803%2Cp_n_feature_browse-bin%3A2656022011&page=2&bbn=9803&sort=date-desc-rank&ie=UTF8&qid=1521705605'
MAIN_URL_3 = 'https://www.amazon.com/s/ref=sr_nr_p_n_feature_browse-b_0?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A18%2Cn%3A10484%2Cn%3A10491%2Cp_n_feature_browse-bin%3A2656022011&bbn=10491&sort=date-desc-rank&ie=UTF8&qid=1521707566&rnid=618072011'

num_categories = 0
num_authors = 0

def clean_string(attribute):
	if(attribute):
		attribute = attribute.encode('ascii', 'ignore').strip()
		attribute = attribute.replace(',', '#')
	return attribute

def handle_authors(soup, author_file):
	global num_authors

	#Handling authors
        by_tags = soup.find_all(class_='a-size-small a-color-secondary')
        #print(type(by_tags), len(by_tags))
	author = ''
        for by_tag in by_tags:
		author = ''
		#If this tag does not contain any text, not valid
		if(not by_tag.get_text()):
			continue

		#If it does not contain by, it is not valid
		if(not 'by' in by_tag.get_text()):
			continue

		#If it contains by, it should exactly be by, otherwise invalid
		try: 
                	if('by' != clean_string(by_tag.get_text())):
                        	continue
		except:
			continue

		try:
         		author_tag = by_tag.findNext(class_='a-size-small a-color-secondary')
			author += clean_string(author_tag.get_text())
			if('and' in author_tag.get_text()):
				author += ' '
				author_sibling_tag = author_tag.findNext(class_='a-size-small a-color-secondary')
				author += clean_string(author_sibling_tag.get_text())
		except:
			print('Exception while processing author string')
			author = 'NA'
			#traceback.print_exc()

		#Special handling for this case
		#if('FREE' in author):
		#	continue
		
		if('FREE' in author):
			author = author.split('FREE')[0]
			if(author):
				author = clean_string(author)

		if('Get it' in author):
                        author = author.split('Get it')[0]
                        if(author):
                                author = clean_string(author)

		print (author)				
                author_file.write(author)
                author_file.write("\n")
		author_file.flush()
		num_authors += 1

def grab_urls(URL, category, num_pages):
	global num_categories

	browser = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')

	#Handling first page separately
	browser.get(URL)
	soup = BeautifulSoup(browser.page_source, 'lxml')
	books = soup.find_all(id='s-results-list-atf')	
	book_links = books[0].find_all('a', href=True)

	url_file = open("books_amazon", "a+")
	author_file = open("authors_categories_amazon", "a+")
	for book_link in book_links:
		if('s-access-detail-page' in book_link['class']):
			url_file.write(book_link['href'])
			url_file.write('\n')
			url_file.flush()
			author_file.write(category)
                	author_file.write('\n')
			author_file.flush()
			num_categories += 1

	handle_authors(soup, author_file)
	
	next_url = ''
	author_file = open("authors_categories_amazon", "a+")
	for i in range(0, num_pages):
		bottom_bar = soup.find_all(id = 'pagn')
		siblings = list(bottom_bar[0].children)
		currFound = 0
		for j in range(0, len(siblings)):
			#print (type(siblings[j]))
			if(not 'Tag' in str(type(siblings[j]))):
				continue;
			if('pagnCur' in str(siblings[j])):
				currFound = 1
				continue
			if(currFound == 1 and 'pagnLink' in str(siblings[j])):
				next_url = BASE_URL + siblings[j].find('a', href=True)['href']
				break
 

		browser.get(next_url)
		soup = BeautifulSoup(browser.page_source, 'lxml')
		books = soup.find_all(id='s-results-list-atf')
		book_links = books[0].find_all('a', href=True)
		for book_link in book_links:
			if('s-access-detail-page' in book_link['class']):
				url_file.write(book_link['href'])
				url_file.write('\n')
				author_file.write(category)
                		author_file.write('\n')
				num_categories += 1

		handle_authors(soup, author_file)

	url_file.close()
	author_file.close()
	print('Number of authors written is %d' %(num_authors))
	print('Number of categories written is %d' %(num_categories))

grab_urls(MAIN_URL_1, 'Science Fiction : Space Opera', 95)
grab_urls(MAIN_URL_2, 'Fantasy : Dark', 95)
grab_urls(MAIN_URL_3, 'Psychological Thrillers', 95)		
