#!/usr/bin/env
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

BASE_URL = 'http://www.booksamillion.com'
MAIN_URL_1 = 'http://www.booksamillion.com/search?filter=book_categories%3AFIC%7Cproduct_type%3Abooks%7Cbook_categories%3AFIC-028%7Cbook_categories%3AFIC-028-030%7Cformat%3APaperback&sort=date'
MAIN_URL_2 = 'http://www.booksamillion.com/search?filter=book_categories%3AFIC%7Cproduct_type%3Abooks%7Cbook_categories%3AFIC-009%7Cbook_categories%3AFIC-009-070%7Cformat%3APaperback&sort=date'
MAIN_URL_3 = 'http://www.booksamillion.com/search?filter=book_categories%3AFIC%7Cproduct_type%3Abooks%7Cformat%3APaperback%7Cbook_categories%3AFIC-031%7Cbook_categories%3AFIC-031-080&sort=date'

def grab_urls(URL, category, num_pages):
	browser = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
	#Handling first page separately
	browser.get(URL)
	soup = BeautifulSoup(browser.page_source, 'lxml')
	books = soup.find_all(class_="title")

	url_file = open("books_millions", "a+")
	category_file = open("categories_millions", "a+")
	for book in books:
		url_file.write(book.find('a', href=True)['href'])
		url_file.write('\n')
		category_file.write(category)
		category_file.write('\n')

	for i in range(0, num_pages):
		page_list = soup.find_all(class_="page-list top")
		pages = page_list[0].find_all('a', href=True)
		for j in range(0, len(pages)):
			if(pages[j]['href'] == '#'):
				break;
			#print(pages[j]['href'], type(pages[j]))

		browser.get(BASE_URL + pages[j+1]['href'])
		soup = BeautifulSoup(browser.page_source, 'lxml')
		books = soup.find_all(class_='title')
		for book in books:
			url_file.write(book.find('a', href=True)['href'])
			url_file.write('\n')
			category_file.write(category)
                	category_file.write('\n')
	url_file.close()
	category_file.close()

grab_urls(MAIN_URL_1, 'Science Fiction - Space Opera', 200)
grab_urls(MAIN_URL_2, 'Fantasy - Dark Fantasy', 190)
grab_urls(MAIN_URL_3, 'Thrillers - Psychological', 80)		
