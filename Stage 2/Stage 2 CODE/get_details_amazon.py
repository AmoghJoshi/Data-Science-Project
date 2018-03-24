#!/usr/bin/env
from bs4 import BeautifulSoup
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint

NAME = 'Name'
CATEGORY = 'Category'
AUTHOR = 'Author'
PRICE = 'Price'
SERIES = 'Series'
PAGES = 'Pages'
PUBLISHER = 'Publisher'
DATE = 'Date'
LANGUAGE = 'Language'
ISBN_10 = 'ISBN-10'
ISBN_13 = 'ISBN-13'
DIMENSIONS = 'Dimensions'
WEIGHT = 'Weight'
COMMA = ','
NEW_LINE = '\n'

def clean_string(attribute):
	if not attribute:
		return attribute
	attribute = attribute.encode('ascii', 'ignore').strip()
	attribute = attribute.replace(',', '#')
	return attribute
	
def get_details():
	browser = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')

	file = open('books_amazon', 'r')
	author_file = open('authors_amazon', 'r')
	category_file = open('categories_amazon', 'r')
	output_file = open('books_amazon_output.csv', 'w+')
	
	header = NAME+COMMA+CATEGORY+COMMA+AUTHOR+COMMA+PRICE+COMMA+SERIES+COMMA+PAGES+COMMA+PUBLISHER+COMMA+DATE+COMMA+LANGUAGE+COMMA+ISBN_10+COMMA+ISBN_13+COMMA+DIMENSIONS+COMMA+WEIGHT+NEW_LINE
	output_file.write(header)
	output_file.flush()

	#Open each book url and get the details
	exception_count = 0
	for book_url in file:
		try:
			browser.get(book_url)
			category = category_file.readline()
			author = author_file.readline()
			category = clean_string(category)
                        author = clean_string(author)
			soup = BeautifulSoup(browser.page_source, 'lxml')
			name_tag = soup.find("span", id="productTitle")
			#paperback_tags = soup.find_all('span', text='Paperback')
			#price_tag = paperback_tags[1].findNext('span', class_='a-size-base a-color-price a-color-price')

			price = ''
			button_tags = soup.find_all(class_='a-button-text')
			for tag in button_tags:
				if('Paperback' in tag.get_text()):
					price_tag = tag.findNext('span', class_='a-size-base a-color-price a-color-price')
					price = clean_string(price_tag.get_text())
					break

			name = clean_string(name_tag.get_text())
				
			isbn_13 = ''
			isbn_10 = ''
			language = ''
			pages = ''
			dimensions = ''
			publisher_date = ''
			series = ''
			weight = ''
			publisher = ''
			date = ''

			#tags = {}
			for li in soup.select('table#productDetailsTable div.content ul li'):
        			title = li.b
        			key = title.text.strip().rstrip(':')
        			value = title.next_sibling
				if(not value):
					continue
				#print(value)
				#value = value.strip()
				value = clean_string(value)
				if('ISBN-13' in key):
					isbn_13 = value
				elif('ISBN-10' in key):
					isbn_10 = value
				elif('Language' in key):
					language = value
				elif('Paperback' in key):
					pages = value
				elif('Dimensions' in key):
					dimensions = value
				elif('Publisher' in key):
					publisher_date = value
					#print (publisher_date)
					publisher = publisher_date.split('(')[0].strip()
					date = publisher_date.split('(')[1].strip()[:-1].replace(',', '')
				elif('Series' in key):
					series = value
				elif('Weight' in key):
					weight = value[:-1].strip()

        			#tags[key] = value
			#print(name, category, author, price, series, pages, publisher, date, language, isbn_10, isbn_13, dimensions, weight)
			
			#write to file
                        line = ''
                        line = name+COMMA+category+COMMA+author+COMMA+price+COMMA+series+COMMA+pages+COMMA+publisher+COMMA+date+COMMA+language+COMMA+isbn_10+COMMA+isbn_13+COMMA+dimensions+COMMA+weight+NEW_LINE
                        print(line)
                        output_file.write(line)
                        output_file.flush()

		except:
			exception_count += 1
			print('An exception occured in the url %s' %(book_url))
			traceback.print_exc()	

	print("Exception count is %d" %(exception_count))
	file.close()
	author_file.close()
	category_file.close()
	output_file.close()

get_details()
