#!/usr/bin/python
from sys import argv

#TEMPLATE = "%(name).02s%(surname)s@domain.com"

def readfile(filename):
	with open(filename, 'r') as f:
		return f.read().split('\r\n')


names_man = readfile( "data/top_names_man.txt" )
names_woman = readfile( "data/top_names_woman.txt" )
surnames_man = readfile( "data/top_surnames_man.txt" )
surnames_woman = readfile( "data/top_surnames_woman.txt" )


for name_man in names_man:
	for surname_man in surnames_man:
		print TEMPLATE % { 'name': name_man, 'surname': surname_man }

for name_woman in names_woman:
	for surname_woman in surnames_woman:
		print TEMPLATE % { 'name': name_woman, 'surname': surname_woman }