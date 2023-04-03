from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    
    
    currentUser = None #stores user
    isLoggedIn = False #checks for if user is logged in

    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        userRegistered = False
        while(userRegistered == False):
            handle = input("What will your twitter handle be?")
            usernameList = db_session.query(User).where(User.username == handle).first()
            if(usernameList is not None):
                print("Username already taken. Try again")
            else:
                password = input("Please enter a password")
                passwordRepeat = input("Re-enter your password")
                if(password == passwordRepeat):
                    db_session.add(User(handle, password))
                    userRegistered = True
                    db_session.commit()
                    print("You have succeeded")
                else:
                    print("Passwords don't match. Try again.")
        self.login()
    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        while(self.isLoggedIn == False):
            username = input("Username: ")
            password = input("Password: ")
            theUser = db_session.query(User).where(User.username == username and User.password == password).first()
            if(theUser is not None and password == theUser.password):
                self.currentUser = theUser
                self.isLoggedIn =  True
            else:
                print("Username or password incorrect")

    #Logs the user out
    def logout(self):
        self.isLoggedIn = False
        self.currentUser = None
        print("You have successfully logged out")


    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        print("Welcome to ATCS Twitter!")
        print("Please select a Menu Option")
        print("1. Login")
        print("2. Register User")
        print("0. Exit")
        nextStep = input("Which option will you choose(1/2/0)?")
        if(nextStep == "1"):
            self.login()
        elif(nextStep == "2"):
            self.register_user()
        else:
            self.isLoggedIn = False
            self.currentUser = None

    def follow(self):
        followUsername = input("Who would you like to follow?")
        myId = self.currentUser.username
        followerid = db_session.query(User.username).where(User.username == followUsername).first()
        toFollow = Follower(myId, followUsername)
        isAlreadyFollowing = db_session.query(Follower).where(Follower.follower_id == myId and Follower.following_id == followerid).first()
        if(isAlreadyFollowing is None):
            db_session.add(toFollow)
            print("You are now following " + followUsername)
        else:
            print("You already follow " + followUsername)
        db_session.commit()

    def unfollow(self):
        followUsername = input("Who would you like to unfollow?")
        myId = self.currentUser.username
        followerid = db_session.query(User.username).where(User.username == followUsername).first()
        isAlreadyFollowing = db_session.query(Follower).where(Follower.follower_id == myId and Follower.following_id == followerid).first()
        if(isAlreadyFollowing is not None):
            db_session.delete(isAlreadyFollowing)
            db_session.commit()
            print("You no longer follow " + followUsername)
        else:
            print("You don't follow " + followUsername)


    def tweet(self):
        content = input("Create tweet: ")
        tags = input("Enter your tags separated by spaces: ")
        tagslist = tags.split(" ")
        db_session.add(Tweet(content, datetime.now(), self.currentUser.username))
        db_session.commit()
        currTweet = db_session.query(Tweet).where(Tweet.content == content).first()
        print(currTweet.id)

        for t in tagslist:
            tagAlreadyExists = db_session.query(Tag.content).where(Tag.content == Tag(t).content).first()
            if(tagAlreadyExists is None):
                db_session.add(Tag(t)) 
                db_session.commit()
            currTag = db_session.query(Tag).where(Tag.content == t).first()
            print(currTag.id)
            print(currTweet.id)
            db_session.add(TweetTag(currTweet.id, currTag.id))
            db_session.commit()
    
    def view_my_tweets(self):
        tweetsList = db_session.query(Tweet).where(Tweet.username == self.currentUser.username).all()
        self.print_tweets(tweetsList)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        trueTweets = db_session.query(Tweet).all()
        following = list(map(lambda x: x.username, self.currentUser.following))
        trueTweets = list(filter(lambda x: x.username in following, trueTweets))
        for count, tweet in enumerate(reversed(trueTweets)):
            if count < 5:
                print("==============================")
                print(tweet)
                print("==============================")

    def search_by_user(self):
        user = input("Enter a username: ")
        userTweets = db_session.query(Tweet).where(Tweet.username == user).all()
        if(userTweets is None):
            print("There is no user by that name")
        else:
            self.print_tweets(userTweets)

    def search_by_tag(self):
        searchedTag = input("Enter a tag: ")
        tag = db_session.query(Tag).where(Tag.content == searchedTag).first()
        if(tag is None):
            print("There are no tweets with this tag")
        else:
            self.print_tweets(tag.tweets)


    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()
        self.startup()
        
        while(self.isLoggedIn == True):
            self.print_menu()
            option = int(input("What would you like to do?"))

            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
        
        self.end()
