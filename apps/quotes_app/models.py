from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
			errors['name'] = "Name should be more than 2"
        if len(postData['email']) < 4:
            errors['email'] = "Email should be more than 4 characters"
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = "Email is invalid"
        if len(postData['password']) < 7:
            errors['password'] = "Password should be more than 7 characters"
        if postData['password'] != postData['conf_password']:
        	errors['ps_match'] = 'Passwords do not match'
        if len(errors) == 0:
        	errors['Registered!'] = 'Registered! Now log in!'
        	hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        	User.objects.create(name=postData['name'], alias=postData['alias'], dob=postData['adate'], password=hash1, email=postData['email'])
        return errors
        
    def login_validator(self, postData):
    	errors = {}
    	if len(User.objects.filter(email=postData['email'])) == 0:
    		errors['emailfail'] = 'incorrect email'
    	else:
    		pass1 = User.objects.get(email=postData['email']).password
    		pass2 = postData['password']
    		if not bcrypt.checkpw(pass2.encode(), pass1.encode()):
    			errors['password'] = 'incorrect Password'
    			print "HEY FUcker"
    	return errors

class QuoteManager(models.Manager):
	def createQuote(self, postData, creator):
		errors = {}
		if len(postData['quote_by']) < 3:
			errors['quote_by'] = "needs to be more than 3 characters"
		if len(postData['message']) < 10:
			errors['message'] = "give me some kind of description, like at least 10 characters"
		else:
			submit = User.objects.get(id=creator)
			u = Quote.objects.create(quote_by=postData['quote_by'], quote=postData['message'], submitted_by=submit)
        	u.save()	
		return errors

class User(models.Model):
	name = models.CharField(max_length=100)
	alias = models.CharField(max_length=100)
	email = models.CharField(max_length=50)
	password = models.CharField(max_length=100)
	dob = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	objects = UserManager()

class Quote(models.Model):
	quote = models.TextField()
	quote_by = models.CharField(max_length=60)
	submitted_by = models.ForeignKey(User, related_name="submitter")
	favorites = models.ManyToManyField(User, default=None)
	objects = QuoteManager()
