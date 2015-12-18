import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from .database import Base, engine


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'), nullable=False)
    
    def as_dictionary(self):
        song = {
            "id": self.id,
            "song_file": {
                "id": self.song_file.id,
                "filename": self.song_file.filename
            }
        }
        return song
        
class File(Base):
    __tablename__="files"
    id = Column(Integer, primary_key=True)
    filename = Column(String(128))
    
    #add a relationship
    passport = relationship("Song", uselist=False, backref="song_file")
    
    def as_dictionary(self):
        file = {
            "id": self.id,
            "filename": self.filename
            }
        return file