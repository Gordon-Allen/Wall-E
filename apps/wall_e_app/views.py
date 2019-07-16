from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from .models import *

def index(request):
    if "id" in request.session.keys():
        redirect('/wall')
    return render(request, 'wall_e_app/index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        user.save()
        request.session['id'] = user.id 
        return redirect("/wall")

def wall(request):
    context = {
        "user" : User.objects.get(id=request.session['id']),
        "post_data" : Message.objects.all(),
        "comment_data" : Comment.objects.all()
    }
    return render(request, 'wall_e_app/user_wall.html', context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        user = User.objects.get(email=request.POST['login_email'])
        request.session['id'] = user.id
        return redirect('/wall')

def log_out(request):
    del request.session['id']
    return redirect('/')

def add_message(request):
    Message.objects.create(message=request.POST['message'], user=User.objects.get(id=request.session['id']))
    return redirect('/wall')

def add_comment(request):
    Comment.objects.create(Comment=request.POST['comment'], user = User.objects.get(id=request.session['id']), message=Message.objects.get(id=request.POST['message_id']))
    return redirect('/wall')

def delete(request, id):
    x = Message.objects.get(id=id)
    x.delete()
    return redirect('/wall')

def dcomment(request, id):
    y = Comment.objects.get(id=id)
    y.delete()
    return redirect('/wall')