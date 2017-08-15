"""
File: PrintPyCrawler.py
Author: Dylan Wagner
Date: August 2017
Description:
	Used to print information of the crawled domain.
"""

import sys
import PyCrawler
from datetime import timedelta
from datetime import datetime
import time


def print_info(started, valid, crawled_domain):
    time_elapased = time.time() - started
    print("----------     Results    ----------")
    print("Started at: " + crawled_domain.url_inpt)
    print("Total links followed: " + str(len(valid)))
    print("Time Elapsed: " + str(timedelta(seconds=time_elapased)))


def print_links_followed_inter(valid):
    print("---------- Links Followed ----------")

    for i in range(len(valid)):
        print('{0: <5}'.format(str(i)) + valid[i])


def print_usage():
    print("Usage: python3 PyCrawler.py [URL] [Root of Domain]\
 '.' for interactive mode")


def print_links_followed(valid):
    for link in valid:
        print(link)


def main():
    if len(sys.argv) < 3:
        print_usage()
        exit()

    if sys.argv[2] not in sys.argv[1]:
        print("Root domain must be part of provided url.")
        exit()

    started = time.time()
    crawled_domain = PyCrawler.Crawler(sys.argv[1], sys.argv[2])
    valid = [x for x in crawled_domain.linked_pages]
    valid.sort()

    if len(sys.argv) > 3:

        print("----------    PyCrawler   ----------")
        print("Version: " + str(PyCrawler.__version__))
        print("Started at: " + str(datetime.now()))

        print_info(started, valid, crawled_domain)
        print_links_followed_inter(valid)

        while True:
            inpt = input("[PyCrawler]>> ")

            if inpt.isdigit():
                if int(inpt) < len(valid) and int(inpt) >= 0:
                    lst = crawled_domain.linked_pages[valid[int(inpt)]]
                    for i in lst:
                        print(i)
            else:
                exit()
    else:
        print_links_followed(valid)

main()
