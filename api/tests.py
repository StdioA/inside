import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from mblog.models import Post, Comment


class APITest(TestCase):
    fixtures = ["post.json", "comment.json"]

    def setUp(self):
        self.admin = User.objects.create_superuser(
            "admin", "email", "password")
        self.user = User.objects.create_user(
            "user", "email", "password")
        self.client = Client()
        self.login()

    def tearDown(self):
        User.objects.all().delete()

    def login(self, user=None):
        user = user or self.admin
        self.client.force_login(user)

    def test_archive_api(self):
        posts = list(Post.objects.all().order_by("-id"))
        url_temp = "/api/archive/"

        ipp = 2
        # Page 1
        url = url_temp + "counts/{}/".format(ipp)
        res = self.client.get(url)
        data = json.loads(res.content)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["posts"]), ipp)
        posts = Post.objects.order_by('-id')[:ipp]
        for post_obj, post in zip(posts, data["posts"]):
            self.assertEqual(post_obj.id, post["id"])
            self.assertEqual(post_obj.content, post["content"])

        # Page 2
        ipp = 3
        last_pid = data["posts"][-1]["id"]
        url = url_temp + "{}/counts/{}/".format(last_pid, ipp)
        res = self.client.get(url)
        data = json.loads(res.content)
        self.assertEqual(len(data["posts"]), ipp)
        posts = Post.objects.filter(id__lte=last_pid).order_by('-id')[:ipp]
        for post_obj, post in zip(posts, data["posts"]):
            self.assertEqual(post_obj.id, post["id"])
            self.assertEqual(post_obj.content, post["content"])

        # Exist filter
        Post.objects.update(exist=False)
        url = url_temp + "counts/2/"
        res = self.client.get(url)
        data = json.loads(res.content)
        self.assertEqual(len(data["posts"]), 0)

    def test_comment_api(self):
        post = Post.objects.first()
        url = "/api/comment/{}/".format(post.id)
        res = self.client.get(url)
        data = json.loads(res.content)
        self.assertEqual(len(data["comments"]), 2)
        for cmt, cmt_obj in zip(data["comments"], post.comment_set.all()):
            self.assertEqual(cmt["content"], cmt_obj.content)
            self.assertEqual(cmt["author"], cmt_obj.author)

        # Create comment
        res = self.client.post(url, {"author": "author", "content": "content"})
        data = json.loads(res.content)
        self.assertTrue(data["success"])
        comment = Comment.objects.filter(post=post).last()
        self.assertEqual(comment.author, "author")
        self.assertEqual(comment.content, "content")

        res = self.client.get(url)
        data = json.loads(res.content)
        self.assertEqual(len(data["comments"]), 3)

        # Post not found
        not_found_url = "/api/comment/{}/".format(post.id + 10086)
        res = self.client.get(not_found_url)
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.content)
        self.assertFalse(data["success"])

    def test_view_post_api(self):
        post = Post.objects.all()[4]
        url = "/api/post/{}/".format(post.id)
        res = self.client.get(url)
        data = json.loads(res.content)
        self.assertTrue(data["success"])
        self.assertEqual(data["post"]["content"], post.content)
        self.assertEqual(len(data["post"]["comments"]), 2)
        self.assertEqual(data["previous_id"], post.id - 1)
        self.assertEqual(data["next_id"], post.id + 1)

        # Post not found
        url = "/api/post/404/"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)

    def test_modify_post_api(self):
        pass
