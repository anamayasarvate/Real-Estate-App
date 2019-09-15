from django.shortcuts import render,get_object_or_404
from .models import Listing
from django.views.generic import ListView
from django.http import HttpResponseForbidden
from .choices import price_choices, bedroom_choices, state_choices

class ListingListView(ListView):	
	model = Listing
	template_name = "listings/listings.html"
	context_object_name = "listings"
	paginate_by = 6

	def get_queryset(self):
		return Listing.objects.filter(is_published = True).order_by('-list_date')

def listing(request, listing_id):
	listing = get_object_or_404(Listing, pk = listing_id)
	if listing.is_published == True:
		context = {'listing': listing}
		return render(request, "listings/listing.html", context)
	else:
		return HttpResponseForbidden()

def search(request):
	listings = Listing.objects.filter(is_published = True)
	if 'keywords' in request.GET:
		keywords = request.GET['keywords']
		if keywords:
			listings = listings.filter(description__icontains = keywords)

	if 'city' in request.GET:
		city = request.GET['city']
		if city:
			listings = listings.filter(city__iexact = city)

	if 'state' in request.GET:
		state = request.GET['state']
		if state:
			listings = listings.filter(state__iexact = state)

	if 'bedrooms' in request.GET:
		bedrooms = request.GET['bedrooms']
		if bedrooms:
			listings = listings.filter(bedrooms__gte = bedrooms)

	if 'price' in request.GET:
		price = request.GET['price']
		if price:
			listings = listings.filter(price__lte = price)


	context = {
		'listings': listings,
		'bedroom_choices': bedroom_choices,
		'price_choices': price_choices,
		'state_choices': state_choices,
		'values': request.GET
	}
	return render(request, 'listings/search.html', context)

