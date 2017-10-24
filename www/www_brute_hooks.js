// ==UserScript==
// @name        www_brute_hooks
// @namespace   www_brute_hooks
// @version     1
// @grant       none
// @run-at document-start
// ==/UserScript==

window.__alert = window.alert
window.alert = function(mess) { console.log("alert( " + mess + " )") }
console.info("alert() disable")