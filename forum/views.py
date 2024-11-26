from django.shortcuts import render
from django.shortcuts import render, redirect
from utils import get_client
from config import Secrets
from bson.objectid import ObjectId
from django.forms.utils import ErrorList
from utilities import DateUtils
from django.contrib.auth.hashers import make_password, check_password

from bson import ObjectId
from datetime import datetime

client = None
db = None
userDB = None
ridesDB = None
routesDB = None
secrets = None
topicsDB = None
commentsDB = None

# Create your views here.


def intializeDB():
    """
    Initializes the connection to the MongoDB database and sets up global variables for collections.

    - `client`: The MongoDB client instance.
    - `db`: The database object, specifically the "SEProject" database.
    - `userDB`: The collection for storing user data within the "SEProject" database.
    - `ridesDB`: The collection for storing ride information within the "SEProject" database.
    - `routesDB`: The collection for storing route information within the "SEProject" database.

    Globals:
        client (MongoClient): The MongoDB client instance.
        db (Database): The "SEProject" database object.
        userDB (Collection): The collection for user data.
        ridesDB (Collection): The collection for ride data.
        routesDB (Collection): The collection for route data.

    Returns:
        None
    """
    global client, db, userDB, ridesDB, routesDB, topicsDB, commentsDB
    client = get_client()
    db = client.SEProject
    userDB = db.userData
    ridesDB = db.rides
    routesDB = db.routes
    topicsDB = db.topics
    commentsDB = db.comments


def rides_with_topics(request):
    """
    Displays all rides and their associated topics.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The page listing all rides with links to their topics.
    """
    intializeDB()
    rides = list(routesDB.find())  # Fetch all rides
    rides_with_topics = []
    visitedDest = set()
    for ride in rides:
        if ride['destination'] not in visitedDest:
            visitedDest.add(ride['destination'])
            # Fetch topics related to the ride
            topics = list(topicsDB.find({"ride_id": ride['destination']}))
            for topic in topics:
                topic['id'] = topic.pop('_id')
            rides_with_topics.append({'ride': ride, 'topics': topics})

    return render(request, 'forum/rides_with_topics.html', {'rides_with_topics': rides_with_topics})


def create_topic(request):
    """
    Handles the creation of a discussion topic for a ride.
    """
    intializeDB()
    rides = list(routesDB.find())  # Fetch all rides for selection
    final_rides = []
    visitedDest = set()
    for ride in rides:
        ride['id'] = ride.pop('_id')
        if ride['destination'] not in visitedDest:
            final_rides.append(ride)
            visitedDest.add(ride['destination'])
    if request.method == "POST":
        ride_id = request.POST.get("ride_id")
        title = request.POST.get("title")
        content = request.POST.get("content")
        user = request.session.get("username")

        if not (ride_id and title and content and user):
            return render(request, "forum/create_topic.html", {"error": "All fields are required!"})

        topic = {
            "ride_id": ride_id,
            "title": title,
            "content": content,
            "creator": user,
            "created_at": datetime.now(),
        }
        topicsDB.insert_one(topic)
        return redirect("rides_with_topics")

    return render(request, "forum/create_topic.html", {"rides": final_rides})


def add_comment(request, topic_id):
    """
    Adds a comment to a specific topic.
    """
    intializeDB()
    if request.method == "POST":
        content = request.POST.get("content")
        user = request.session.get("username")

        comment = {
            "topic_id": ObjectId(topic_id),
            "content": content,
            "creator": user,
            "created_at": datetime.now(),
        }
        commentsDB.insert_one(comment)
        return redirect("forum_topic_details", topic_id=topic_id)
    return redirect("forum_topic_details", topic_id=topic_id)


def forum_topics(request, ride_id):
    """
    Displays all topics related to a specific ride.
    """
    intializeDB()
    topics = list(topicsDB.find({"ride_id": ride_id}))
    for topic in topics:
        topic['id'] = topic.pop('_id')
    return render(request, "forum/topics.html", {"topics": topics, "ride_id": ride_id})


def forum_topic_details(request, topic_id):
    """
    Displays a specific topic and its associated comments.
    """
    intializeDB()
    topic = topicsDB.find_one({"_id": ObjectId(topic_id)})
    topic['id'] = topic.pop('_id')
    comments = list(commentsDB.find({"topic_id": ObjectId(topic_id)}))
    return render(request, "forum/topic_details.html", {"topic": topic, "comments": comments})
