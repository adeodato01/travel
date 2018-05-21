from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages


def index(request):
    # return HttpResponse("This is THE homepage")
    return render(request, "travels_app/index.html")


def registration(request):
    result = User.objects.ValidateTheUser(request.POST)
    if result['status']:
        request.session['user_id'] = result['user_id']
        return redirect('/travels')
    else:
        print(result['errors'])
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/main')


def login(request):
    result = User.objects.ValidateLogin(request.POST)
    if result['status']:
        request.session['user_id'] = result['user_id']
        return redirect('/travels')
    else:
        print(result['errors'])
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/main')


def home(request):
    context = {
        "ind_user": User.objects.get(id=request.session['user_id']),
        # "trips": User.objects.get(id=request.session['user_id']).trips.all(),
        # "all": Trip.objects.all(),
        'my_trips': Trip.objects.filter(users=request.session['user_id']),
        'not_my_trips': Trip.objects.exclude(users=request.session['user_id']),
        # "except": Trip.objects.all().exclude(users=request.session['user_id']),
    }
    return render(request, "travels_app/travels.html", context)


def destination(request, number):
    trip = Trip.objects.get(id=number)
    context = {
        "trip": trip,
        "other_attendees": trip.users.exclude(id=trip.trip_creator.id)
    }
    return render(request, "travels_app/display.html", context)


def add(request):
    return render(request, "travels_app/add_trip.html")


def addVerify(request):
    print('\n''\n'"************THIS Travel Entry**********")
    print(request.POST)
    print("*****************************"'\n''\n')

    result = Trip.objects.ValidateTrip(request.POST, request.session['user_id'])

    print('\n''\n'"************THIS error**********")
    print(result)
    print("*****************************"'\n''\n')
    if result['status']:
        # request.session['user_id'] = result['user_id']
        return redirect('/travels')
    else:
        print(result['errors'])
        for error in result['errors']:
            messages.error(request, error)
        return redirect('/travels/add')
    # return HttpResponse("This is the Travel Plan Verify page")


def addMe(request, number):
    this_trip = Trip.objects.get(id=number)
    this_user = User.objects.get(id=request.session['user_id'])
    this_user.trips.add(this_trip)
    return redirect('/travels')



def logout(request):
    request.session.flush()
    return redirect('/main')
