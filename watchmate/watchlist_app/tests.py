from urllib import response
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models


# Create your tests here.
class StreamPlatformTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='example', password='191027sm')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(
            name='Netflix', about='netflix about', website='https://www.netflix.com')

    def test_streamplatform_create(self):
        data = {
            'name': 'Netflix',
            'about': 'netflix',
            'website': 'http://www.netflix.com'
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(
            reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='example', password='191027sm')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(
            name='Netflix', about='netflix about', website='https://www.netflix.com')

        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title='movie 1',
            storyline='story 1',
            active=True
        )

    def test_watchlist_create(self):
        data = {
            'platform': self.stream,
            'title': 'Movie 1',
            'storyline': 'Story 1',
            'active': True
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_element(self):
        response = self.client.get(
            reverse('movie-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title, 'movie 1')
        self.assertEqual(models.WatchList.objects.count(), 1)


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='example', password='191027sm')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(
            name='Netflix', about='netflix about', website='https://www.netflix.com')

        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title='movie 1',
            storyline='story 1',
            active=True
        )

        self.watchlist2 = models.WatchList.objects.create(
            platform=self.stream,
            title='movie 2',
            storyline='story 2',
            active=True
        )

        self.review = models.Review.objects.create(
            review_user=self.user,
            rating=5,
            description='Greate movie',
            watchlist=self.watchlist2,
            active=True
        )

    def test_review_create(self):
        data = {
            'review_user': self.user,
            'rating': 5,
            'description': 'movie 2',
            'watchlist': self.watchlist,
            'active': True
        }
        response = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.WatchList.objects.count(), 2)

        # The same user can't create more than 1 review for the same watchlist
        response = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            'review_user': self.user,
            'rating': 5,
            'description': 'movie 2',
            'watchlist': self.watchlist,
            'active': True
        }
        # Test for not authenticated user
        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            'review_user': self.user,
            'rating': 4,
            'description': 'movieeeee 2',
            'watchlist': self.watchlist,
            'active': False
        }
        response = self.client.put(
            reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(
            reverse('review-list', args=(self.watchlist.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_element(self):
        response = self.client.get(
            reverse('review-detail', args=(self.review.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TODO: Add delete request

    def test_review_user(self):
        response = self.client.get(
            '/watch/reviews/?username' + self.user.username
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
