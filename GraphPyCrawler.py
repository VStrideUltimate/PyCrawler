"""
File: GraphPyCrawler.py
Author: Dylan Wagner
Date: August 2017
Description:
	Used to show website connectivity visualy
"""

import sys
import PyCrawler


def print_usage():
    print("Usage: python3 PyCrawler.py [URL] [Root of Domain]\
 [GraphName]")


def main():
    if len(sys.argv) < 4:
        print_usage()
        exit()

    if sys.argv[2] not in sys.argv[1]:
        print("Root domain must be part of provided url.")
        exit()

	# begin crawling
    crawled_domain = PyCrawler.Crawler(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
   try:
      main()
   except KeyboardInterrupt:
      # do nothing here
      pass
