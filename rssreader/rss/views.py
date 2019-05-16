from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import FeedSerializer
from .models import Feed
import feedparser

@csrf_exempt
def rest_feeds(request):
    if request.method == "GET":
        feeds = Feed.objects.all()
        serializer = FeedSerializer(feeds, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = FeedSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def rest_feeds_detail(request, pk):
    try:
        feed = Feed.objects.get(pk=pk)
    except Feed.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        serializer = FeedSerializer(feed)
        return JsonResponse(serializer.data)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = FeedSerializer(feed, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=404)
    elif request.method == "DELETE":
        feed.delete()
        return HttpResponse()

def rest_items(request):
    feeds = Feed.objects.all()
    items = []

    for feed in feeds:
        rss = feedparser.parse(feed.url)

        try: 
            items.extend(rss["items"])
        except KeyError:
            continue

        items = list(reversed(sorted(items, key=lambda item: item["published_parse"])))

        return JsonResponse(items, safe=False)

def index(request):
   url = 'https://www.djangoproject.com/rss/weblog/'
   feed = feedparser.parse(url)
   if request.GET.get("url"):
       url = request.GET["url"]
       feed = feedparser.parse(url)
   else:
       feed = None

   return render(request, 'rss/reader.html')