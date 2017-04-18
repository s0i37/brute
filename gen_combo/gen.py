#!/usr/bin/python

# -*- coding: utf-8 -*-
import re
from sys import argv, stderr
import json
from transliterate import translit
from os.path import exists
from getopt import getopt
from datetime import datetime
import Levenshtein

CONSOLE_CODEPAGE = 'cp866'
name_db_file = 'names.json'
surname_db_file = 'surnames.txt'
YEAR = datetime.now().year
password_patterns = {}

def switch_kbd( keys_layout, string_ru='' ):
	string_swithed = ''
	for char in string_ru:
		string_swithed += keys_layout["en"][ keys_layout["ru"].index(char) ]
	return string_swithed

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

def escape( string ):
	safe_string = ''
	bad_chars = "[](){}<>^+|?.$\\"
	for char in string:
		if char in bad_chars:
			safe_string += '\\'
		safe_string += char
	return safe_string

def levenshtein( names_db, name_ascii, limit_ratio=0.0 ):
	max_ratio = 0
	name_ascii = name_ascii.lower()
	#name_ascii = name_ascii.replace('iya','ija')
	#name_ascii = name_ascii.replace('ya','ja').replace('yu','ju').replace('iy','ij')
	name_unicode_in = translit( name_ascii, 'ru' )
	name = ''
	for name_unicode in names_db:
		name_unicode = name_unicode.lower()
		ratio = Levenshtein.ratio( name_unicode, name_unicode_in )
		if ratio >= limit_ratio and ratio > max_ratio:
			max_ratio = ratio
			name = name_unicode
	return name

'''
def get_like_name( names_db, name_ascii ):
	word_errors = 2
	name_ascii = name_ascii.lower()
	name_ascii = name_ascii.replace('iya','ija')
	name_ascii = name_ascii.replace('ya','ja').replace('yu','ju').replace('iy','ij')
	name_unicode_in = translit( name_ascii, 'ru' )
	chars_pairs = set()
	for off in xrange( len(name_unicode_in) - 1 ):
		chars_pairs.add( name_unicode_in[off:off+2] )

	names_chars_pairs = {}
	for name_unicode in names_db.keys():
		name_unicode = name_unicode.lower()
		name_chars_pairs = set()
		for off in xrange( len(name_unicode) -1 ):
			name_chars_pairs.add( name_unicode[off:off+2] )
		names_chars_pairs[ name_unicode ] = name_chars_pairs

	max_matches = 0
	max_matches_name = ''
	_chars_pairs = _name_chars_pairs = ()
	for name_unicode,name_chars_pairs in names_chars_pairs.items():
		matches = chars_pairs & name_chars_pairs
		if len(matches) > max_matches and len(name_unicode_in) >= len(name_unicode) and len(matches) > (len(name_unicode_in)-1)-word_errors*2:
			max_matches = len(matches)
			max_matches_name = name_unicode
			_chars_pairs = chars_pairs
			_name_chars_pairs = name_chars_pairs

	return max_matches_name
'''

def get_password_patterns( names_db, name_unicode='' ):
	return names_db.get( name_unicode )



class Name:
	def __init__(self, name_en):
		self.name_en = name_en

	def __str__(self):
		return self.name_en

	@property
	def ru(self):
		return levenshtein( password_patterns['names']['names'].keys(), self.name_en )

	@property
	def ru_switched(self):
		return switch_kbd( password_patterns['names']['keyboard_layout'], self.ru )


class Surname:
	def __init__(self, name_en):
		self.surname_en = name_en

	def __str__(self):
		return self.surname_en

	@property
	def ru(self):
		return levenshtein( password_patterns['surnames'], self.surname_en )

	@property
	def ru_switched(self):
		return switch_kbd( password_patterns['names']['keyboard_layout'], self.ru )


class Passwords:
	def __init__(self, userdom_mask='__SURNAME__@__DOMAIN__' ):
		self.o = open('out.log','w')
		self.password_patterns = {}
		self.generate_operations = []
		self.is_exist_name = False
		self.is_exist_surname = False
		self.is_exist_domain = False
		self.is_debug = False
		if userdom_mask.find('__SURNAME__') != -1:
			self.is_exist_surname = True
		if userdom_mask.find('__NAME__') != -1:
			self.is_exist_name = True
		if userdom_mask.find('__DOMAIN__') != -1:
			self.is_exist_domain = True
		self.regexp = escape( userdom_mask ).replace('*', '(?:.{1})').replace('__NAME__', '(?P<name>.*)').replace('__SURNAME__', '(?P<surname>.*)').replace('__DOMAIN__', '(?P<domain>.*)')

	def set_password_patterns( self, password_patterns={} ):
		self.password_patterns = password_patterns

	def set_generate_operations( self, generate_operations=[] ):
		self.generate_operations = generate_operations

	def generate( self, userdom ):
		def extract_part(match, name=''):
			try:	return match.group( name ).lower()
			except:	pass
		
		userdom = userdom.strip().lower()
		if not userdom:
			return
		
		if self.is_debug:
			stderr.write( "[debug] regexp: {regexp}\n".format( regexp=self.regexp ) )

		m = re.match(self.regexp, userdom)
		if not m:
			stderr.write( '[warn] {login} parse fail\n'.format( login=userdom ) )
			return
		name = extract_part(m, 'name') if self.is_exist_name else ''
		surname = extract_part(m, 'surname') if self.is_exist_surname else ''
		domain = extract_part(m, 'domain') if self.is_exist_domain else ''
		parts = {"name": name, "surname": surname, "domain": domain}

		if self.is_debug:
			stderr.write( "[debug] name={name}, surname={surname}, domain={domain}\n".format(name=name, surname=surname, domain=domain) )

		if self.generate_operations:
			for generate_operation in self.generate_operations:
				Passwords.__dict__[generate_operation](self, userdom, parts)
		else:
			if self.password_patterns and 'names' in self.password_patterns["names"].keys() and len(name) >= 3:
				self._gen_passwords_by_name(userdom, parts)
				self._gen_passwords_by_name_switch_kbd(userdom, parts)
				self._gen_passwords_by_name_ru(userdom, parts)
			if len(surname) >= 3:
				self._gen_passwords_by_surname(userdom, parts)
				self._gen_passwords_by_surname_ru_switch_kbd(userdom, parts)
			if len(name) >=3 and len(surname) >= 3:
				self._gen_passwords_by_NS(userdom, parts)


	def _gen_passwords_by_name( self, userdom, parts ):
		name = Name( parts["name"] )

		if self.is_debug:
			stderr.write( "[debug] _gen_passwords_by_name()\n" )
		if self.is_debug:
			stderr.write( "[debug] {name} -> {name_ru}\n".format( name=name, name_ru=name.ru.encode( CONSOLE_CODEPAGE ) ) )

		for suffix in self.password_patterns['names']['suffixes']:
			print "{login}:{password}".format( login=userdom, password="{Name}{suffix}".format( Name=str(name).capitalize(), suffix=suffix ) )

	def _gen_passwords_by_name_ru_switch_kbd( self, userdom, parts ):
		name = Name( parts["name"] )

		if self.is_debug:
			stderr.write( "[debug] _gen_passwords_by_name_switch_kbd()\n" )
		self.o.write( "{name} -> {name_ru}\n".format( name=name, name_ru=name.ru.encode( 'utf-8' )) )
		if not name.ru:
			return
		if self.is_debug:
			stderr.write( "[debug] {name} -> {name_ru} -> {name_switched}\n".format( name=name, name_ru=name.ru.encode( CONSOLE_CODEPAGE ), name_switched=name.ru_switched ) )

		for suffix in self.password_patterns['names']['suffixes']:
			print "{login}:{password}".format( login=userdom, password="{Name}{suffix}".format( Name=str(name.ru_switched).capitalize(), suffix=suffix) )

	def _gen_passwords_by_surname( self, userdom, parts ):
		surname = Surname( parts["surname"] )

		if self.is_debug:
			stderr.write( "[debug] _gen_passwords_by_surname()\n" )

		for suffix in self.password_patterns['names']['suffixes']:
			print "{login}:{password}".format( login=userdom, password="{Surame}{suffix}".format( Surame=str(surname).capitalize(), suffix=suffix) )
			print "{login}:{password}".format( login=userdom, password="{Sur}{suffix}".format( Sur=str(surname)[0].upper() + str(surname)[1:3], suffix=suffix ) )

	def _gen_passwords_by_surname_ru_switch_kbd( self, userdom, parts ):
		surname = Surname( parts["surname"] )

		if self.is_debug:
			stderr.write( "[debug] _gen_passwords_by_surname_ru()\n" )
		self.o.write( "{surname} -> {surname_ru}\n".format( surname=surname, surname_ru=surname.ru.encode('utf-8') ) )
		if not surname.ru:
			return
		if self.is_debug:
			stderr.write( "[debug] {surname} -> {surname_ru}\n".format( surname=surname, surname_ru=surname.ru.encode( CONSOLE_CODEPAGE ) ) )

		for suffix in self.password_patterns['names']['suffixes']:
			print "{login}:{password}".format( login=userdom, password="{Surname}{suffix}".format( Surname=str(surname.ru_switched).capitalize(), suffix=suffix ) )

	def _gen_passwords_by_NS( self, userdom, parts ):
		name = Name( parts["name"] )
		surname = Surname( parts["surname"] )
		
		if self.is_debug:
			stderr.write( "[debug] _gen_passwords_by_NS()\n" )

		for suffix in self.password_patterns['names']['suffixes']:
			print "{login}:{password}".format( login=userdom, password="{NameSurname}{suffix}".format( NameSurname=str(name).capitalize() + str(surname).capitalize(), suffix=suffix ) )

	def _gen_passwords_by_domain( self, userdom, parts ):
		domain = parts["domain"]

		if self.is_debug:
			stderr.write( "[debug] _gen_passwords_by_NS()\n" )

		for suffix in self.password_patterns['names']['suffixes']:
			print "{login}:{password}".format( login=userdom, password="{domain}{suffix}".format( domain=domain.capitalize(), suffix=suffix ) )

def main():
	global password_patterns
	is_debug = False
	generate_types = { 
		"name": "_gen_passwords_by_name",
		"name_switch": "_gen_passwords_by_name_ru_switch_kbd",
		"surname": "_gen_passwords_by_surname",
		"surname_switch": "_gen_passwords_by_surname_ru_switch_kbd",
		"ns": "_gen_passwords_by_NS",
		"domain": "_gen_passwords_by_domain",
	}
	generate_operations = []
	(opts,args) = getopt( argv[1:], "d", ["generate="])
	for opt,val in opts:
		if opt == "-d":
			is_debug = True
		elif opt == '--generate':
			generate_operations.append( generate_types[val] )

	if len(args) < 2:
		print "\n{prog} (opts) loginmask [in_dict|login]".format( prog=argv[0] )
		print "Options:"
		print "\t-d\t\t\tShow debug message"
		print "\t--generate=TYPE\t\tSet type generation of passwords"
		print "\t\t\t\tTYPE: " + ",".join( generate_types.keys() )
		print "Example:"
		print "\t{prog} __NAME__.__SURNAME__@__DOMAIN__ users.txt".format( prog=argv[0] )
		print "\t{prog} **__SURNAME__@__DOMAIN__ user@domain.com".format( prog=argv[0] )
		exit()

	userdom_mask = args[0]
	dictfile_in = args[1]

	out = Passwords( userdom_mask )
	out.is_debug = is_debug
	out.set_password_patterns( { "names": load_name_db(name_db_file), "surnames": load_surname_db(surname_db_file) } )
	password_patterns = out.password_patterns
	out.set_generate_operations( generate_operations )
	if exists(dictfile_in):
		with open( dictfile_in, 'r' ) as f:
			for userdom in f.read().split('\n'):
				out.generate( userdom )
	else:
		userdom = args[1]
		out.generate( userdom )

if __name__ == '__main__':
	main()