from django.test import TestCase
from django.conf import settings
from http import HTTPStatus


class HashtagTweetView(TestCase):
    def test_url_exists_at_desired_location(self):
        response = self.client.get('/hashtags/sony')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tweets_default_limit(self):
        response = self.client.get('/hashtags/sony')
        self.assertEqual(len(response.json()), settings.TWEETS_LIMIT)

    def test_tweets_limit(self):
        limit = 10
        response = self.client.get('/hashtags/sony', data={
            'limit': limit
        })
        self.assertEqual(len(response.json()), limit)

    def test_special_character_hastag(self):
        response = self.client.get('/hashtags/%@!#*(')
        self.assertNotEqual(response.status_code, HTTPStatus.OK)

    def test_twitter_api_result_limit_range(self):
        min_response = self.client.get('/hashtags/sony', data=dict(limit=9))
        self.assertTrue(min_response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR)
        max_response = self.client.get('/hashtags/sony', data=dict(limit=101))
        self.assertTrue(max_response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR)


class UserTweetView(TestCase):
    def test_url_exists_at_desired_location(self):
        response = self.client.get('/users/khan')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tweets_default_limit(self):
        response = self.client.get('/users/khan')
        self.assertEqual(len(response.json()), settings.TWEETS_LIMIT)

    def test_tweets_limit(self):
        limit = 10
        response = self.client.get('/users/khan', data={
            'limit': limit
        })
        self.assertEqual(len(response.json()), limit)

    def test_special_character_hastag(self):
        response = self.client.get('/users/%@!#*(')
        self.assertNotEqual(response.status_code, HTTPStatus.OK)

    def test_twitter_api_result_limit_range(self):
        min_response = self.client.get('/users/khan', data=dict(limit=9))
        self.assertTrue(min_response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR)
        max_response = self.client.get('/users/khan', data=dict(limit=101))
        self.assertTrue(max_response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR)
