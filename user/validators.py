from django.core.exceptions import ValidationError
from utils import get_client
import re

userDB = None

def intializeDB():
    global userDB
    if(userDB == None):
        client = get_client()
        db = client.SEProject
        userDB = db.userData

def validate_email_domain(value):
    pattern = re.compile("^[a-zA-Z0-9]+$")
    allowed_domain = 'ncsu.edu'
    email_parts = value.split('@')
    domain = email_parts[-1]
    if len(email_parts) != 2:
        raise ValidationError(f"Invalid email")
    if not pattern.match(email_parts[0]):
        raise ValidationError(f"Invalid email")
    if domain != allowed_domain:
        raise ValidationError(f"Email must be from the {allowed_domain} domain.")
    
def validate_unique_unity_id(value):
    intializeDB()
    unity_user = userDB.find_one({"unityid": value})
    if(unity_user):
        raise ValidationError("Unity ID must be unique")

def validate_unique_username(value):
    intializeDB()
    unity_user = userDB.find_one({"username": value})
    if(unity_user):
        raise ValidationError("Unity ID must be unique")

def validate_password(value):
    if len(value) < 8:
        raise ValidationError(f"Password is too short")
    
    elif len(value) > 16:
        raise ValidationError(f"Password is too long")
    
    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", value):
        raise ValidationError("Password must contain at least one lowercase letter.")

    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", value):
        raise ValidationError("Password must contain at least one uppercase letter.")

    # Check for at least one digit
    if not re.search(r"\d", value):
        raise ValidationError("Password must contain at least one digit.")

    # Check for at least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
        raise ValidationError("Password must contain at least one special character.")

    # Check for common passwords
    common_passwords = ["password!123456", "12345678", "qwerty", "admin"]
    if value.lower() in common_passwords:
        raise ValidationError("This password is too common. Please choose a more unique password.")
    
    # Check for repeated characters
    if re.search(r"(.)\1{2,}", value):
        raise ValidationError("Password contains repeated characters. Please avoid easily guessable patterns.")