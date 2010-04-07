#!/usr/bin/python


import sys

import __init__


checker = __init__.GrandChecker()
checker.verbose = True
checker.find_out_language_of_file(sys.argv[1])
