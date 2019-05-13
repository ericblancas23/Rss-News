from django.test import TestCase
from django.urls import reverse
from rss.models import Feed
import json
# Create your tests here.
class RssRestFeedsViewTests(TestCase):
    def test_create_feed(self):
        url = "https://www.djangoproject.com/rss/weblog/"
        json_data = json.dumps({ "url":url })

        response = self.client.post(
            reverse("rest-feeds"),
            json_data,
            content_type="application/json"
        )

        feeds = Feed.objects.all()

        self.assertEqual(response.status_code, 201)
        self.assertQuerysetEqual(
            feeds,
            ["<Feed '{}'>".format(url)]
        )

    def test_get_feeds(self):
        pass

    def test_update_feeds(self):
        pass
        
    def test_delete_feeds(self):
        pass
    


class RssFeedModelTests(TestCase):
    def setUp(self):
        Feed.objects.create(
            url="https://www.djangoproject.com/rss/weblog/"
        )
    def test_model_has_url(self):
        django_feed = Feed.objects.get(
            url="https://www.djangoproject.com/rss/weblog/"
        )
        self.assertEqual(
            django_feed.url,
            "https://www.djangoproject.com/rss/weblog/"
        )
class RssIndexViewTests(TestCase):
    def test_no_feed(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["feed"], None)
    
    def test_user_feed(self):
        response = self.client.get(reverse("index") + "?url=https://www.djangoproject.com/rss/weblog/")

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context["feed"], None)
