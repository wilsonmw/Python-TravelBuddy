from django.shortcuts import render, redirect
from .models import Trip, User
from django.contrib import messages
import datetime

# Create your views here.
def home(request):
    if not request.session['userId']:
        return redirect('/')
    user = User.objects.get(id=request.session['userId'])
    trips = Trip.objects.filter(owner = user)
    otherTrips = Trip.objects.all().exclude(owner = user).exclude(joins = user)
    joins = Trip.objects.filter(joins = user)
    context = {
        'user':user,
        'trips':trips,
        'otherTrips':otherTrips,
        'joins':joins
    }
    return render(request, 'travelBuddy_app/home.html', context)

def addTrip(request):
    if not request.session['userId']:
        return redirect('/')
    results = Trip.objects.addNewTrip(request.POST, request.session['userId'])
    if results['status']==False:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/addTravel')
    return redirect('/home')

def addTravel(request):
    if not request.session['userId']:
        return redirect('/')
    return render(request, 'travelBuddy_app/addTravel.html', context)

def logout(request):
    request.session['userId']=None
    return redirect('/')

def show(request, id):
    if not request.session['userId']:
        return redirect('/')
    trip = Trip.objects.get(id=id)
    joins = trip.joins.all()
    context = {
        'trip':trip,
        'joins':joins,
    }
    return render(request, 'travelBuddy_app/show.html', context)

def join(request, id):
    if not request.session['userId']:
        return redirect('/')
    join = Trip.objects.join(id, request.session['userId'])
    return redirect('/home')

