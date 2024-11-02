from http.client import HTTPResponse
from django.shortcuts import render,redirect
from numpy import True_, dtype
import requests
import json
from datetime import datetime
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from services import MapsService
from config import Secrets, URLConfig
from utilities import DateUtils

from publish.forms import RideForm
from utils import get_client
# from django.http import HttpResponse

# Create your views here.
client = None
db = None
userDB = None
ridesDB  = None
routesDB  = None
mapsService = None

secrets = Secrets()
urlConfig = URLConfig()



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
    ridesDB  = db.rides
    routesDB  = db.routes

def initializeService():
    """
    Initializes the MapsService instance and sets it as a global variable.

    This function creates an instance of the `MapsService` class using the 
    provided `RoutesHostname` from `urlConfig` and the `GoogleMapsAPIKey` from 
    `secrets`. It then assigns this instance to the global variable `mapsService`.

    Globals:
        mapsService (MapsService): An instance of the MapsService class that is 
                                   initialized with routing and API key configurations.

    Dependencies:
        - `urlConfig.RoutesHostname`: The hostname for route services.
        - `secrets.GoogleMapsAPIKey`: The API key for accessing Google Maps services.

    Returns:
        None
    """
    global mapsService
    mapsService = MapsService(urlConfig.RoutesHostname, secrets.GoogleMapsAPIKey)

def publish_index(request):
    """
    Handles the logic for rendering the ride publishing page and ensuring user authentication.

    This function performs the following steps:

    Args:
        request (HttpRequest): The HTTP request object containing session data and other 
                               request information.

    Returns:
        HttpResponse: A redirect to the 'index' page if the user is not logged in, or a rendered 
                      response of the 'publish/publish.html' template with context data if the 
                      user is authenticated.
    """
    intializeDB()
    if not request.session.has_key('username'):
        request.session['alert'] = "Please login to create a ride."
        return redirect('index')
    return render(request, 'publish/publish.html', {"username": request.session['username'], "alert":True, "gmap_api_key": secrets.GoogleMapsAPIKey})

def display_ride(request, ride_id):
    """
    Displays the ride details and associated routes for a given ride ID.

    Args:
        request (HttpRequest): The HTTP request object containing session data and other 
                               request information.
        ride_id (str): The unique identifier of the ride to be displayed.

    Returns:
        HttpResponse: A rendered response of the 'publish/route.html' template with 
                      context data including ride details, routes, and selected route.
    """
    intializeDB()
    print("Ride id", ride_id)
    ride = ridesDB.find_one({'_id': ride_id})
    # print(f"Ride = {ride}")
    routes = get_routes(ride)
    print(f"Route = {routes}")
    selected = routeSelect(request.session.get('username', None), routes)
    # print(f"Routes = {selected}")
    context = {
            "username": request.session.get('username', None),
            "ride": ride,
            "routes": routes,
            "selectedRoute": selected
        }
    return render(request, 'publish/route.html', context)

def select_route(request):
    intializeDB()
    if request.method == 'POST':
        route_id = request.POST.get("hiddenInput")
        username = request.POST.get('hiddenUser')
        ride = request.POST.get('hiddenRide')
        print("route from form: ",route_id)
        ride = ride.replace("\'", "\"")
        ride = json.loads(ride)
        ride_id = ride['_id']
        attach_user_to_route(username, route_id)
        return redirect(display_ride, ride_id=ride['_id'] )
    return render(request, 'publish/publish.html', {"username": None, "gmap_api_key": secrets.GoogleMapsAPIKey})

def routeSelect(username, routes):
    intializeDB()
    user = userDB.find_one({"username": username})
    if user == None or routes == None:
        print("returning NONE")
        return None


    user_routes = user['rides']
    print("User routes: ",user_routes)
    for route in routes:
        if route['_id'] in user_routes:
            print("FOUND")
            return route['_id']
    return None

def get_routes(ride):
    routes = []
    if 'route_id' not in ride:
        return None
    route_ids = ride['route_id']
    documents = routesDB.find({'_id': {'$in': route_ids}})
    docs = []
    for doc in documents:
        doc['id'] = doc["_id"]
        route_date = doc['id'].split("_")[3]
        user = userDB.find_one({"_id": doc['creator'] })
        user['id'] = user['_id']
        doc['creator'] = user
        doc['distance'] = round(doc["distance"], 1)
        if not DateUtils.has_date_passed(route_date):
            docs.append(doc)   
    return docs

def create_route(request):
    """
    Handles the selection of a route for a specific ride and updates the database accordingly.

    Args:
        request (HttpRequest): The HTTP request object containing session data and form data.

    Returns:
        HttpResponse: A redirect to `display_ride()` if a route is selected, or a rendered 
                      response of 'publish/publish.html' if it's not a POST request.
    """
    intializeDB()
    initializeService()
    if request.method == 'POST':
        route = {
            "_id":
                f"""{request.POST.get('purpose')}_{request.POST.get('s_point')}_{request.POST.get('destination')}_{request.POST.get("date")}_{request.POST.get("hour")}_{request.POST.get("minute")}_{request.POST.get("ampm")}""",
                "purpose": request.POST.get('purpose'),
                "s_point": request.POST.get('spoint'),
                "destination": request.POST.get('destination'),
                "type": request.POST.get('type'),
                "date": request.POST.get("date"),
                "hour": request.POST.get("hour"),
                "minute":  request.POST.get("minute"),
                "ampm": request.POST.get("ampm"),
                "details": request.POST.get("details"),
            }
        ride_id = request.POST.get('destination')
        route['creator'] = attach_user_to_route(request.session['username'], route['_id'])
        if(request.POST.get("slat")):
            route["s_lat"] = request.POST.get("slat")
            route["s_long"] = request.POST.get("slong")
        if(request.POST.get("dlat")):
            route["d_lat"] = request.POST.get("dlat")
            route["d_long"] = request.POST.get("dlong")

        if(request.POST.get("dlat") and request.POST.get("slat")):
            res = mapsService.get_route_details(route["s_lat"], route["s_long"], route["d_lat"], route["d_long"])
            route['fuel'] = res.get("fuel", 0)
            route["distance"] = res.get("distance", 0)

        if routesDB.find_one({'_id': route['_id']}) == None:
            routesDB.insert_one(route)
            print("Route added")
            if ridesDB.find_one({'_id': ride_id}) == None:
                ride = {
                    "_id":
                        request.POST.get('destination'),
                    "destination": request.POST.get('destination'),
                    "route_id": [route['_id']]
                }
                ridesDB.insert_one(ride)
                print("Ride Added")
            else:
                ride = ridesDB.find_one({'_id': ride_id})
                ride['route_id'].append(route['_id'])
                ridesDB.update_one({'_id': ride_id},{"$set": {"route_id": ride['route_id']}})
                print("Ride Updated")
        return redirect(display_ride, ride_id=ride_id)
    return render(request, 'publish/publish.html', {"username": request.session.get('username', None), "gmap_api_key": secrets.GoogleMapsAPIKey})

def attach_user_to_route(username, route_id):
    """
    Attaches a selected route to the user's list of rides in the database.

    Args:
        username (str): The username of the user who selected a route.
        route_id (str): The ID of the route to be attached to the user's list of rides.

    Returns:
        ObjectId: The unique ID (`_id`) of the user if found and updated.
        HttpResponse: A redirect to 'home/home.html' if the user is not found.
    """
    intializeDB()
    remove = False
    user = userDB.find_one({"username": username})
    route = routesDB.find_one({"_id": route_id})
    if user == None:
        return redirect('home/home.html', {"username": None})
    if route == None:
        return redirect('home/home.html', {"username": username})
    user['rides'].append(route_id)
    users = route.get('users', [])


    for i in range(len(users)):
        if(users[i] == user["_id"]):
            remove = True
            del users[i]

    if not remove:
        users.append(user['_id'])

    
    userDB.update_one({"username": username},{"$set": {"rides": user['rides']}})
    routesDB.update_one({"_id": route_id}, {"$set": {"users": users}})
    return user['_id']
