"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from ribbit_app.models import Ribbit


class TestRibbit(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user',
                                             'testuser@ribbit.com', 'password1')
        self.ribbit = Ribbit.objects.create(content="Test Ribbit #1",
                                            user=self.user,
                                            creation_date=datetime.now())

    def test_home_page_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateNotUsed(response, 'buddies.html')

    def test_ribbit_created(self):
        self.assertEquals(self.ribbit.content, "Test Ribbit #1")

    def test_home_page_template_for_logged_in_user(self):
        self.assertTrue(self.client.login(username='test_user', password='password1'), True)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'buddies.html')

    def test_user_can_read(self):
        self.assertTrue(self.client.login(username='test_user', password='password1'), True)
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Test Ribbit #1")

    def test_user_profile(self):
        self.assertTrue(self.client.login(username="test_user", password='password1'), True)
        response = self.client.get("/users/test_user/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_user")