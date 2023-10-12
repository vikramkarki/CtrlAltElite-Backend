from django.db.models import Avg, Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from restaurant_review.models import Client,Therapist,Appointment
from restaurant_review.serializers import AppointmentSerializer

from restaurant_review.models import Restaurant, Review

# Create your views here.

def index(request):
    print('Request for index page received')
    restaurants = Restaurant.objects.annotate(avg_rating=Avg('review__rating')).annotate(review_count=Count('review'))
    return render(request, 'restaurant_review/index.html', {'restaurants': restaurants})


def details(request, id):
    print('Request for restaurant details page received')
    restaurant = get_object_or_404(Restaurant, pk=id)
    return render(request, 'restaurant_review/details.html', {'restaurant': restaurant})


def create_restaurant(request):
    print('Request for add restaurant page received')
    return render(request, 'restaurant_review/create_restaurant.html')


@csrf_exempt
def add_restaurant(request):
    try:
        name = request.POST['restaurant_name']
        street_address = request.POST['street_address']
        description = request.POST['description']
    except (KeyError):
        # Redisplay the form
        return render(request, 'restaurant_review/add_restaurant.html', {
            'error_message': "You must include a restaurant name, address, and description",
        })
    else:
        restaurant = Restaurant()
        restaurant.name = name
        restaurant.street_address = street_address
        restaurant.description = description
        Restaurant.save(restaurant)

        return HttpResponseRedirect(reverse('details', args=(restaurant.id,)))


@csrf_exempt
def add_review(request, id):
    restaurant = get_object_or_404(Restaurant, pk=id)
    try:
        user_name = request.POST['user_name']
        rating = request.POST['rating']
        review_text = request.POST['review_text']
    except (KeyError):
        # Redisplay the form.
        return render(request, 'restaurant_review/add_review.html', {
            'error_message': "Error adding review",
        })
    else:
        review = Review()
        review.restaurant = restaurant
        review.review_date = timezone.now()
        review.user_name = user_name
        review.rating = rating
        review.review_text = review_text
        Review.save(review)

    return HttpResponseRedirect(reverse('details', args=(id,)))

class AppointmentListView(APIView):
    def get(self, request, item_id=None):
        if item_id:
            item = get_object_or_404(Appointment, id=item_id)
            serializer = AppointmentSerializer(item)
            Appointments=Appointment.objects.filter(id=item_id).select_related("client").select_related("therapist")
            Appoint={}
            for appo in Appointments:
                Appoint={
                    "id":appo.id,
                    "therapistid":appo.therapist.id,
                    "therapistName":appo.therapist.name,
                    "clientId":appo.client.id,
                    "clientName":appo.client.name,
                    "clientAddress":appo.client.address,
                    "checkinTime":appo.sc_checkin_time,
                    "checkoutTime":appo.sc_checkout_time,
                    "actualCheckinTime":appo.act_checkin_time,
                    "actualCheckoutTime":appo.act_checkout_time,
                    "status":appo.status,
                    "therapistContact":appo.therapist.contact

                }
            
            return Response(Appoint)
        else:
            items = Appointment.objects.all()
            serializer = AppointmentSerializer(items, many=True)
            Appointments=Appointment.objects.select_related("client").select_related("therapist")
            App_list= []
            for appo in Appointments:
                Appoint={
                    "id":appo.id,
                    "therapistid":appo.therapist.id,
                    "therapistName":appo.therapist.name,
                    "clientId":appo.client.id,
                    "clientName":appo.client.name,
                    "clientAddress":appo.client.address,
                    "checkinTime":appo.sc_checkin_time,
                    "checkoutTime":appo.sc_checkout_time,
                    "actualCheckinTime":appo.act_checkin_time,
                    "actualCheckoutTime":appo.act_checkout_time,
                    "status":appo.status,
                    "therapistContact":appo.therapist.contact

                }
                App_list.append(Appoint)
            return Response(App_list)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

