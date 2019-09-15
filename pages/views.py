from django.shortcuts import render
from listings.models import Listing
from realtors.models import Realtor
from listings.choices import bedroom_choices, price_choices, state_choices

def index(request):	
	listings = Listing.objects.filter(is_published = True).order_by('-list_date')[:3]
	context = {
		'listings': listings,
		'bedroom_choices': bedroom_choices,
		'price_choices': price_choices,
		'state_choices': state_choices
	}
	return render(request, 'pages/index.html', context)

def about(request):
	realtors = Realtor.objects.all().order_by('-hire_date')
	context = {'realtors': realtors}
	return render(request, "pages/about.html", context)