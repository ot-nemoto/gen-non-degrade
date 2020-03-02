# coding: UTF-8

import sys
import os
import re
import json
import argparse
import configparser
import urllib.parse
import urllib.request

# ======================================
# argparse
# ======================================
parser = argparse.ArgumentParser(description='Request and save results.')
parser.add_argument("-s", "--section", default='DEFAULT', help='Section in config.ini')
parser.add_argument("-d", "--dir", required=True, help='Root directory to output results.')
parser.add_argument("url_path", help='URL path to request.')
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
  url = urllib.parse.urljoin(config[args.section]['RequestUrl'], args.url_path)
  req = urllib.request.Request(url)
  print(url)
  with urllib.request.urlopen(req) as res:
    res_body = json.dumps(
      json.loads(res.read().decode('utf-8')), ensure_ascii = False, indent = 2)
    #print(res_body)

except Exception as e:
  print(e, file=sys.stderr)
  res_body = "{0}".format(e)

finally:
  filepath = os.path.join(
    args.dir,
    re.sub('/$', '', re.sub('^/', '', args.url_path)))
  dirname = os.path.dirname(filepath)
  basename = os.path.basename(filepath)

  # make directory if not exists.
  if os.path.exists(dirname) is False:
    os.makedirs(dirname)

  # write response body
  with open("%s/_%s" % (dirname, basename), mode = 'w') as f:
    f.write(res_body)
