#!/bin/env python
# Made by Taylor McClure

# imports
from bs4 import BeautifulSoup
import requests
import boto3
from boto3.session import Session
import sys

# vars
pax_site = 'http://prime.paxsite.com/registration'
s3_bucket = ''
old_div_loc = ''
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
REGION_NAME = 'us-west-2'
TOPIC_ARN = ''

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
        Key=old_div_loc)
        
        old_div = response['Body'].read()

        return old_div

    def pax_live():
        # response from live site
        response_live = requests.get(pax_site)

        # gather pax registration page
        soup = BeautifulSoup(response_live.text, "html.parser")

        # parse for interesting div
        new_div = soup.find(id='badgeAvailability').encode('utf-8')

        return new_div

    def sns_alert():
        # establish a connection to sns client
        sns = session.client('sns')

        # push a message if it has been changed
        publish_sns = sns.publish(TopicArn=TOPIC_ARN,
            Message='This automated message has been sent in response to Taylor\'s Lambda Function detecting a change in the PAX Prime ticket page \n\nProceed to http://prime.paxsite.com/registration to get your tickets. \n\nYou better hurry, these tickets sold out for Sat + Sun in 3 hours after being on sale.',
            Subject='HOLY CRAP GO GET PAX TICKETS!!!')

        return publish_sns

    # to check if different
    if len(pax_live()) == len(s3_get()):
        message = 'This has executed successfully, no changes found'
    else:
        sns_alert()
	message= 'HOLY CRAP GO BUY TICKETS!!!'

    return message
