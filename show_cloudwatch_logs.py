# coding: UTF-8

import configparser
import json
from datetime import datetime
import boto3
from boto3.session import Session

config = configparser.ConfigParser()
config.read('config.ini')

session = Session(profile_name = config['AWS']['Profile'])
client = session.client('logs')

LAST_EVENT_TIMESTAMP = int(datetime.strptime('2020-01-01', "%Y-%m-%d").timestamp() * 1000)

def log_stream_names(token = None):
  if token == None:
    response = client.describe_log_streams(
      logGroupName = config['AWS']['LogGroupName'],
      orderBy = 'LastEventTime',
      limit = 10
    )
  else:
    response = client.describe_log_streams(
      logGroupName = config['AWS']['LogGroupName'],
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
      logGroupName = config['AWS']['LogGroupName'],
      logStreamName = log_stream_name,
      limit = 100
    )
  else:
    response = client.get_log_events(
      logGroupName = config['AWS']['LogGroupName'],
      logStreamName = log_stream_name,
      nextToken = token,
      limit = 100
    )

  for event in response.get('events'):
    yield event.get('message')

  if response.get('nextForwardToken').split('/')[1] != response.get('nextBackwardToken').split('/')[1]:
    yield from log_event_messages(log_stream_name, response.get('nextBackwardToken'))  

try:
  for x in log_stream_names():
    #print(x)
    for y in log_event_messages(x):
      print(y)
except Exception as e:
  print(e)
