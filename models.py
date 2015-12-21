import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime
from flask import url_for
from raspberry_play import db

class Video(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    video_url = db.StringField(verbose_name="Video_url", required=True)
    name = db.StringField(verbose_name="Name", max_length=255, required=True)
    meta = {
        'indexes': ['-created_at', 'name'],
        'ordering': ['-created_at']
    }

