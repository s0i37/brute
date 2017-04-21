#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import json
import time
from sys import argv
from os.path import exists
from transliterate import translit
import Levenshtein

#TEMPLATE = '(?:.{1})(?:.{1})(?P<name>.*)\.(?P<surname>.*)@(?P<domain>.*)'
TEMPLATE = '(?:.{1})(?:.{1})(?P<surname>.*)@(?P<domain>.*)'

name_db_file = 'data/names.json'
surname_db_file = 'data/surnames.txt'


def load_name_db( filename='' ):
	with open( filename, 'r' ) as f:
		return json.loads( f.read() )

def load_surname_db( filename='' ):
	surnames = []
	with open( filename, 'r') as f:
		while True:
			line = f.readline()
			if not line:
				break
			surnames.append( line.strip().decode('utf-8').lower() )
	return surnames


def switch( string ):
	keys_layout = {
		"en":"qwertyuiop[]asdfghjkl;'zxcvbnm,.",
		"ru":u"йцукенгшщзхъфывапролджэячсмитьбю"
	}
	swithed = ""
	for char in string:
		swithed += keys_layout["en"][ keys_layout["ru"].index(char) ]
	return swithed

def en_ru(string):
	return translit( string, 'ru' )


def levenshtein( names_db, name_ascii, limit_ratio=0.0 ):
	max_ratio = 0
	name_ascii = name_ascii.lower()
	name_unicode_in = en_ru(name_ascii)
	name = ''
	for name_unicode in names_db:
		name_unicode = name_unicode.lower()
		ratio = Levenshtein.ratio( name_unicode, name_unicode_in )
		if ratio >= limit_ratio and ratio > max_ratio:
			max_ratio = ratio
			name = name_unicode
	return name



def get_names(parts):
	results = [ parts['name'] ]
	name_ru = levenshtein( names.keys(), parts['name'] )
	results += names.get(name_ru)
	results += [ switch(name_ru) ]
	return results

def get_surnames(parts):
	results = [ parts['surname'] ]
	surname_ru = levenshtein( surnames, parts['surname'] )
	#results += [ surname_ru ]
	results += [ switch(surname_ru) ]
	return results

def parse( login ):
	def extract_part(match, name=''):
		try:	return match.group( name ).lower()
		except:	pass
	
	login = login.strip().lower()
	m = re.match(TEMPLATE, login)
	if not m:
		return
	name = extract_part(m, 'name') if '<name>' in TEMPLATE else ''
	surname = extract_part(m, 'surname') if '<surname>' in TEMPLATE else ''
	domain = extract_part(m, 'domain') if '<domain>' in TEMPLATE else ''
	parts = {"name": name, "surname": surname, "domain": domain}

	results = []
	if len(name) >= 3:
		results += get_names(parts)
	if len(surname) >= 3:
		results += get_surnames(parts)

	with open(out_file_name, 'w') as o:
		for result in results:
			o.write( "%s\n" % result )


def main():
	while True:
		try:
			login = raw_input()
			parse( login )
		except EOFError:
			pass
		except Exception as e:
			return

if __name__ == '__main__':
	out_file_name = argv[1]
	names = load_name_db(name_db_file)
	surnames = load_surname_db(surname_db_file)
	main()