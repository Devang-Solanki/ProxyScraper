# ProxyScraper

This tool scrape proxies from different sites and API as follow:

* [free-proxy](https://free-proxy-list.net/)
* [sslproxies](https://sslproxies.org/)
* [proxylist](https://proxylist.geonode.com/)
* [proxyscrape](https://proxyscrape.com/)
* [proxy-list](https://www.proxy-list.download/)


# Installation

Use the below comand for installing dependencies:

    pip install -r requirements.txt

# Usage

Scrape proxies by using following comand

    python3 proxy.py -t https -o proxy .txt
    
    
   *-t or --type, For chosing proxy type, Supported proxy https, http, socks4, socks5
   * -o or --output, For writing output to a file
   * -h or --help, For help
        
# Credit

[Proxy scraper and checker](https://github.com/iw4p/proxy-scraper)





