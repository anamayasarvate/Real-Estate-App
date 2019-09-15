from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from contacts.models import Contact
from django.contrib.auth.decorators import login_required

def register(request):
	if request.method == "POST":
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		if password1 != password2:
			messages.error(request, "ERROR: Passwords did not match")
			return redirect('register')
		elif User.objects.filter(username = username).exists():
			messages.error(request, "ERROR: username already exists")
			return redirect('register')		
		elif User.objects.filter(email = email).count() > 0:
			messages.error(request, "ERROR: email already exists")
			return redirect('register')	
		else:
			user = User.objects.create_user(first_name = first_name,
			last_name = last_name,username = username,
			email = email, password = password1)
			user.save()
			#For direct login after registrstion
			'''
			auth.login(request, user)
			messages.success(request, "SUCCESS: You have successfully logged in!")
			return redirect('index')
			'''
			messages.success(request, "SUCCESS: You have been registered!")
			return redirect('login')
	return render(request, 'accounts/register.html')

def login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		print(user)
		if user is not None:
			auth.login(request, user)
			messages.success(request, "SUCCESS: You have successfully logged in!")
			return redirect('dashboard')
		else: 
			messages.error(request, "ERROR: username or password did not match")
			return redirect('login')

	return render(request, 'accounts/login.html')

def logout(request):
	if request.method == "POST":
		auth.logout(request)
		messages.success(request, "SUCCESS: You have successfully logged out!")
		return redirect('index')

@login_required
def dashboard(request):
	contacts = Contact.objects.filter(user_id = request.user.id).order_by('-contact_date')
	context = {
	"contacts": contacts
	}

	return render(request, 'accounts/dashboard.html', context)
