from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import FeedSerializer
from .models import Feed
import feedparser

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

def index(request):
   url = 'https://www.djangoproject.com/rss/weblog/'
   feed = feedparser.parse(url)
   if request.GET.get("url"):
       url = request.GET["url"]
       feed = feedparser.parse(url)
   else:
       feed = None

   return render(request, 'rss/reader.html', {
       'feed': feed
   })