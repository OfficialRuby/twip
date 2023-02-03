from django.shortcuts import render, redirect
from django.views.generic import View
from tweet.helper_class import TwitterAPI
from django.contrib import messages
from tweet.models import AuthToken, UserToken


class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {

        }

        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        twitter_api_obj = TwitterAPI()
        authorize = twitter_api_obj.perform_auth()
        AuthToken.objects.create(
            auth_token=authorize.oauth_token, auth_token_secret=authorize.oauth_token_secret)
        return redirect(authorize.oauth_url)


class CallbackView(View):
    def get(self, request, *args, **kwargs):
        denied = request.GET.get('denied')
        oauth_token = request.GET.get('oauth_token')
        oauth_verifier = request.GET.get('oauth_verifier')
        if denied:
            messages.warning(request, 'Please authorize app to continue')
            return redirect('home')
        elif oauth_token and oauth_verifier:
            twitter_api_obj = TwitterAPI()
            auth = AuthToken.objects.filter(auth_token=oauth_token).first()

            access_token, access_secret = twitter_api_obj.get_access_token(
                oauth_verifier, auth.auth_token, auth.auth_token_secret)
            UserToken.objects.get_or_create(access_token=access_token,
                                            access_token_secret=access_secret)
            # You can perform any action on behalf of the authenticated using
            # `access_token` and `access_token_secret` provided above
            # Your mongo db logics can go on here
            # You can also construct a tweepy api object using  the `create_api_object`
            # method from the `TwitterAPI` class in the helper_class.py as seen below
            # api=twitter_api_obj.create_api_object(access_token, access_secret)
            # see `https://docs.tweepy.org/en/stable/getting_started.html#hello-tweepy`
            '''
            Let mongoDB code goes here
            below is an example
            '''
            # api = twitter_api_obj.create_api_object(
            #     access_token, access_secret)
            # timeline = api.home_timeline()
            # with open('response.txt', 'w') as f:
            #     for tweet in timeline:
            #         f.write(str(tweet))

            messages.success(
                request, 'You have successfully authorized this app')
            return redirect('home')
        return redirect('home')
