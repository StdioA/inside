from django.test import TestCase, Client
from django.contrib.auth.models import User
from mblog.models import Post


class MBlogAppTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            "admin", "email", "password")
        self.user = User.objects.create_user(
            "user", "email", "password")
        self.client = Client()

    def tearDown(self):
        User.objects.all().delete()

    def login(self, user=None):
        user = user or self.admin
        self.client.force_login(user)

    def test_login_logout(self):
        next_url = "/some_next"
        login_url = "/login/?next={}".format(next_url)
        logout_url = "/logout/"

        res = self.client.get(login_url)
        self.assertEqual(res.status_code, 200)

        # Login failed
        res = self.client.post(login_url, {
            "username": self.user.username,
            "password": "wrong"
        })
        self.assertIn("Invalid", res.context["error"])

        # Login successfully
        res = self.client.post(login_url, {
            "username": self.user.username,
            "password": "password"
        })
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, next_url)
        self.assertEqual(self.client.session["_auth_user_id"],
                         str(self.user.id))

        # Logout
        res = self.client.get(logout_url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, "/")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_archive_page(self):
        """
        Test accessibility
        """
        url = "/archive/"
        # Not login
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)
        self.assertIn("login", res.url)

        # Login
        self.login()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_index_page(self):
        url = "/"
        self.login()
        # Returns 404 if no post exists
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)

        # Redirect to latest post page
        for i in range(1, 5):
            post = Post.objects.create(content="Content {}".format(i))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, "/{}".format(post.id))

    def test_create_post(self):
        url = "/0"
        self.login()

        # Get view
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

        # Create post
        content = "Test content"
        res = self.client.post(url, {"content": content})
        self.assertEqual(res.status_code, 302)
        post = Post.objects.last()
        self.assertEqual(post.content, content)
        self.assertEqual(res.url, "/{}".format(post.id))

    def test_view_post(self):
        post = Post.objects.create(content="hhhhhh")
        url = "/{}".format(post.id)
        # Normal user will visit a static page
        self.login(self.user)
        res = self.client.get(url)
        self.assertIsNone(res.context)

        # Admin will visit a dynamic page
        self.login(self.admin)
        res = self.client.get(url)
        self.assertEqual(res.context["post"], post)
        self.assertEqual(res.context["previous"], 0)    # no post before
        self.assertEqual(res.context["next"], 0)
