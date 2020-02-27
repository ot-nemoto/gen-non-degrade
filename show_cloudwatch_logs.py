# coding: UTF-8

import argparse
import configparser
import json
from datetime import datetime
import boto3
from boto3.session import Session

# ======================================
# argparse
# ======================================
parser = argparse.ArgumentParser(description='Show Amazon CloudWatch Logs.')
parser.add_argument("-s", "--section", default='DEFAULT', help='Section in config.ini')
args = parser.parse_args()

# ======================================
# configparser
# ======================================
config = configparser.ConfigParser()
config.read('config.ini')

LAST_EVENT_TIMESTAMP = int(datetime.strptime('2020-01-01', "%Y-%m-%d").timestamp() * 1000)

def log_stream_names(token = None):
  if token == None:
    response = client.describe_log_streams(
      logGroupName = config[args.section]['LogGroupName'],
      orderBy = 'LastEventTime',
      limit = 10
    )
  else:
    response = client.describe_log_streams(
      logGroupName = config[args.section]['LogGroupName'],
      orderBy = 'LastEventTime',
      nextToken = token,
      limit = 10
    )

  for log_stream in response.get('logStreams'):
    if log_stream.get('lastEventTimestamp') >= LAST_EVENT_TIMESTAMP:
      yield log_stream.get('logStreamName')
  if response.get('nextToken') is not None:
    yield from log_stream_names(response.get('nextToken'))

def log_event_messages(log_stream_name, token = None):
  if token == None:
    response = client.get_log_events(
      logGroupName = config[args.section]['LogGroupName'],
      logStreamName = log_stream_name,
      limit = 100
    )
  else:
    response = client.get_log_events(
      logGroupName = config[args.section]['LogGroupName'],
      logStreamName = log_stream_name,
      nextToken = token,
      limit = 100
    )

  for event in response.get('events'):
    yield event.get('message')

  if response.get('nextForwardToken').split('/')[1] != response.get('nextBackwardToken').split('/')[1]:
    yield from log_event_messages(log_stream_name, response.get('nextBackwardToken'))  

try:
  session = Session(profile_name = config[args.section]['Profile'])
  client = session.client('logs')

  for x in log_stream_names():
    #print(x)
    for y in log_event_messages(x):
      print(y)
except Exception as e:
  print(e)
