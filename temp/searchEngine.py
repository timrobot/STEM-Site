import os, jinja2

seeds = ["home.html",
         "biology.html",
         "chemistry.html",
         "physics.html",
         "medicine.html",
         "mathematics.html",
         "robotics.html"
        ]

class result_link():
    url = ""
    rank = 0
    name = ""
    icon = ""
    description = ""
    def __init__(self, url = "", rank = 0, name = "", icon = "", description = ""):
        self.url = url
        self.rank = rank
        self.name = name
        self.icon = icon
        self.description = description
    def __cmp__(self, other):
        return cmp(self.rank, other.rank)
    def __str__(self):
        return str([self.url, self.rank])

class Engine():
    jinja_environment = None
    def get_page( self, url ):
	return str(self.jinja_environment.get_template(url).render({}))
    def get_all_links( self, page ):
	links = []
	start = page.find("<a")
	while start != -1:
		end = page.find(">", start)
		startquote = page.find("href", start)
		startquote = page.find("\"", startquote) + 1
		endquote = page.find("\"", startquote)
		if endquote < end:
			links.append(page[startquote:endquote])
		start = page.find("<a", end + 1)
	return links
    def get_word_count( self, page, word, ignore_case = True ):
	count = 0
	if ignore_case:
		page = page.lower()
		word = word.lower()
	location = page.find(word)
	while location != -1:
		count += 1
		location = page.find(word, location + 1)
	return count
    def get_meta_content( self, page, meta ):
	location = page.find("meta")
	while location != -1:
		endtag = page.find(">", location)
		name = page.find("name", location)
		name = page.find("\"", name) + 1
		if name < endtag:
			if page[name:page.find("\"", name)] == meta:
				content = page.find("content", location)
				content = page.find("\"", content) + 1
				if content < endtag:
					return page[content:page.find("\"", content)]
		location = page.find("meta", endtag)
	return ""
    def crawl_web( self, seed, words ):
	index = []
	links = [] + seed
	i = 0
	while i < len(links):
		url = links[i]
		page = self.get_page(url)
		if page:
			page_links = self.get_all_links(page)
			for link in page_links:
				if link.find("http") != -1:
					continue
				if link not in links:
					links.append(link)
			rank = 0
			for word in words:
				if url.find(word) != -1:
					rank += 5
				rank += self.get_word_count(page, word)
			if rank > 0:
				name = self.get_meta_content(page, "name")
				icon = self.get_meta_content(page, "icon")
				description = self.get_meta_content(page, "description")
				result = result_link(url, rank, name, icon, description)
				index.append(result)
		i += 1
	return index
    def search_web( self, query ):
	valid = "abcdefghijklmnopqrstvuwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
	word = ""
	words = []
	for c in query:
		if valid.find(c) != -1:
			word += c
		else:
			if word != "":
				words.append(str(word))
				word = ""
	if word != "":
		words.append(str(word))
	index = Heap()
	index.heap = self.crawl_web(seeds, words)
	index.sort()
	return index.heap

class Heap():
    # this is a min heap
    heap = []
    def __init__(self, heap = []):
        assert type(heap) == type([])
        self.heap = heap
    def sort(self):
        for i in range(0, len(self.heap)):
            self.siftUp(i)
        for i in range(len(self.heap) - 1, 0, -1):
            self.siftDown(i)
    def siftUp(self, ptr):
        if (len(self.heap) <= 1 or ptr >= len(self.heap)):
            return
        while (ptr > 0):
            parent = (ptr - 1) / 2
            if (self.heap[parent] > self.heap[ptr]):
                temp = self.heap[parent]
                self.heap[parent] = self.heap[ptr]
                self.heap[ptr] = temp
                ptr = parent
            else:
                break
    def siftDown(self, ptr):
        if (len(self.heap) <= 1 or ptr >= len(self.heap)):
            return
        temp = self.heap[0]
        self.heap[0] = self.heap[ptr]
        self.heap[ptr] = temp
        maximum = ptr
        ptr = 0
        while (ptr < maximum):
            left = ptr * 2 + 1
            right = left + 1
            if (left >= maximum):
                break
            minimum = left
            if (right < maximum and self.heap[left] > self.heap[right]):
                minimum = right
            if (self.heap[ptr] > self.heap[minimum]):
                temp = self.heap[ptr]
                self.heap[ptr] = self.heap[minimum]
                self.heap[minimum] = temp
                ptr = minimum
            else:
                break
