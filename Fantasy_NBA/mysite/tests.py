from django.test import TestCase, Client
from django.urls import reverse
from .models import Thread, Post
from django.contrib.auth.models import User

class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.thread_list_url = reverse('thread_list')
        self.create_thread_url = reverse('create_thread')
        self.user = User.objects.create_user(username='testuser', password='password')
        self.thread = Thread.objects.create(title='Test Thread', creator=self.user)
        self.post = Post.objects.create(thread=self.thread, author=self.user, content='Test Post Content')

    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, 'mysite/home.html')

    def test_thread_list_view(self):
        response = self.client.get(self.thread_list_url)
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, 'mysite/thread_list.html')

    def test_create_thread_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.create_thread_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mysite/create_thread.html')

    def test_thread_detail_view(self):
        thread_detail_url = reverse('thread_detail', kwargs={'pk': self.thread.pk})
        response = self.client.get(thread_detail_url)
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, 'mysite/thread_detail.html')
