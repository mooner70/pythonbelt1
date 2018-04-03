# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import time
from  datetime import *
import bcrypt
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex = re.compile('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
class RegManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["name"]) < 3:
            errors["name"] = "Name should be more than 3 characters"
        if len(postData["email"]) < 1:
            errors["email"] = "Email field cannot be empty"
        elif not email_regex.match(postData["email"]):  
            errors["email"] = "Invalid email address"
        count = User.objects.filter(email=postData["email"]).count()
        if count > 0:
            errors["email"] = "Email already exists"
        if len(postData["password"]) < 8:     
            errors["password"] = "Password should be more thatn 8 characters"
        if postData["password"] != postData["confirm"]:
            errors["confirm"] = "Confirmation does not match Password"
        if len(postData["birthday"]) < 1:
            errors["birthday"] = "Birthday field cannot be empty"
        if postData["birthday"] > datetime.now().strftime("%Y-%m-%d"):
            errors["birthday"] = "Birthday can not be in the future"   
        return errors
    def login_validator(self, postData):
        errors = {}
        if len(postData["email"]) < 1:
            errors["email"] = "Email field cannot be empty"
        elif not email_regex.match(postData["email"]):  
            errors["email"] = "Invalid email address"
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be longer than 8 characters"
        check = User.objects.filter(email=postData["email"])
        if len(check) == 0:
            errors["password"] = "You must enter a password"
            return errors
        if not bcrypt.checkpw(postData["password"].encode(), check[0].password.encode()):
            errors["password"] = "Password doesn't match"
        return errors
    def add_validator(self, postData):
        errors = {}
        if postData["taskdate"] < datetime.now().strftime("%Y-%m-%d"):
            errors["taskdate"] = "Date can not be in the past"
        # if postData["time"].strptime("%I:%M:%S").time():
        #     errors["time"] = "Time can not be in the past"
        if len(postData["task"]) < 1:
            errors["task"] = "Task field cannot be empty"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RegManager()

class Appointments(models.Model):
    task = models.CharField(max_length=255)
    time = models.DateTimeField(null=True, blank=True)
    taskdate = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, related_name = "appointments")
    # users = models.ManyToManyField(User, related_name = "user_apts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RegManager()