"""
File: PyCrawler.py
Author: Dylan Wagner
Date: August 2017
Description:
	Program used to discover and follow links as they are gathered of a given web domain.

"""
import sys
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

__author__ = 'Dylan Wagner'
__version__ = 0.1


class Crawler(object):
    """
    Crawler class:
        Used to recursively map domain pages.
    """

    def __init__(self, url_inpt, root):
        self.url_inpt = url_inpt
        self.root = root
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

        call_url = urlparse(call_url).hostname
        if call_url is None:
            return False

        return self.root in call_url

    def find_links(self, source):
        links = []
        soup = BeautifulSoup(source, "html.parser")

        for link in soup.findAll('a'):
            links.append(link.get("href"))

        return links

    def find_domain_links(self, source): # FIX THIS!!!!!
        # find all links to domain in source
        links = [ln for ln in self.find_links(source) if ln != '/' and ln is not None]

        for i in range(len(links)):
            parsed_link = urlparse(links[i])
            if len(parsed_link.netloc) is 0:
                parsed_uri = urlparse(self.url_inpt)
                links[i] = '{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri) + '{link.path}'.format(link=parsed_link)

        return [x for x in links if self.in_domain(x)]

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
    print("Usage: python3 PyCrawler.py [URL] [Root of Domain]")


def main():
    if len(sys.argv) < 3:
        help()
        exit()

    if sys.argv[2] not in sys.argv[1]:
        print("Root domain must be part of provided url.")
        exit()

    crawl = Crawler(sys.argv[1], sys.argv[2])
    print(crawl.linked_pages)


main()
