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


def get_source(call_url):
    # attempt to gather URL source code.
    try:
        req = requests.request('GET', call_url)

        if req.status_code == 404:
            return 'ERROR -> 404'
        else:
            return req.text

    except requests.exceptions.ConnectionError:

        return 'ERROR -> No Connection'


def find_links(source):
    links = []
    soup = BeautifulSoup(source, "html.parser")

    for link in soup.findAll('a'):
        href = link.get("href")
        if href is not None:
            links.append(href)

    return links


def fix_path(url, call_url):
    parsed_url = urlparse(url)
    parsed_call = urlparse(call_url)
    split_url_path = parsed_url.path.split('/')
    split_call_path = parsed_call.path.split('/')
    path_to_append = ''

    if parsed_url.hostname is None:

        if split_url_path[0] is not '':
            pathd = [seg for seg in split_call_path if '.' not in seg]

            move_below = len(pathd) - split_url_path.count('..')
            path_to_append = '/'.join(pathd[:move_below]) + '/'

    formt = [prt for prt in split_url_path if '..' not in prt]
    path_to_append += '/'.join(formt)

    return "{url.scheme}://{url.netloc}{path}".format(url=parsed_call, path=path_to_append)


class Crawler(object):
    """
    Crawler class:
        Used to recursively map domain pages.
    """

    def __init__(self, url_inpt, root):
        self.url_inpt = url_inpt
        self.root = root
        self.linked_pages = {}
        self.build_relation(self.url_inpt)

    def in_domain(self, call_url):

        call_url = urlparse(call_url).hostname
        if call_url is None:
            return False

        return self.root in call_url

    def find_domain_links(self, source, call_url):  # FIX THIS!!!!!
        # find all links to domain in source
        links = find_links(source)

        for i in range(len(links)):
            links[i] = fix_path(links[i], call_url)

        return [url for url in links if self.in_domain(url)]

    def build_relation(self, call_url):
        # recursively build web domain graph
        if call_url in self.linked_pages:
            return

        self.linked_pages[call_url] = []
        source = get_source(call_url)

        if source[:5] == 'ERROR':
            self.linked_pages[call_url].append(source)
            return

        links = self.find_domain_links(source, call_url)

        for link in links:
            if link not in self.linked_pages[call_url]:
                self.linked_pages[call_url].append(link)
            self.build_relation(link)


def print_usage():
    print("Usage: python3 PyCrawler.py [URL] [Root of Domain]")


def main():
    if len(sys.argv) < 3:
        print_usage()
        exit()

    if sys.argv[2] not in sys.argv[1]:
        print("Root domain must be part of provided url.")
        exit()

    crawl = Crawler(sys.argv[1], sys.argv[2])
    print(crawl.linked_pages)


main()
