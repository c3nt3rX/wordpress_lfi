#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser
import socket
import httplib

usage = "python %prog -t google.com"

parser = OptionParser(usage=usage)
parser.add_option("-t", action="store", dest="target",
                  help="Target e.g. google.com")

(options, args) = parser.parse_args()

def test(target):
	test_lfi = open('lfi.txt', 'r').readlines()
	test_lfi = map(lambda s: s.strip(), test_lfi)
	for line in test_lfi:
		try:
			conn = httplib.HTTPConnection(target)
			conn.request("HEAD",line)
			response = conn.getresponse()
			if response.status == 200 or response.status == 301:
				print "[+] Found LFI flaw --> http://"+target+line+"\n"
			elif response.status == 403:
				print "[+] May be interesting --> http://"+target+line
				print "[+] Response: " + str(response.status) + " " + str(response.reason)
				print "[+] You need to bypass it with hex characters or other method.\n"
		except Exception as e:
			print "[!] Failed to check: http://"+target+line
			print "[!] " + str(e)

def test_connection(target):
	try:
		conn = httplib.HTTPConnection(target)
		conn.request("HEAD", "/")
		response = conn.getresponse()
		print "[+] Site response: " + str(response.status) + " " + str(response.reason)
		test_lfi = open('lfi.txt', 'r').readlines()
		test_lfi = map(lambda s: s.strip(), test_lfi)
		tests = len(test_lfi)
		print "[+] Loaded " + str(tests) + " tests against " + target
		print "[+] Scanning target..\n"
		test(target)
	except Exception as e:
		print "[!] Website is down or doesn't exist. Got error: " + str(e)
		print "[!] Exiting :-("

def banner():
        print "\n| ------------------------------------------------------------------- |"
        print "|            Kick-Ass [WordPress File Inclusion by c3nt3rX]           |"
        print "| ------------------------------------------------------------------- |"

if len(sys.argv) < 2:
        banner()
        parser.print_help()
        sys.exit(2)

if __name__ == "__main__":
        banner()
        target = options.target
	print "\n"
	test_connection(target)
