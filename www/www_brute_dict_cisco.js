// ==UserScript==
// @name        www_brute_dict_cisco
// @namespace   www_brute_dict_cisco
// @version     1
// @grant       none
// ==/UserScript==

if( window.__brute == undefined )
	window.__brute = []

window.__brute.push( {
	allow: [ /.*/ ],
	deny: [],
	combo: [
		['root', 'attack'],
		['root', 'Cisco'],
		['root', 'blender'],
		['root', 'secur4u'],
		['cisco', 'cisco'],
		['Cisco', 'Cisco'],
		['admin', 'cisco'],
		['admin', 'admin'],
		['admin', 'default'],
		['admin', 'diamond'],
		['admin', 'changeme'],
		['Administrator', 'admin'],
		['pnadmin', 'pnadmin'],
		['uwmadmin', 'password'],
		['enable', 'cisco'],
		['cmaker', 'cmaker'],
		['public', 'secret'],
		['ReadOnly', 'secret'],
		['access', 'secret'],
		['private', 'secret'],
		['ReadWrite', 'secret'],
		['netrangr', 'attack'],
		['wlse', 'wlsedb'],
		['hsa', 'hsadb'],
		['End User', '7936']
	],
	users: [
		"admin",
		"Admin",
		"administrator",
		"Administrator",
		"root",
		"cisco",
		"Cisco",
		"cmaker",
		"public",
		"private",
		"access"
	],
	passwords: [
	'c',
	'cc',
	'cisco',
	'Cisco router',
	'letmein',
	'Cisco',
	'_Cisco',
	'changeit'
	]
} )