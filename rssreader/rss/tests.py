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
        url = "https://www.djangoproject.com/rss/weblog/"
        Feed.objects.create(
            url=url
        )
        response = self.client.get(reverse('rest-feeds'))
        feed = response.json()[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(feed["url"], url)

    def test_update_feeds(self):
        url = "https://www.djangoproject.com/rss/weblog/"
        new_url = "https://utan.io/?feed=rss2"
        Feed.objects.create(
            url=url
        )
        json_data = json.dumps({
            "url":new_url
        })
        response = self.client(
            "/rss/feeds/1/",
            json_data,
            content_type = "application/json"
        )
        feeds = Feed.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            feeds,
            ["<Feed '{}'>".format(new_url)]
        )

    def test_delete_feeds(self):
        Feed.objects.create(
                url="https://www.djangoproject.com/rss/weblog/"
            )

        response = self.client.delete("/rss/feeds/1/")

        feeds = Feed.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            feeds,
            []
        )
    


class RssFeedModelTests(TestCase):
    def test_get_items(self):
        Feed.objects.create(
            url = "https://www.djangoproject.com/rss/weblog/"
        )
        response = self.client.get(reverse("rest-items"))
        self.assertEqual(response.status_code, 200)
        
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
