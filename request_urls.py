# coding: UTF-8

import sys
import argparse
import configparser
import urllib.parse
import urllib.request

# ======================================
# argparse
# ======================================
parser = argparse.ArgumentParser(description='Request and save results.')
parser.add_argument("-s", "--section", default='DEFAULT', help='Section in config.ini')
parser.add_argument("url_path", help='URL path to request')
args = parser.parse_args()

# ======================================
# configparser
# ======================================
config = configparser.ConfigParser()
config.read('config.ini')

########################################
# main
########################################
try:
  print(args.url_path)
  print(config[args.section]['RequestUrl'])
  url = urllib.parse.urljoin(config[args.section]['RequestUrl'], args.url_path)
  print(url)
  req = urllib.request.Request(url)
  with urllib.request.urlopen(req) as response:
    the_page = response.read()
    print(the_page)

except Exception as e:
  print(e, file=sys.stderr)
