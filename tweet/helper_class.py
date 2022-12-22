from collections import namedtuple
from decouple import Csv, config
import tweepy
from django.conf import settings


class TwitterAPI:
    def __init__(self):
        self.api_key = config('TWITTER_API_KEY')
        self.api_secret = config('TWITTER_API_SECRET')
        self.client_id = config('TWITTER_CLIENT_ID')
        self.client_secret = config('TWITTER_CLIENT_SECRET')
        self.oauth_callback_url = config('TWITTER_OAUTH_CALLBACK_URL')

    def perform_auth(self):
        OAuthInfo = namedtuple('OAuthInfo', ['oauth_url', 'oauth_token', 'oauth_token_secret'])
        oauth1_user_handler = tweepy.OAuthHandler(self.api_key, self.api_secret, callback=self.oauth_callback_url)
        url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)
        oauth_token = oauth1_user_handler.request_token["oauth_token"]
        oauth_token_secret = oauth1_user_handler.request_token["oauth_token_secret"]
        return OAuthInfo(url, oauth_token, oauth_token_secret)

    def get_access_token(self, oauth_verifier, oauth_token, oauth_token_secret):
        AccessToken = namedtuple('AccessToken', ['access_token', 'access_token_secret'])
        new_oauth1_user_handler = tweepy.OAuthHandler(self.api_key, self.api_secret, callback=self.oauth_callback_url)
        new_oauth1_user_handler.request_token = {
            'oauth_token': oauth_token,
            'oauth_token_secret': oauth_token_secret
        }
        access_token, access_token_secret = new_oauth1_user_handler.get_access_token(oauth_verifier)
        return AccessToken(access_token, access_token_secret)

    def get_me(self, access_token, access_token_secret):
        try:
            client = tweepy.Client(consumer_key=self.api_key, consumer_secret=self.api_secret,
                                   access_token=access_token, access_token_secret=access_token_secret)
            info = client.get_me(user_auth=True)
            return info.data
        except Exception as e:
            print(e)
            return None
