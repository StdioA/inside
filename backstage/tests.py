import json
from io import BytesIO
from django.test import TestCase, Client
from django.contrib.auth.models import User
from mblog.models import Post, Comment


class BackStageTest(TestCase):
    fixtures = ["post.json", "comment.json"]

    def setUp(self):
        self.posts = list(Post.objects.all())
        self.client = Client()
        self.user = User.objects.create(username="user", is_superuser=True)

    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()

    def test_data_view(self):
        """
        Test accessbility for back-end
        """
        backstage_url = '/manage/data/'
        res = self.client.get(backstage_url)
        self.assertEqual(res.status_code, 404)

        self.client.force_login(self.user)
        res = self.client.get(backstage_url)
        self.assertEqual(res.status_code, 200)

    def test_post_import_export(self):
        self.client.force_login(self.user)

        # Export data
        export_url = '/manage/data/export/'
        res = self.client.get(export_url)
        self.assertEqual(res.status_code, 200)
        exported_data = list(res.streaming_content)[0]
        data = json.loads(exported_data)
        self.assertEqual(len(data["posts"]), len(self.posts))
        for post_obj, post_payload in zip(self.posts, data["posts"]):
            for field in ("id", "exist", "content"):
                self.assertEqual(getattr(post_obj, field), post_payload[field])

        # Import data
        import_url = '/manage/data/import/'
        # Error: no data file
        res = self.client.post(import_url)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.context["success"])
        self.assertEqual(res.context["message"], "Please Select data file.")
        # Error: wrong file format
        file = BytesIO(b'blahblahblah')
        res = self.client.post(import_url, {"data": file})
        self.assertFalse(res.context["success"])
        self.assertEqual(res.context["message"], "JSON parsing error")

        # Normal condition
        Post.objects.all().delete()
        Comment.objects.all().delete()
        file = BytesIO(exported_data)
        res = self.client.post(import_url, {"data": file})
        self.assertTrue(res.context["success"])
        self.assertEqual(res.context["message"],
                         "%d posts has been imported!" % len(self.posts))

        self.assertEqual(Post.objects.count(), len(self.posts))
        self.assertEqual(Comment.objects.count(), 2 * len(self.posts))
