"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    following = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.follower_id",
                             secondaryjoin="User.username==Follower.following_id")
    
    followers = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.following_id",
                             secondaryjoin="User.username==Follower.follower_id",
                             overlaps="following")
    
    #init
    def __init__(self, username, password):
        self.username = username
        self.password =  password
    #repr
    def __repr__(self):
        return "@" + self.username


class Follower(Base):
    __tablename__ = "followers"

    # Columns
    id = Column("id", INTEGER, autoincrement = True, primary_key=True)
    follower_id = Column('follower_id', TEXT, ForeignKey('users.username'))
    following_id = Column('following_id', TEXT, ForeignKey('users.username'))


    def __init__(self, follower_id, following_id):
        self.follower_id = follower_id
        self.following_id = following_id

class Tweet(Base):
    # TODO: Complete the class
    __tablename__ = "tweets"

    #Columns
    id = Column("id", INTEGER, autoincrement = True, primary_key= True)
    content = Column("content", TEXT)
    timestamp = Column("timestamp", INTEGER)
    username = Column("username", TEXT, ForeignKey('users.username'))
    tags = relationship("Tag", secondary = "tweettags", back_populates="tweets")

    #init
    def __init__(self, content, timestamp, username):
        #id autoincrements
        self.content = content
        self.timestamp = timestamp
        self.username = username

    def printTags(self):
        retstr = ""
        for t in self.tags:
            retstr += t.content
        return retstr

    #repr
    def __repr__(self):
        return "@" + self.username + ("\n") + self.content + ("\n")+ self.printTags() +("\n")+ self.timestamp

class Tag(Base):
    # TODO: Complete the class
    __tablename__ = "tags"

    #Columns
    id = Column("id", INTEGER, autoincrement = True, primary_key = True)
    content = Column("content", TEXT)
    tweets = relationship("Tweet", secondary = "tweettags", back_populates = "tags")

    def __init__(self, tag):
        self.content = tag

    #Constructor
    def __repr__(self):
        return "#"+self.content


class TweetTag(Base):
    # TODO: Complete the class
    __tablename__ = "tweettags"

    #Columns
    id = Column("id", INTEGER, autoincrement = True, primary_key = True)
    tweet_id = Column("tweet_id", INTEGER, ForeignKey('tweets.id'))
    tag_id = Column("tag_id", INTEGER, ForeignKey('tags.id'))

    def __init__(self, tweet_id, tag_id):
        self.tweet_id = tweet_id
        self.tag_id = tag_id

