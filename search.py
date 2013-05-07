import os, sys
from django.utils import timezone
import urllib

def siftUp( index, node ):
	if (len(index) <= 1):
		return index
	while (node > 0):
		parent = (node - 1) / 2
		if (index[parent]["data"] > index[node]["data"]):
			temp = index[parent]
			index[parent] = index[node]
			index[node] = temp
			node = parent
		else:
			break
	return index

def siftDown( index, node ):
	if (len(index) <= 1):
		return index
	temp = index[0]
	index[0] = index[node]
	index[node] = temp
	ptr = 0
	while (ptr < node):
		left = ptr * 2 + 1
		right = left + 1
		if (left >= node):
			break
		minimum = left
		if (right < node and index[left]["data"] > index[right]["data"]):
			minimum = right
		if (index[ptr]["data"] > index[minimum]["data"]):
			temp = index[ptr]
			index[ptr] = index[minimum]
			index[minimum] = temp
			ptr = minimum
		else:
			break
	return index

def heapsort( index ):
	for i in range(0, len(index)):
		index = siftUp(index, i)
	for i in range(len(index) - 1, 0, -1):
		index = siftDown(index, i)
	return index

def get_page( url ):
	page = ""
	fp = open(url, 'r')
	if (fp):
		page = fp.read()
		fp.close()
	else:
		try:
			return urllib.urlopen(url).read()
		except:
			return page
	return page

def get_all_links( page ):
	links = []
	startIndex = page.find("openURL")
	while (startIndex != -1):
		startIndex = page.find("'", startIndex) + 1
		endIndex = page.find("'", startIndex)
		links.append(page[startIndex:endIndex])
		startIndex = page.find("openURL", startIndex)
	return links

def get_word_frequency( page, word, ignore_case = True ):
	occurences = 0
	if (ignore_case):
		page = page.lower()
		word = word.lower()
	location = page.find(word)
	while (location != -1):
		occurences++
		location = page.find(word, location + 1)
	return occurences

def crawl_web( seed, words ):
	index = []
	links = [seed]
	i = 0
	while i < len(links):
		page = get_page(links[i])
		if (page != ""):
			# get links
			page_links = get_all_links(page)
			for link in page_links:
				if (link not in links):
					links.append(link)
			# get the rank (url storage mechanism, not keyword)
			rank = 0
			for word in words:
				if (links[i].find(word) != -1):
					rank += 5
				rank += get_word_frequency(page, word)
			if rank > 0:
				index.append({"data": rank, "url": links[i]})
		i++
	return index

def search( query ):
	words = []
	# tokenize
	valid = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
	start = 0
	for end in range(0, len(query)):
		if (find(valid, (query[end])) != -1):
			if (start < end):
				words.append(query[start:end])
			start = end + 1
		if (end == len(query) and start < end):
			words.append(query[start:end])
	# crawl
	index = crawl_web("index.html", words)
	# sort results
	index = heapsort(index)
	return index
