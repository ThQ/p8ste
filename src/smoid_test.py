#!/usr/bin/python
import smoid
import sys

checker = smoid.GrandChecker()
checker.verbose = True
checker.find_out_language_of_file(sys.argv[1])
