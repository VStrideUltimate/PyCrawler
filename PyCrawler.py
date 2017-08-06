"""
File: PyCrawler.py
Author: Dylan Wagner
Date: August 2017
Description:
	Program used to discover and follow links as they are gathered of a given web domain.

"""
import sys
import requests


__author__ = 'Dylan Wagner'
__version__ = 0.1


class Crawler(object):
	"""
	Crawler class:
		Used to recursively map domain pages.
	"""
	def __init__(self, url_inpt):
		self.url_inpt = url_inpt
		self.linked_pages = {}
		self.bulid_relation(self.url_inpt)


	def get_source(self, call_url):

		# attempt to gather URL source code.
		try:
			req = requests.request('GET', call_url) 

			if req.status_code == 404:
				return 'ERROR -> 404'
			else:
				return req.text

		except requests.exceptions.ConnectionError:

				return 'ERROR -> No Connection'
	

	def in_domain(self, call_url):

		return self.url_inpt in call_url


	def find_links(self, source):
		return []


	def find_domain_links(self, source):
		# find all links to domain in source
		links = self.find_links(source)

		return [link for link in links if self.in_domain(link)] # list comprehension


	def bulid_relation(self, call_url):
		# recursively build web domain graph
		if call_url in self.linked_pages:
			return

		self.linked_pages[call_url] = []
		source = self.get_source(call_url)

		if source[:5] == 'ERROR':
			self.linked_pages[call_url].append(source)
			return

		links = self.find_domain_links(source)

		for link in links:
			self.linked_pages[call_url].append(link)
			self.bulid_relation(link)


def help():
	print("Usage: python3 PyCrawler.py [URL]")


def main():

	if len(sys.argv) < 2:
		help()
		exit()

	crawl = Crawler(sys.argv[1])
	print(crawl.linked_pages)

main()