from django.views import generic
from django.http import JsonResponse
from django.conf import settings
from http import HTTPStatus
from twitter.internal_service import InternalService
import logging

logger = logging.getLogger(__name__)


class HashtagTweet(generic.View):

    def get(self, request, hashtag):
        try:
            InternalService.page_limit = self.request.GET.get('limit', settings.TWEETS_LIMIT)
            list_tweets = InternalService().fetch_tweets_by_hashtag(hashtag)
            response_data = list_tweets['content']
            response_status = list_tweets['status']
        except Exception as e:
            err_msg = e.message if hasattr(e, 'message') else str(e)
            logger.error('[HashtagTweet] Error: {}'.format(err_msg))
            response_data = "Something went wrong! Please try again later."
            response_status = HTTPStatus.INTERNAL_SERVER_ERROR
        return JsonResponse(response_data, status=response_status, json_dumps_params={'indent': 2}, safe=False)


class UserTweet(generic.View):

    def get(self, request, user):
        try:
            InternalService.page_limit = self.request.GET.get('limit', settings.TWEETS_LIMIT)
            list_tweets = InternalService().fetch_tweets_by_user(user)
            response_data = list_tweets['content']
            response_status = list_tweets['status']
        except Exception as e:
            err_msg = e.message if hasattr(e, 'message') else str(e)
            logger.error('[UserTweet] Error: {}'.format(err_msg))
            response_data = "Something went wrong! Please try again later."
            response_status = HTTPStatus.INTERNAL_SERVER_ERROR
        return JsonResponse(response_data, status=response_status, json_dumps_params={'indent': 2}, safe=False)
