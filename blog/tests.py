from django.test import TestCase
from blog.models import Blog
from django.contrib.auth.models import User
from django.shortcuts import reverse


class BlogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='ali')
        self.blog = Blog.objects.create(
            title='title of blog',
            text='this is a text here',
            status=Blog.STATUS_CHOICES[0][0],
            author=self.user,

        )
        self.blog2 = Blog.objects.create(
            title='title2 of blog',
            text='this is a text2 here',
            status=Blog.STATUS_CHOICES[1][0],
            author=self.user,
        )

    def test_post(self):
        resource = self.client.get('/blog/')
        self.assertEqual(resource.status_code, 200)

    def test_post_by_name(self):
        resource = self.client.get(reverse('home'))
        self.assertEqual(resource.status_code, 200)

    def test_title_on_blog_page(self):
        response = self.client.get(reverse('home'))
        # self.assertContains(response, 'title of blog')
        # or
        self.assertContains(response, self.blog.title)

    def test_text_on_blog_page(self):
        response = self.client.get(reverse('home'))
        # self.assertContains(response, 'this is a text here')
        # or
        self.assertContains(response, self.blog.text)

    def test_post_detail_by_url(self):
        response = self.client.get(f'/blog/{self.blog.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_by_name(self):
        response = self.client.get(reverse('detail', args=[self.blog.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_on_detail_page(self):
        response = self.client.get(reverse('detail', args=[self.blog.id]))
        self.assertContains(response, self.blog.text)
        self.assertContains(response, self.blog.title)

    def test_status_on_detail_page(self):
        response = self.client.get(reverse('detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_on_page(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.blog.title)
        self.assertNotContains(response, self.blog2.title)

    def test_post_model_str(self):
        self.assertEqual(str(self.blog), self.blog.title)
        self.assertEqual(str(self.blog2), self.blog2.title)

    def test_detail_of_posts(self):
        post = self.blog
        self.assertEqual(post.title, 'title of blog')
        self.assertEqual(post.text, 'this is a text here')
        self.assertEqual(post.status, 'pub')
        self.assertEqual(post.author, self.user)

    def test_create_post(self):
        response = self.client.post(reverse('create_post'), {
            'title': 'title',
            'text': 'text??????????',
            'status': 'pub',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.last().title, 'title')
        self.assertEqual(Blog.objects.last().text, 'text??????????')
        self.assertEqual(Blog.objects.last().status, 'pub')
        self.assertEqual(Blog.objects.last().author, self.user)

    def test_update_post(self):
        response = self.client.post(reverse('edit_post', args=[self.blog2.id]),{
            'title': 'title2 of blog updated',
            'text': 'this is a text2 here is updated',
            'status': 'pub',
            'author': self.blog2.author.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Blog.objects.last().title, 'title2 of blog updated')
        self.assertEqual(Blog.objects.last().text, 'this is a text2 here is updated')





    def test_delete_post(self):
        response = self.client.post(reverse('delete_post', args=[self.blog.id]))
        self.assertEqual(response.status_code, 302)
