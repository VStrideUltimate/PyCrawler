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
	def __init__(self, url_inpt):
		self.url_inpt = url_inpt
		self.linked_pages = {}
		self.bulid_relation(self.url_inpt)

	def get_source(self, call_url):
		req = requests.request('GET', call_url)
		return req.text
	

	def find_domain_links(self, source):
		# find all links to domain in source
		return []

	def bulid_relation(self, call_url):
		# recursively build web domain graph
		if call_url in self.linked_pages:
			return

		self.linked_pages[call_url] = []
		source = self.get_source(call_url)
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