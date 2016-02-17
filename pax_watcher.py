#!/bin/env python
# Made by Taylor McClure

# imports
from bs4 import BeautifulSoup
import requests
import boto3
from boto3.session import Session
import sys

# vars
SITE = 'http://prime.paxsite.com/registration'
S3_BUCKET = ''
OLD_DIV_LOC = 'key prefix in your bucket'
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
REGION_NAME = ''
TOPIC_ARN = 'SNS topicARN'
HTML_ID = 'badgeAvailability'
SNS_MESSAGE = 'type your custom message here'
SNS_SUBJECT = 'type your custom subject here'

def my_handler(event, context):
    # boto3 connection
    session = Session(aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION_NAME)

    def s3_get():
        # establish s3 client connection
        s3 = session.client('s3')

        # s3 get old_div and store as string
        response = s3.get_object(Bucket=s3_bucket,
        Key=OLD_LOC)

        OLD_DIV = response['Body'].read()

        return OLD_DIV

    def live_site():
        # response from live site
        response_live = requests.get(SITE)

        # gather pax registration page
        soup = BeautifulSoup(response_live.text, "html.parser")

        # parse for interesting div
        NEW_DIV = soup.find(id=HTML_ID).encode('utf-8')

        return NEW_DIV

    def sns_alert():
        # establish a connection to sns client
        sns = session.client('sns')

        # push a message if it has been changed
        PUBLISH_SNS = sns.publish(TopicArn=TOPIC_ARN,
            Message= SNS_MESSAGE,
            Subject=SNS_SUBJECT)

        return PUBLISH_SNS

    # to check if different
    if len(live_site()) == len(s3_get()):
        message = 'This has executed successfully, no changes found'
    else:
        sns_alert()
	message= 'SOMETHING CHANGED!!!'

    return message
