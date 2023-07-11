from mongoengine import connect

import configuration

def init():
    connect(host=configuration.DB_URI)
