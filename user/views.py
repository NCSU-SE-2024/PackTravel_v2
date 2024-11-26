from django.shortcuts import render, redirect
from utils import get_client
from .forms import RegisterForm, LoginForm, EditUserForm
from services import GoogleCloud
from config import Secrets
from bson.objectid import ObjectId
from django.forms.utils import ErrorList
from utilities import DateUtils
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

client = None
db = None
userDB = None
ridesDB = None
routesDB = None
googleCloud = None
secrets = None

def initializeCloud():
    """
    Initializes the Google Cloud service with credentials and storage bucket.
    
    Globals:
        googleCloud (GoogleCloud): Google Cloud service instance for file upload.
        secrets (Secrets): Object holding sensitive credentials.
    """
    global googleCloud, secrets
    if not secrets:
        secrets = Secrets()
    
    if not googleCloud:
        googleCloud = GoogleCloud(secrets.CloudCredentials, secrets.CloudStorageBucket)

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


# Home page for PackTravel
def index(request, username=None):
    """
    Renders the home page and adds authenticated user data to the session if logged in.

    Args:
        request (HttpRequest): The request object.
        username (str, optional): Username to display on the page.

    Returns:
        HttpResponse: The home page with user session data.
    """
    intializeDB()
    if request.user.is_authenticated:
        request.session["username"] = request.user.username
        request.session['fname'] = request.user.first_name
        request.session['lname'] = request.user.last_name
        request.session['email'] = request.user.email
        user = userDB.find_one({"username": request.user.username})
        if not user:
            userObj = {
                "username": request.user.username,
                "fname": request.user.first_name,
                "lname": request.user.last_name,
                "email": request.user.email,
                "rides": []
            }
            userDB.insert_one(userObj)
            print("User Added")
        else:
            print("User Already exists")
            print(f'Username: {user["username"]}')
        return render(request, 'home/home.html', {"username": request.session["username"]})
    if request.session.has_key('username'):
        return render(request, 'home/home.html', {"username": request.session["username"]})
    return render(request, 'home/home.html', {"username": None})


def register(request):
    """
    Handles user registration, storing user data in the database and uploading profile picture.

    Args:
        request (HttpRequest): The request object containing form data.

    Returns:
        HttpResponse: Redirects to home page on success, or renders registration form on failure.
    """

    intializeDB()
    initializeCloud()
    if request.method == "POST":
        public_url = ""
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["profile_picture"]
            if image is not None:
                image.name = f"{form.cleaned_data['username']}.png"
                public_url = googleCloud.upload_file(image, image.name)
            
            userObj = {
                "username": form.cleaned_data["username"],
                "unityid": form.cleaned_data["unityid"],
                "fname": form.cleaned_data["first_name"],
                "lname": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email"],
                "password": make_password(form.cleaned_data["password1"]),
                "phone": form.cleaned_data["phone_number"],
                "rides": [],
                "pfp": public_url
            }
            
            savedUser = userDB.insert_one(userObj)
            request.session['username'] = userObj["username"]
            request.session['unityid'] = userObj["unityid"]
            request.session['fname'] = userObj["fname"]
            request.session['lname'] = userObj["lname"]
            request.session['email'] = userObj["email"]
            request.session['phone'] = userObj["phone"]
            request.session['userid'] = str(savedUser.inserted_id)
            return redirect('index')
        else:
            return render(request, 'user/register.html', {"form": form})
    else:
        if request.session.has_key('username'):
            return index(request, request.session['username'])
        form = RegisterForm()
        return render(request, 'user/register.html', {"form": form})


def logout(request):
    """
    Logs out the user by clearing session data.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Redirects to the home page.
    """
    try:
        request.session.clear()
    except:
        pass
    return redirect(index)

def user_profile(request, userid):
    """
    Renders the user's profile page or a 404 page if the user ID is not found.

    Args:
        request (HttpRequest): The request object.
        userid (str): The ID of the user profile to display.

    Returns:
        HttpResponse: Profile page or 404 page if user not found.
    """
    intializeDB()
    if(not userid):
        return render(request, "user/404.html", {"username": request.session.get("username", None)})
    profile = userDB.find_one({"_id": ObjectId(userid)})
    if not profile:
        return render(request, "user/404.html", {"username": request.session.get("username", None)})

    user_id = str(profile['_id'])

    # Fetch routes created by this user
    user_routes = routesDB.find({"creator": ObjectId(user_id)})

    past_rides,current_rides  = list(), list()
    for route in user_routes:
        if DateUtils.has_date_passed(route['date']):
            past_rides.append(route)
        else:
            current_rides.append(route)
                
    if(profile):
        return render(request, 'user/profile.html', {"username": request.session.get("username", None), "user": profile, "pastrides": past_rides, "currentrides": current_rides})

    else:
        return render(request, "user/404.html", {"username": request.session.get("username", None)})

# @describe: Existing user login
def login(request):
    """
    Logs in an existing user by validating the form data and saving session details.

    Args:
        request (HttpRequest): The request object containing form data.

    Returns:
        HttpResponse: Redirects to home page on success, or renders login form on failure.
    """

    intializeDB()
    if request.session.has_key('username'):
        return redirect('index')
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                user = userDB.find_one({"username": username})
                if user and check_password(form.cleaned_data["password"], user["password"]):
                    request.session['userid'] = str(user['_id'])
                    request.session["username"] = username
                    request.session['unityid'] = user["unityid"]
                    request.session['fname'] = user["fname"]
                    request.session['lname'] = user["lname"]
                    request.session['email'] = user["email"]
                    request.session["phone"] = user["phone"]
                    return redirect('index')
                else:
                    form.add_error('password', "Invalid username or password")
            return render(request, 'user/login.html', {"form": form})
        form = LoginForm()
        return render(request, 'user/login.html', {"form": form})


def my_rides(request):
    """
    Renders the user's rides if logged in, otherwise redirects to home.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The user's ride page or redirect to home if not authenticated.
    """
    intializeDB()
    if not request.session.has_key('username'):
        request.session['alert'] = "Please login to view your rides."
        messages.info(request, "Please login to view your rides!")
        return redirect('index')
    all_routes = list(routesDB.find())
    user_list = list(userDB.find())
    final_user, processed = list(), list()
    for user in user_list:
        if request.session["username"] == user['username']:
            final_user = user
    user_routes = final_user['rides']
    for route in all_routes:
        for i in range(len(user_routes)):
            if user_routes[i] == route['_id']:
                route['id'] = route['_id']
                processed.append(route)

    return render(request, 'user/myride.html', {"username": request.session['username'], "rides": processed})


def delete_ride(request, ride_id):
    """
    Deletes a specified ride from the routes collection.

    Args:
        request (HttpRequest): The request object.
        ride_id (str): The ID of the ride to delete.

    Returns:
        HttpResponse: Redirects to the user's rides page.
    """
    intializeDB()
    user = userDB.find_one({"username": request.session['username']})
    if user is None:
        pass
    routesDB.delete_one({"_id": ride_id})
    return redirect("/myrides")


def edit_user(request):
    intializeDB() 
    user = userDB.find_one({"username": request.session['username']}) 

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES)  
        if form.is_valid():
            image = form.cleaned_data.get("profile_picture") 
            public_url = user.get('pfp')
            if image: 
                initializeCloud() 
                image.name = f"{request.session['username']}.png" 
                public_url = googleCloud.upload_file(image, image.name) 

            
            userDB.update_one(
                {"username": request.session['username']},
                {
                    "$set": {
                        "fname": form.cleaned_data['first_name'],
                        "lname": form.cleaned_data['last_name'],
                        "phone": form.cleaned_data['phone_number'],
                        "pfp": public_url,  
                    }
                }
            )

            
            request.session['fname'] = form.cleaned_data['first_name']
            request.session['lname'] = form.cleaned_data['last_name']
            request.session['phone'] = form.cleaned_data['phone_number']

            return redirect('user_profile', userid=str(user['_id']))  
    else:
        form = EditUserForm(initial={
            "unityid": user.get("unityid"),
            "first_name": user.get("fname"),
            "last_name": user.get("lname"),
            "email": user.get("email"),
            "phone_number": user.get("phone"),
            "profile_picture": user.get("pfp"),
        })  

    return render(request, 'user/edit_user.html', {"username": request.session['username'], 'form': form})  

   


