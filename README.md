# PyCrawler
Program used to recursively discover and follow links as they are gathered of a given web domain.

import PyCrawler

PyCrawler.Crawler([Starting URL])

[Starting URL] Ex: http://domain.com

Explored web domain can be gathered as a Dictionary by accessing the
PyCrawler.linked_pages


## Provided Interface
---
### PrintPyCrawler
Print interface for the PyCrawler module. Runnable in interactive mode and shout mode.

Usage:
python3 PrintPyCrawler.py [Starting URL] {.}

Note: Passing an extra argument enters interactive mode.
