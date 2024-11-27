"""
Views for the 'search' application.

This module contains the views that handle the search-related functionality for the 'search' app in the application.

Functions:
    - `intializeDB`: Initializes the connection to the MongoDB database and sets up global variables for collections.
    - `search_index`: Handles the logic for searching available rides, checking if routes are still available, and rendering the search results page.

Dependencies:
    - `get_client`: Utility function for establishing a MongoDB client connection.
    - `DateUtils.has_date_passed`: Utility function to check if a route's date has passed.
    - `Secrets`: Configuration class that stores secret keys like the Google Maps API key.
    - `RideForm`: Form used for creating a ride (though not directly used in this snippet).
    - `UserCreationForm`: Django form for user registration (though not directly used here).
    - `messages`: Django's messaging framework for providing feedback to users.
"""

from http.client import HTTPResponse
from django.shortcuts import render, redirect
# from numpy import True_, dtype
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from utilities import DateUtils

from publish.forms import RideForm
from utils import get_client
from config import Secrets

client = None
db = None
userDB = None
ridesDB = None
routesDB = None
secrets = Secrets()


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
    global client, db, userDB, ridesDB, routesDB
    client = get_client()
    db = client.SEProject
    userDB = db.userData
    ridesDB = db.rides
    routesDB = db.routes


def search_index(request):
    """
    Handles the search functionality for available rides.

    This view retrieves all available rides from the database, processes them to count the number of active routes
    (routes with dates that have not passed), and displays the search results on the 'search.html' template.
    If the user is not logged in, they will be redirected to the login page with a message.

    Args:
        request (HttpRequest): The request object containing session and user data.

    Returns:
        HttpResponse: The rendered response for the search page, including a list of rides and relevant data.
    """
    intializeDB()
    if not request.session.has_key('username'):
        request.session['alert'] = "Please login to create a ride."
        messages.info(request, "Please login to search a ride!")
        return redirect('index')
    all_rides = list(ridesDB.find())
    processed, routes = list(), list()
    for ride in all_rides:
        route_count = 0
        routes = ride['route_id']
        for route in routes:
            route_date = route.split("_")[3]
            if not DateUtils.has_date_passed(route_date):
                route_count += 1
        ride['id'] = ride.pop('_id')
        ride['count'] = route_count
        processed.append(ride)
    return render(request, 'search/search.html', {"username": request.session['username'], "rides": processed, "gmap_api_key": secrets.GoogleMapsAPIKey})
