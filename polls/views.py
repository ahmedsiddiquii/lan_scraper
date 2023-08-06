from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scrapper import scrape_data_from_google_maps
from .google_scrape import scrpe
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Queries, Google_data
from .requests_scraper import *
import threading

from rest_framework import serializers
from .models import Google_data

class GoogleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Google_data
        fields = ['name', 'description', 'location', 'phone', 'email', 'website', 'reviews']

@api_view(['POST'])
def save_data(request):
    if request.method == 'POST':
        longitude = request.data.get('longitude')
        latitude = request.data.get('latitude')
        query_type = request.data.get('type')

        # Check if data is exists
        existing_query = Queries.objects.filter(
            longitude=longitude,
            latitude=latitude,
            type=query_type
        ).first()

        if existing_query:
            # Data already exists
            response_data = {
                'status': 'Data already saved!',
                'longitude': existing_query.longitude,
                'latitude': existing_query.latitude,
                'number_of_data': existing_query.number_of_data,
                'type': existing_query.type,
                'status': existing_query.status
            }
            response_data = {'status': 'Already Exist!'}

            return Response(response_data)
        else:
            #  save the new data
            query = Queries(
                longitude=longitude,
                latitude=latitude,
                number_of_data=request.data['number_of_data'],
                type=query_type,
                status="pending"
            )
            query.save()
            longitude = longitude
            latitude = latitude
            content_type = query_type
            number_of_results = request.data['number_of_data']
            s=threading.Thread(target=scrape_google_maps,args=(content_type,number_of_results,latitude,longitude,query))
            s.start()
            print("scraper started")

        response_data = {'status': 'Data saved successfully!'}

        return Response(response_data)

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

@api_view(['DELETE'])
def delete_data(request):
    try:
        longitude = request.data.get('longitude')
        latitude = request.data.get('latitude')
        query_type = request.data.get('type')

        # Check if any record with same latitude, longitude, or type exists
        matching_queries = Queries.objects.filter(
            Q(longitude=longitude) | Q(latitude=latitude) | Q(type=query_type)
        )

        if matching_queries.exists():
            # Remove the data that matches the criteria
            matching_queries.delete()
            return Response({'status': 'Data removed successfully!'})
        else:
            return Response({'status': 'No matching data found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'status': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
