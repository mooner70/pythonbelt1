# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.timezone import get_current_timezone
from datetime import datetime
from time import strptime, localtime, strftime
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
# from .models import UserRegistration
from models import *
import bcrypt

def index(request):
    
    return render(request, 'index.html')
def logout(request):
    request.session.flush()
    return redirect('/')
def user_registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect("/")
    else:
        pw = request.POST["password"]
        hash1 = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        b = User.objects.create(name=request.POST["name"], email=request.POST["email"], password=hash1, birthday=request.POST["birthday"])
        request.session['name'] = request.POST["name"]
        request.session["user_id"] = b.id
        return redirect("/appointments")
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect("/")
    else:
        user = User.objects.get(email = request.POST["email"])
        request.session['name'] = user.name
        request.session["user_id"] = user.id
        return redirect("/appointments")
def add(request):
    errors = Appointments.objects.add_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect("/appointments")
    else:
        a = User.objects.get(name=request.session['name'])
        time = datetime.strptime(request.POST["time"], "%H:%M")
        Appointments.objects.create(taskdate=request.POST["taskdate"], task=request.POST["task"], time=time, user = a)
        return redirect("/appointments")
def appointments(request):
    c = User.objects.get(id=request.session["user_id"])
    
    context = {
        "my_tasks" : Appointments.objects.filter(user = c, taskdate__date=datetime.now()),
        "other_appointments" : Appointments.objects.filter(user = c).exclude(taskdate__date=datetime.now()),
        "testsort" : Appointments.objects.order_by("taskdate")
    }
    return render(request, 'appointments.html', context)
def delete_from_list(request, id):
    a = Appointments.objects.get(id=id)
    a.delete()
    return redirect('/appointments')
def edit_appointments(request, id):
    context = {
        "task_id" : Appointments.objects.get(id=id),
        "task" : Appointments.objects.get(id=id).task, 
        "time" : Appointments.objects.get(id=id).time.strftime("%H:%M"),
        "taskdate" : Appointments.objects.get(id=id).taskdate.strftime("%Y-%m-%d")
        }
    print context
    return render(request, 'update.html', context)
def save_appointments(request, id):
    errors = Appointments.objects.add_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect("/appointments/" + id)
    else:
        # a = User.objects.get(name=request.session['name'])
        time = datetime.strptime(request.POST["time"], "%H:%M")
        u = Appointments.objects.get(id=id)
        u.taskdate = request.POST["taskdate"]
        u.time = time
        u.task = request.POST["task"]
        u.save()






        # Appointments.objects.create(taskdate=request.POST["taskdate"], task=request.POST["task"], time=time)
        return redirect("/appointments")


# Updating the record - once you obtain an object that has the record you want to modify, use save() to update the record.  For example
#     1. b = Blog.objects.first() # gets the first record in the blogs table
#     2. b.name = "CodingDojo Blog"  # set name to be "CodingDojo Blog"
#     3. b.save() # updates the blog record