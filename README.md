STEM-Site
=========

Converting the only php file to django due to framework choice.

Search Engine functions:

	def search( query ):
		...

query is a string, given in from the user. this function ONLY searches the local site and their html links.

The returning data structure is a linked list of result\_link class:

	[ result_link1, result_link2, ...]

Where the result\_link class is the following:

	class result_link():
		rank = int()
		url = str()
		name = str()
		icon = str()
		description = str()