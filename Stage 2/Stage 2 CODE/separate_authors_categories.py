#!/usr/bin/env

def separate():
	merged_file = open("authors_categories_amazon", "r")
	author_file = open("authors_amazon", "w+")
	categories_file = open("categories_amazon", "w+")
	for i in range(0, 288):
		line = ''
		for j in range(0, 12):
			line = merged_file.readline()
			categories_file.write(line)

		for j in range(0, 12):
			line = merged_file.readline()
			author_file.write(line)

	merged_file.close()
	author_file.close()
	categories_file.close()

separate()
