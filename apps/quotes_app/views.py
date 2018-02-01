# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from forms import *
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
	return redirect('/main')

def landing(request):
	print "hi"
	if request.method == 'POST':
		logForm = loginForm(request.POST)
	else:
		logForm = loginForm()
	return render(request, 'quotes/index.html', {'logForm': logForm})

def user_create(request):
	errors = User.objects.register_validator(request.POST)
	if len(errors) == 0:
		x = User.objects.get(email=request.POST['email'])
		request.session['regId'] = x.id
		p = Poke.objects.create(user=User.objects.get(id=request.session['id']))
		return redirect('/')
	else:
		for error in errors:
			messages.error(request, errors[error])
		return redirect('/')

def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors) == 0:
		U = User.objects.get(email=request.POST['email'])
		request.session['email'] = U.email
		request.session['name'] = U.name
		request.session['id'] = U.id
		return redirect('/quotes')
	else:
		for error in errors:
			messages.error(request, errors[error])
		return redirect('/')

def dashboard(request):
	context = {
	'all_quotes': Quote.objects.exclude(favorites=User.objects.get(email=request.session['email'])),
	'fav_quotes': Quote.objects.filter(favorites=User.objects.get(email=request.session['email']))
	}
	return render(request, 'quotes/dashboard.html', context)

def submit_quote(request):
	errors = Quote.objects.createQuote(request.POST, request.session['id'])
	if len(errors) ==0:
		return redirect('/quotes')
	else: 
		for error in errors:
			messages.error(request, errors[error])
		return redirect('/quotes')

def user_add_favorite(request):
	this_user = User.objects.get(id=request.session['id'])
	this_quote = Quote.objects.get(id=request.POST['favorites'])
	this_quote.favorites.add(this_user)
	return redirect('/quotes')

def user_remove_favorite(request):
	this_user = User.objects.get(id=request.session['id'])
	this_quote = Quote.objects.get(id=request.POST['remove'])
	this_quote.favorites.remove(this_user)
	return redirect('/quotes')

def user_quotes(request, id):
	usr = User.objects.get(id=id)
	context = {
	'user': usr,
	'my_quotes': Quote.objects.filter(submitted_by__id=usr.id)
	}
	return render(request, 'quotes/user_quotes.html', context)

def logout(request):
	request.session.flush()
	return redirect('/')