# coding:utf8
from __future__ import unicode_literals
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import ProfileEditForm
from .models import StepUser, StepUserHistory


def step_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(request, user)
            profile(request, user.id)
            return redirect('web-mug:profile', user.id)
    return redirect('web-mug:index')


def step_logout(request):
    logout(request)
    return redirect('web-mug:index')


def profile(request, user_id):
    users = StepUser.objects.all().order_by('-steps')[:10]
    usersteps = StepUserHistory.objects.all()
    theUser = StepUser.objects.get(user__id=user_id)
    fats = StepUser.objects.all().order_by('steps')[:10]

    month = datetime.date.today() - datetime.timedelta(days=30)
    week = datetime.date.today() - datetime.timedelta(days=7)
    today = datetime.date.today()

    stepsmonth = StepUserHistory.objects.filter(step_user=user_id).filter(date__range=(month, today))
    stepmonth = 0
    for step in stepsmonth:
        stepmonth += step.steps

    stepsweek = StepUserHistory.objects.filter(step_user=user_id).filter(date__range=(week, today))
    stepweek = 0
    for step in stepsweek:
        stepweek += step.steps

    stepstoday = StepUserHistory.objects.filter(step_user=user_id).filter(date=today)
    steptoday = 0
    for step in stepstoday:
        steptoday += step.steps

    allsteps = StepUserHistory.objects.filter(step_user=user_id)
    allstep = 0
    for step in allsteps:
        allstep += step.steps

    context = {
        'theUser': theUser,
        'users': users,
        'usersteps': usersteps,
        'fats': fats,
        'stepmonth': stepmonth,
        'stepweek': stepweek,
        'steptoday': steptoday,
        'allstep': allstep
    }
    return render(request, 'profile/profile.html', context)


def profile_edit(request, user_id, ):
    theUser = StepUser.objects.get(user=user_id)
    context = {
        'theUser': theUser
    }
    return render(request, 'profile/profile-edit.html', context)


def profile_edit_form(request, user_id):
    form = ProfileEditForm()
    if request.method == 'POST':
        f = ProfileEditForm(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        city = request.POST['city']
        age = request.POST['age']
        if f.is_valid():
            StepUser.objects.filter(stepUser=user_id).update(city=city, age=age)
            User.objects.filter(id=user_id).update(first_name=first_name, last_name=last_name)
            use = StepUser.objects.get(stepUser=user_id)
            use.photo = request.FILES['photo']
            use.save()
            return redirect('profile', user_id)
        context = {
            'form': f,
            'first_name': first_name,
            'last_name': last_name,
            'city': city,
            'age': age
        }
        return render(request, 'profile/profile-edit.html', context)
    return redirect('profile_edit')


def profiles(request):
    users = StepUser.objects.all()
    steps = StepUserHistory.objects.all()
    context = {
        'users': users,
        'steps': steps
    }
    return render(request, 'profile/profiles.html', context)
