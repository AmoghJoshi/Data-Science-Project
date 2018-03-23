#!/usr/bin/env
from bs4 import BeautifulSoup
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
	attribute = attribute.encode("ascii").strip()
	attribute = attribute.replace(',', '#')
	return attribute

def get_details():
	browser = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
	exception_count = 0
	file = open('books_millions', 'r')
	category_file = open('categories_millions', 'r')
	output_file = open('books_millions_output.csv', 'w+')
	
	header = NAME+COMMA+CATEGORY+COMMA+AUTHOR+COMMA+PRICE+COMMA+SERIES+COMMA+PAGES+COMMA+PUBLISHER+COMMA+DATE+COMMA+LANGUAGE+COMMA+ISBN_10+COMMA+ISBN_13+COMMA+DIMENSIONS+COMMA+WEIGHT+NEW_LINE
	print (header)
	output_file.write(header)
	output_file.flush()

	#Open each book url and get the details
	for book_url in file:
		try:
			#book_url = 'http://www.booksamillion.com/p/Invaders-Plan/L-Ron-Hubbard/9781619865303?id=7213449419989'
			name = ''
			category = ''
			author = ''
			price = ''
			series = ''
			pages = ''
			publisher = ''
			date = ''
			language = ''
			isbn_10 = ''
			isbn_13 = ''
			dimensions = ''
			weight = ''
			
			browser.get(book_url)
			soup = BeautifulSoup(browser.page_source, 'lxml')
			details = soup.find_all(class_='details-content-text')
			details_list = list(details[-1].children)
			product_details = list(details_list[1].children)

			#print(series_tag.get_text())	
			for product_detail in product_details:
				#print(type(product_detail), product_detail)
				if(not 'Tag' in str(type(product_detail))):
					continue
				#if(not ':' in product_detail.get_text()):
				#	continue
				key = clean_string(product_detail.get_text().split(':')[0])
				value = product_detail.get_text().split(':')[1]
				value = clean_string(value)
				if('ISBN-13' in key):
					isbn_13 = value
				elif('ISBN-10' in key):
					isbn_10 = value
				elif('Publisher' in key):
					publisher = value
				elif('Date' in key):
					date = value
				elif('Count' in key):
					pages = value
				elif('Dimensions' in key):
					dimensions = value
				elif('Weight' in key):
					weight = value
	
			#isbn_13 = product_details[1].get_text().split(':')[1].strip().encode("ascii")
			#isbn_10 = product_details[3].get_text().split(':')[1].strip().encode("ascii")
			#publisher = product_details[5].get_text().split(':')[1].strip().encode("ascii")	
			#publish_date = product_details[7].get_text().split(':')[1].strip().encode("ascii")
			#page_count = product_details[11].get_text().split(':')[1].strip().encode("ascii")

			title_details = soup.find_all(class_='details-title-text')
			name_details = list(title_details[0].children)
			name = clean_string(name_details[0].get_text())
			price_details = list(title_details[1].children)
			price = clean_string(price_details[1].get_text())

			author_details = soup.find_all(class_='details-author-text')
			author_details_list = list(author_details[0].children)
			author = clean_string(author_details_list[1].get_text())
			
			category = clean_string(category_file.readline())			
			#print(name, category, author, price, series, pages, publisher, date, language, isbn_10, isbn_13, dimensions, weight)
			
			#write to file
			line = ''
			line = name+COMMA+category+COMMA+author+COMMA+price+COMMA+series+COMMA+pages+COMMA+publisher+COMMA+date+COMMA+language+COMMA+isbn_10+COMMA+isbn_13+COMMA+dimensions+COMMA+weight+NEW_LINE
			print(line)
			output_file.write(line)
			output_file.flush()
		except:
			exception_count += 1
			print("Exception occured in the following url: %s" %(book_url))
			traceback.print_exc()
		#break

	print("Exception count is %d" %(exception_count))				
	file.close()
	category_file.close()
	output_file.close()
get_details()
