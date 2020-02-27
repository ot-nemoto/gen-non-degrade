# coding: UTF-8

import argparse
import configparser
import json
from datetime import datetime
from pytz import timezone
import boto3
from boto3.session import Session

# ======================================
# constant
# ======================================
EVENT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

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

########################################
# log_stream_names
########################################
def log_stream_names(token = None):
  if token == None:
    response = client.describe_log_streams(
      logGroupName = config[args.section]['LogGroupName'],
      orderBy = 'LastEventTime',
      limit = 50
    )
  else:
    response = client.describe_log_streams(
      logGroupName = config[args.section]['LogGroupName'],
      orderBy = 'LastEventTime',
      nextToken = token,
      limit = 50
    )

  for log_stream in response.get('logStreams'):
    if log_stream.get('lastEventTimestamp') >= firstEventTimestamp and log_stream.get('firstEventTimestamp') <= lastEventTimestamp:
      yield log_stream.get('logStreamName')
  if response.get('nextToken') is not None:
    yield from log_stream_names(response.get('nextToken'))

########################################
# log_event_messages
########################################
def log_event_messages(log_stream_name, token = None):
  if token == None:
    response = client.get_log_events(
      logGroupName = config[args.section]['LogGroupName'],
      logStreamName = log_stream_name,
      startTime = firstEventTimestamp,
      endTime = lastEventTimestamp,
      limit = 10000
    )
  else:
    response = client.get_log_events(
      logGroupName = config[args.section]['LogGroupName'],
      logStreamName = log_stream_name,
      startTime = firstEventTimestamp,
      endTime = lastEventTimestamp,
      nextToken = token,
      limit = 10000
    )

  for event in response.get('events'):
    yield event.get('message')

  print("=============================================")
  if response.get('nextForwardToken').split('/')[1] != response.get('nextBackwardToken').split('/')[1]:
    yield from log_event_messages(log_stream_name, response.get('nextBackwardToken'))  

########################################
# main
########################################
try:
  session = Session(profile_name = config[args.section]['Profile'])
  client = session.client('logs')

  # EventTimestamp range
  firstEventTimestamp = int(
    timezone(config[args.section].get('TimeZone')).localize(
      datetime.strptime(
        config[args.section].get('FirstEventTime') or '1970-01-01 00:00:00', EVENT_TIME_FORMAT)).timestamp() * 1000)
  lastEventTimestamp = int(
    timezone(config[args.section].get('TimeZone')).localize(
      datetime.strptime(
        config[args.section].get('LastEventTime') or '2999-12-31 23:59:59', EVENT_TIME_FORMAT)).timestamp() * 1000)

  for log_stream_name in log_stream_names():
    #print(log_stream_name)
    for log_event_message in log_event_messages(x):
      print(log_event_message)
except Exception as e:
  print(e, file=sys.stderr)
