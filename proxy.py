#!/usr/bin/python3
import multiprocessing
import sys
from bs4 import BeautifulSoup
import os
import argparse
import time
from security import safe_requests


# Python program to print colored text and background
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))


def proxyscrapeScraper(api_url2, typep):
	r = safe_requests.get(api_url2, timeout=60)
	
	for line in r.content.decode("utf-8").splitlines():
		x = line.split(":")
		print(" |{:<18} | {:<8} | {:<8} | {:<12} | {:<14}|".format(x[0], x[1], typep, "-"  , "-"))

		
def proxyFromApi(api_url):

	r = safe_requests.get(api_url, timeout=60)
	json_data = r.json()
	
	for values in json_data['data']:
		print(" |{:<18} | {:<8} | {:<8} | {:<12} | {:<14}|".format(values['ip'], values['port'], values['protocols'][0] , values['anonymityLevel'],values['country']))

	
def https(proxy_domain):
	
	r = safe_requests.get(proxy_domain, timeout=60)
	soup = BeautifulSoup(r.content, 'html.parser')
	table = soup.find('table', attrs={'class': 'table table-striped table-bordered'})		
	
	table = proxyscrape(proxy_domain)
	
	for row in table.find_all('tr'):
		columns = row.find_all('td')
		
		try: 
			if columns[6].get_text() == "yes":
				print(" |{:<18} | {:<8} | {:<8} | {:<12} | {:<14}|".format(columns[0].get_text(), columns[1].get_text(),"https",columns[4].get_text(),columns[2].get_text()))
			print("yeh")
		except:
			pass


def socks4(proxy_domain):

	r = safe_requests.get(proxy_domain, timeout=60)
	soup = BeautifulSoup(r.content, 'html.parser')
	table = soup.find('table', attrs={'class': 'table table-striped table-bordered'})		
	
	table = proxyscrape(proxy_domain)

	for row in table.find_all('tr'):
		columns = row.find_all('td')
		
		try: 
			if columns[4].get_text() == "Socks4":
				print(" |{:<18} | {:<8} | {:<8} | {:<12} | {:<14}|".format(columns[0].get_text(), columns[1].get_text(),columns[4].get_text(),columns[5].get_text(),columns[2].get_text()))
			print("yeh")
		except:
			pass

			
def proxy_list(proxy_domain, typep):
	
	r = safe_requests.get(proxy_domain, timeout=60)
	soup = BeautifulSoup(r.content, 'html.parser')
	table = soup.find('table', id = "tbl")

	for row in table.find_all('tr'):
		columns = row.find_all('td')
		
		try: 
			print(" |{:<18} | {:<8} | {:<8} | {:<12} | {:<14}|".format(columns[0].get_text(), columns[1].get_text(),typep,columns[2].get_text(),columns[3].get_text()))
	
		except:
			pass
			

if __name__ == "__main__":

	startTime = time.time()
	process = []
	
	ap = argparse.ArgumentParser(description ='Proxy Scraper')
	ap.add_argument("-t", "--type", choices = {'socks4', 'https', 'socks5', 'http'})
	ap.add_argument("-o", "--output", const = "false", nargs = "?")
	args = vars(ap.parse_args())
	
	proxy_domain_https= ["https://free-proxy-list.net/", "https://sslproxies.org/"] 
	proxy_domain_socks4= "https://socks-proxy.net/"
	api_url= "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&speed=fast&protocols=" + args['type']
	api_url2 = "https://api.proxyscrape.com/v2/?request=getproxies&protocol="+ args['type'] +"&timeout=10000&country=all&ssl=all&anonymity=all"
	proxylist = "https://www.proxy-list.download/" + args["type"].upper()
	
	if args["type"] == "https" : 
		for url in proxy_domain_https : 
			proc = multiprocessing.Process(target=https, args = [url])
			proc.start()
			process.append(proc)	
			
	elif args["type"] == "socks4" : socks4(proxy_domain_socks4)
	
	
	prRed("""  , __  , __   __   _     _               ___  , __   ___,  , __  ___  , __  
/|/  \/|/  \ /\_\/r_\  /(_|   |     ()  / (_)/|/  \ /   | /|/  \/ (_)/|/  \ 
 |___/ |___/|    |   \/   |   |     /\ |      |___/|    |  |___/\__   |___/ 
 |     | \  |    |   /\   |   |    /  \|      | \  |    |  |    /     | \   
 |     |  \_/\__/  _/  \_/ \_/|/  /(__/ \___/ |  \_/\__/\_/|    \___/ |  \_/
                             /|                                             
                             \|       
                             
                             				By Solanki Devang""")

	if bool(args["output"]):
		f = open(args["output"], "w")
		prGreen("Writing output to: " + os.getcwd() + "/" + args["output"])
		prGreen("Proxy type: " + args["type"])
		sys.stdout=f
		print(" |{:<18} | {:<8} | {:<8} | {:<12} | {:<14}|".format("IP", "Port", "Type" ,"CN", "Anonymity"))
		
	else: 
		prYellow("|{:<18} | {:<8} | {:<8} | {:<12} | {:<14}|".format("IP", "Port", "Type" ,"CN", "Anonymity"))
	
	for p in process:
		p.join
			
	p1 = multiprocessing.Process(target=proxyFromApi, args = [api_url])
	p2 = multiprocessing.Process(target=proxyscrapeScraper, args = [api_url2, args["type"]])
	p3 = multiprocessing.Process(target=proxy_list, args = [proxylist, args["type"]])
	
	p1.start()
	p2.start()
	p3.start()
	
	p1.join()
	p2.join()
	p3.join()
	
	print ('\n Done this script took {0} second !'.format(time.time() - startTime))
