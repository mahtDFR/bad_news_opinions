import os
import random
import shutil
import string
import time
from itertools import cycle

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import get_tweets  # open file that generates tweets

# initialize a list to keep links in
links = []

# look inside the text file
filehandler = open("source_articles.txt", "r")
lines = filehandler.readlines()
filehandler.close()

for line in lines:  # read each line in file
	if len(line.strip()) == 0:  # if there is whitespace,
		pass  # ignore it
	else:  # otherwise
		links.append(line.strip())  # remove trailing spaces and add link to list

print(str(len(links)) + " link(s) found in source_articles.txt" + "\n")
print(str(len(get_tweets.tweets)) + " tweets scraped" + "\n")  # print the amount of entries in the list

# set up parameters for selenium headless browser to take screenshots
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.page_load_strategy = 'none'

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1920, 1920)
driver.set_page_load_timeout(0.6)
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")

# directory management for temp and output files
path = os.getcwd()
dest = path + "/bad_opinions"
temp = path + "/temp"

# if temp and destination dirs dont already exist, create them
if not os.path.exists(dest):
	print(":: creating directory: " + dest + "\n")
	os.makedirs(dest)

if not os.path.exists(temp):
	print(":: creating directory: " + temp + "\n")
	os.makedirs(temp)

# iterate through links in list infinitely
links_cycle = cycle(links)
total_items = 0

for l in links_cycle:

	source = requests.get(l).text  # request the url
	soup = BeautifulSoup(source, 'lxml')  # make a beautiful soup object to parse html

	headline = soup.h1  # get headline from h1 tags on website
	tweet = (random.choice(get_tweets.tweets))  # pick a random tweet from the tweet list
	headline.string = tweet  # swap out the original headline string with the tweet

	print('"' + headline.text + '"')

	with open("temp\soup.html", "w", encoding='utf-8') as file:  # dump modified html as file in temp dir
		file.write(str(soup))

	while True:
		try:
			driver.get(temp + "\soup.html")  # open modified html in headless browser
			print("page loading")
		except:
			TimeoutException
		break

	# initialize a random ascii character generator to generate random filenames
	filename = "".join(random.choice(string.ascii_lowercase) for r in range(8)) + ".png"

	while True:
		try:
			# screenshot the html element (in this case the element class name is "u-cf")
			driver.find_element_by_class_name("u-cf").screenshot(dest + "/" + filename)
			print(":: png dumped to: " + dest + "/" + filename + "\n")
		except:
			Exception
		break

	# keep count of the amount of output files
	total_items += 1
	# print(":: fake headlines generated: " + str(total_items) + "\n")

	# exit strategy
	if int(total_items) >= 30:
		print("that's enough for now." + "\n")
		break

# final exit routine
driver.quit()
time.sleep(1)
print(":: destroying temp directory" + "\n")
shutil.rmtree(temp)
print("closing. goodbye." + "\n")
exit()
