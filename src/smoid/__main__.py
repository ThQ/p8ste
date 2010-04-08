#!/usr/bin/python


import getopt
import os
import os.path
import sys

import __init__

short_options = "dhpv"
long_options = []
options, arguments = getopt.gnu_getopt(sys.argv[1:], short_options, long_options)

def print_err (msg):
    sys.stderr.write("[Error] " + msg + "\n")

def show_usage ():
    print "Usage: smoid [OPTION]... [FILE_NAME]..."
    print "Ex: smoid -dhv my_directory/"
    print ""
    print "Options:"
    print " -d       Treat the arguments as directory paths"
    print " -p       Print the file path along the language name"
    print " -v       Show the results of individual checks"

class SmoidOptions:
    def __init__ (self):
        self.run = True
        self.files = []
        self.directories = []
        self.verbose = False
        self.treat_arguments_as_directories = False
        self.show_file_paths = False

    def has_items (self):
        result = False
        if self.treat_arguments_as_directories:
            result = len(self.directories) > 0
        else:
            result = len(self.files) > 0
        return result

smoptions = SmoidOptions()
for option, value in options:
    if option == "-v":
        smoptions.verbose = True
    elif option == "-p":
        smoptions.show_file_paths = True
    elif option == "-d":
        smoptions.treat_arguments_as_directories = True
    elif option == "-h":
        smoptions.run = False

for argument in arguments:
    if smoptions.treat_arguments_as_directories:
        smoptions.directories.append(argument)
    else:
        smoptions.files.append(argument)

if smoptions.run and smoptions.has_items() :
    checker = __init__.GrandChecker()
    checker.verbose = smoptions.verbose

    # A list of directory paths was submitted, list them and print the
    # result for each file found.
    if smoptions.treat_arguments_as_directories:
        for dir_path in smoptions.directories:
            if os.path.isdir(dir_path):
                files = sorted(os.listdir(dir_path))
                for item in files:
                    item_path = os.path.join(dir_path, item)
                    if os.path.isfile(item_path):
                        lang = checker.find_out_language_of_file(item_path)
                        if smoptions.show_file_paths:
                            print item_path,
                        print lang,
                        print ""
            else:
                print_err ("%s is not a directory path" % dir_path)
    else:
        for file_path in smoptions.files:
            if os.path.isfile(file_path):
                lang = checker.find_out_language_of_file(file_path)
                if smoptions.show_file_paths:
                    print file_path,
                print lang,
                print ""
            else:
                print_err("%s is not a file path" % file_path)
else:
    show_usage()
