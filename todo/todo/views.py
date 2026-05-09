from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from todo import models
from todo.models import TODOO
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def home(request):
    return redirect('/todopage')

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')
        print(fnm, emailid, pwd)

        if User.objects.filter(username=fnm).exists():
            return HttpResponse("⚠ Username already exists")

        my_user = User.objects.create_user(fnm, emailid, pwd)
        my_user.save()
    return redirect('/login')

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(fnm, pwd)

        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            auth_login(request, userr)
            return redirect('/todopage')
        else:
            return HttpResponse("❌ Invalid credentials")

    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def todopage(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODOO(title=title, user=request.user)
        obj.save()
        return redirect('/todopage')

    res = models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res})

def delete_todo(request, srno):
    print(srno)
    obj = models.TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

@login_required(login_url='/login')
def edit_todo(request, srno):
    print("Editing:", srno)

    try:
        obj = models.TODOO.objects.get(srno=srno, user=request.user)
    except models.TODOO.DoesNotExist:
        return HttpResponse("⚠ Task not found")

    if request.method == 'POST':
        title = request.POST.get('title')
        completed = request.POST.get('completed')
        print(title, completed)

        obj.title = title
        # The model field is status (BooleanField). Persist to that field.
        obj.status = True if completed == "on" else False
        obj.save()
        return redirect('/todopage')

    return render(request, 'edit_todo.html', {'todo': obj})