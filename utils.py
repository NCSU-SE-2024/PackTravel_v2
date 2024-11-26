import os
import sys
import certifi
from pymongo import MongoClient
from config import Secrets


def get_client():
    secret = Secrets()
    client = MongoClient(secret.MongoConnectionURL,
                         tlsCAFile=certifi.where())

    return client
