# Inside models.py
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^[a-zA-Z\d]{8,}$")
NAME_REGEX = re.compile(r"^[a-zA-Z\d]{3,}$")


class UserManager(models.Manager):
    def ValidateTheUser(self, postData): # 5/17 the name "postData" isn't excluseive... it could be anything You only need to MIGRATE when you change the shape of the database
        result = {
            'status': False,
            'errors': []
        }
        if len(postData['name']) < 1:
            result['errors'].append("Your name is required")
        elif not NAME_REGEX.match(postData['name']):
            result['errors'].append("Your name must be more than 3 characters")
        if len(postData['username']) < 1:
            result['errors'].append("A username is required")
        elif not NAME_REGEX.match(postData['username']):
            result['errors'].append("Your username must be more than 3 characters")
        if len(postData['password1']) < 1:
            result['errors'].append("Password is required")
        elif not PASSWORD_REGEX.match(postData['password1']):
            result['errors'].append("Password must contain a number, a letter, and be at least 8 characters")
        if len(postData['password2']) < 1:
            result['errors'].append("Password confirmation is required")
        elif postData['password2'] != postData['password1']:
            result['errors'].append("Passwords must match")
        if len(result['errors']) == 0:  # this is important to see if there are errors
            result['status'] = True
            # We need to return the User ID in a return statement to Session in Views.
            result['user_id'] = User.objects.create(
                name = postData['name'],
                username = postData['username'],
                password = bcrypt.hashpw(postData['password1'].encode(), bcrypt.gensalt())
                #if this is a passrword, the bcrypt it (import it first)
            ).id  # Save this USER id in Session on the Views page

        return result

    def ValidateLogin(self, postData):
        result = {
            'status': False,
            'errors': []
        }
        existing_users = User.objects.filter(username__iexact=postData['username'])
        if len(existing_users) == 0:
            result['errors'].append("Invalid email & password combination")
        else:
            if bcrypt.checkpw(postData['password3'].encode(), existing_users[0].password.encode()):
                result['status'] = True
                result['user_id'] = existing_users[0].id
            else:
                result['errors'].append("Invalid email & password combination")
        return result

    def ValidateTrip(self, postData, user_id):
        result = {
            'status': False,
            'errors': [],
        }
        # today = datetime.date.today()
        # startDate = postData['start']
        # endDate = postData['end']
        # start_date = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
        # end_date = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
        if len(postData['destination']) < 1:
            result['errors'].append("A destination is required")
        if len(postData['description']) < 1:
            result['errors'].append("A description of the trip is required")
        if len(postData['start']) < 1:
            result['errors'].append("A start date is required")
        else:
            today = datetime.date.today()
            startDate = postData['start']
            # endDate = postData['end']
            # temp = datetime.datetime.strptime()
            start_date = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
            # end_date = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
            if start_date <= today:
                result['errors'].append("Start date must be in the future")
        if len(postData['end']) < 1:
            result['errors'].append("An end date is required")
        else:
            # today = datetime.date.today()
            startDate = postData['start']
            endDate = postData['end']
            start_date = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
            if end_date <= start_date:
                result['errors'].append("End date must be after start date")
        # if start_date <= today:
        #     result['errors'].append("Start date must be in the future")
        # if end_date <= start_date:
        #     result['errors'].append("End date must be after start date")

        if len(result['errors']) == 0:  # this is important to see if there are errors
            result['status'] = True
            me = User.objects.get(id=user_id)
            trip = Trip.objects.create(
                destination=postData['destination'],
                description=postData['description'],
                start=postData['start'],
                end=postData['end'],
                trip_creator=me
            )
            trip.users.add(me)
            trip.save()
        return result

    # def ValidateTrip(self, postData):


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()  # 5/17 this LINE is super important AND the UserManager class has to be ABOVE this line

    def __repr__(self):
        return "<User object: name:{} username:{} id:{}>".format(self.name, self.username, self.id)


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    start = models.DateField(auto_now=False)
    end = models.DateField(auto_now=False)
    trip_creator = models.ForeignKey(User, related_name="created_trips", null=True)
    users = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return "<Trip object: Destination:{}>".format(self.destination)


    # email = models.CharField(max_length=255)
    # books = models.ManyToManyField(Book, related_name="authors", null=True)
    # notes = models.TextField(null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
