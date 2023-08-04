from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scrapper import scrape_data_from_google_maps
from .google_scrape import scrpe

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Queries, Google_data

from rest_framework import serializers
from .models import Google_data

class GoogleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Google_data
        fields = ['name', 'description', 'location', 'phone', 'email', 'website', 'reviews']

@api_view(['POST'])
def save_data(request):
    if request.method == 'POST':
        query = Queries(
            longitude=request.data['longitude'],
            latitude=request.data['latitude'],
            number_of_data=request.data['number_of_data'],
            type=request.data['type'],
            status="pending")
        query.save()
        return Response({'status': 'Data saved successfully!'})

    return Response({'status': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_data(request):
    if request.method == 'GET':
        longitude = request.GET.get('longitude')
        latitude = request.GET.get('latitude')
        query_type = request.GET.get('type')

        data_entries = Google_data.objects.filter(
            longitude=longitude,
            latitude=latitude,
            query_id__name=query_type
        )
        serializer = GoogleDataSerializer(data_entries, many=True)
        return Response({'data': serializer.data})

    return Response({'status': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)
