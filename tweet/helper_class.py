'''
helper class for working with twitter oauth API using tweepy
'''

from collections import namedtuple
import os
import tweepy
from django.conf import settings


class TwitterAPI:
    '''
    initialize api key by pulling values from environment variables
    '''

    def __init__(self):
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.client_id = os.getenv('TWITTER_CLIENT_ID')
        self.client_secret = os.getenv('TWITTER_CLIENT_SECRET')
        self.oauth_callback_url = os.getenv('TWITTER_OAUTH_CALLBACK_URL')

    def perform_auth(self):
        '''
        function to obtain OAuth URL, OAuth token and OAuth token_secret
        '''
        # make return value more object oriented using namedtuple
        OAuthInfo = namedtuple(
            'OAuthInfo', ['oauth_url', 'oauth_token', 'oauth_token_secret'])
        # initialize ouath handler
        oauth1_user_handler = tweepy.OAuthHandler(
            self.api_key, self.api_secret, callback=self.oauth_callback_url)
        # generate oauth authorization url
        url = oauth1_user_handler.get_authorization_url(
            signin_with_twitter=True)
        # obtain oauth token and oauth token secret
        oauth_token = oauth1_user_handler.request_token["oauth_token"]
        oauth_token_secret = oauth1_user_handler.request_token["oauth_token_secret"]
        # return oauth response
        return OAuthInfo(url, oauth_token, oauth_token_secret)

    def get_access_token(self, oauth_verifier, oauth_token, oauth_token_secret):
        '''
        function to generate access token pair using returned auth token from `perform_auth` function
        '''
        # make return value more object oriented using namedtuple
        AccessToken = namedtuple(
            'AccessToken', ['access_token', 'access_token_secret'])
        # generate access token using saved oauth token
        new_oauth1_user_handler = tweepy.OAuthHandler(
            self.api_key, self.api_secret, callback=self.oauth_callback_url)
        new_oauth1_user_handler.request_token = {
            'oauth_token': oauth_token,
            'oauth_token_secret': oauth_token_secret
        }
        access_token, access_token_secret = new_oauth1_user_handler.get_access_token(
            oauth_verifier)
        # return authenticated user access token and access token secret
        return AccessToken(access_token, access_token_secret)

    def get_me(self, access_token, access_token_secret):
        '''
        fetch authenticated user  information
        '''
        try:
            # initialize new api client using authenticated user access token and access token secret
            client = tweepy.Client(consumer_key=self.api_key, consumer_secret=self.api_secret,
                                   access_token=access_token, access_token_secret=access_token_secret)
            api = client.get_me(user_auth=True)
            return api.data
        except Exception as e:
            print(e)
            return None
