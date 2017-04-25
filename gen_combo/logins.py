#!/usr/bin/python
import os
from sys import argv

TEMPLATE = "%(name).02s%(surname)s@domain.com"

def readfile(filename):
	with open(filename, 'r') as f:
		return f.read().split('\r\n')


names_man = readfile( "data/top_names_man.txt" )
names_woman = readfile( "data/top_names_woman.txt" )
surnames_man = readfile( "data/top_surnames_man.txt" )
surnames_woman = readfile( "data/top_surnames_woman.txt" )

def gen_top100():
	for name_man in names_man:
		for surname_man in surnames_man:
			print TEMPLATE % { 'name': name_man, 'surname': surname_man }

	for name_woman in names_woman:
		for surname_woman in surnames_woman:
			print TEMPLATE % { 'name': name_woman, 'surname': surname_woman }

def gen_custom(userlist_filename):
	with open(userlist_filename, 'r') as f:
		for user in f:
			user = user.split('\n')[0]
			surname = name = middlename = ''
			try:
				parts = user.split(' ')
				surname = parts[0]
				name = parts[1]
				middlename = parts[2]
			except:
				pass
			if surname:
				print TEMPLATE % { 'name': name, 'surname': surname }

if len(argv) > 1:
	userlist_filename = argv[1]
	if os.path.isfile(userlist_filename):
		gen_custom(userlist_filename)
else:
	gen_top100()