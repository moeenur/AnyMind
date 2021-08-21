from django.conf import settings
from utility.internal_api import ClientApi, InternalAPIResponseError
from http import HTTPStatus
from datetime import datetime
import requests
import logging

logger = logging.getLogger(__name__)


def parse_response(response):
    """
    Convert response from Twitter
    :param response:
    :return:
    """
    result = []
    if response and "data" in response:
        for data in response["data"]:
            user = next(filter(lambda usr: usr["id"] == data["author_id"],
                               response["includes"]["users"]), None) if "users" in response["includes"] else None
            account = dict()
            if user:
                account["fullname"] = user["name"]
                account["href"] = f"/{user['username']}"
                account["id"] = user["id"]
            item = dict()
            item["account"] = account
            parse_date = datetime.strptime(data['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
            item["date"] = parse_date.strftime("%H:%M %p - %d %b %Y")
            item["hashtags"] = list(map(lambda ht: f"#{ht['tag']}",
                                        data["entities"]["hashtags"])) if "hashtags" in data["entities"] else []
            item["likes"] = data["public_metrics"]["like_count"]
            item["replies"] = data["public_metrics"]["reply_count"]
            item["retweets"] = data["public_metrics"]["retweet_count"]
            item["text"] = data["text"]
            result.append(item)
    return result


class InternalService(ClientApi):
    """
    Search Tweets following Twitter API v2.
    https://developer.twitter.com/en/docs/twitter-api/tweets/search/quick-start/recent-search
    """
    page_limit = None

    def __init__(self):
        super(InternalService, self).__init__()
        self.endpoint_url = f"{settings.TW_API_HOST}/2/tweets/search/recent"
        self.query_params = self.make_response()

    def make_response(self):
        """specify fields that would like to retrieve"""
        params = {
            'tweet.fields': 'created_at,public_metrics,entities',
            'expansions': 'author_id',
            'user.fields': 'description'
        }
        return self.response_limit(params)

    def response_limit(self, params):
        if self.page_limit:
            params['max_results'] = self.page_limit
        return params

    def fetch_tweets_by_hashtag(self, query_txt):
        try:
            self.query_params['query'] = f"#{query_txt}"
            response = self.run(self.query_params)
            if response.status_code == HTTPStatus.OK:
                result = parse_response(response.json())
                return dict(status=HTTPStatus.OK, content=result)
        except (InternalAPIResponseError, requests.RequestException) as e:
            logger.error('[InternalService][fetch_tweets_by_hashtag] Error: {}'.format(e))
            err_msg = "whoops! failed to get the tweets due to Twitter API error"
            return dict(status=HTTPStatus.INTERNAL_SERVER_ERROR, content=err_msg)

    def fetch_tweets_by_user(self, query_txt):
        try:
            self.query_params['query'] = f"@{query_txt}"
            response = self.run(self.query_params)
            if response.status_code == HTTPStatus.OK:
                result = parse_response(response.json())
                return dict(status=HTTPStatus.OK, content=result)
        except (InternalAPIResponseError, requests.RequestException) as e:
            logger.error('[InternalService][fetch_tweets_by_user] Error: {}'.format(e))
            err_msg = "whoops! failed to get the tweets due to Twitter API error"
            return dict(status=HTTPStatus.INTERNAL_SERVER_ERROR, content=err_msg)
