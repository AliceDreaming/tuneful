import unittest
import os
import shutil
import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
from io import StringIO

import sys; print(list(sys.modules.keys()))
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())

    def test_get_empty_songs(self):
        """Getting songs from an mepty database"""
        response=self.client.get("/api/songs")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
    
        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data, [])
    
    def test_songs_get(self):
        """ get all the songs """
        fileA=models.File(filename="songA")
        songA=models.Song()
        songA.song_file=fileA
        
        fileB=models.File(filename="songB")
        songB=models.Song()
        songB.song_file=fileB
        
        session.add_all([songA, songB, fileA, fileB])
        session.commit()
        
        response = self.client.get("/api/songs")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        songs = json.loads(response.data.decode("ascii"))
        self.assertEqual(len(songs), 2)
        
        song0=songs[0]
        self.assertEqual(song0.id, songA.id)
        self.assertEqual(song0.song_file.id, fileA.id)
        self.assertEqual(song0.song_file.filename, fileA.filename)
        
        song1=songs[1]
        self.assertEqual(song1.id, songB.id)
        self.assertEqual(song1.song_file.id, fileB.id)
        self.assertEqual(song1.song_file.filename, fileB.fileName)