import os
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail

def inquiry(request):
	if request.method == "POST":
		listing_title = request.POST['listing']
		listing_id = request.POST['listing_id']
		user_id = request.POST['user_id']
		realtor_email = request.POST['realtor_email']
		name = request.POST['name']
		email = request.POST['email']
		phone = request.POST['phone']
		message = request.POST['message']

		if request.user.is_authenticated:
			if Contact.objects.filter(user_id = user_id, listing_id = listing_id).exists():
				messages.error(request, "You have already made an inquiry on this listing")
				return redirect('/listings/' + listing_id)

		contact = Contact(listing = listing_title, listing_id = listing_id,
						  name = name, email = email, phone = phone,
						  message = message, user_id = user_id)
		contact.save()
		send_mail(
			'Property listing inquiry',
			'There has been an inquiry about the listing- '+listing_title+
			', Sign into the admin for more info',
			os.environ.get("EMAIL_USER"),
			['anamayasarvate@gmail.com', realtor_email],
			fail_silently = False
			)
		messages.success(request, "Your message has been successfully sent!")
		return redirect('/listings/' + listing_id)
