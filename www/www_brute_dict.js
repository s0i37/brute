// ==UserScript==
// @name        www_brute_dict
// @namespace   www_brute_dict
// @version     1
// @grant       none
// ==/UserScript==

if( window.__brute == undefined )
	window.__brute = []

window.__brute.push( {
	allow: [ /.*/ ],
	deny: [],
	combo: [

	],
	users: [
		"admin",
		"administrator",
		"root",
		"test",
	],
	passwords: [
		"1",
		"12",
		"123",
		"1234",
		"12345",
		"123456",
		"1234567",
		"12345678",
		"123456789",
		"87654321",
		"987654321",
		"11111",
		"111111",
		"22222",
		"55555",
		"555555",
		"777",
		"77777",
		"7777777",
		"00000",
		"54321",
		"123321",
		"654321",
		"666666",
		"password",
		"secret",
		"root",
		"toor",
		"sa",
		"administrator",
		"admin",
		"nimda",
		"gfhjkm",
		"ljcneg",
		"computer",
		"internet",
		"service",
		"test",
		"shadow",
		"success",
		"foobar",
		"welcome",
		"hello",
		"access",
		"control",
		"connect",
		"zxcvbnm",
		"zxczxc",
		"asdfgh",
		"asdfjkl;",
		"qwerty",
		"qwert",
		"aaaaaa",
		"abc",
		"ABC123",
		"1q2w3e",
		"a12345",
		"a1b2c3d4"
	]
} )