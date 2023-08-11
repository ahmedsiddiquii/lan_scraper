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
from .g_loc import *
import threading
from .news import scrape_api

from rest_framework import serializers
from .models import Google_data

class GoogleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Google_data
        fields = '__all__'

@api_view(['GET', 'POST'])
def get_newsdata(request):
    print(request.method)
    if request.method=='POST':
        country=request.data.get('country')
        if country:
            data = scrape_api(country) 
            response_data = {
                'status': 'success',
                'message': 'Data retrieved successfully',
                'data': data
            }
            return JsonResponse(response_data, status=200)
        else:
            response_data = {
                'status': 'error',
                'message': 'Country parameter is missing or invalid'
            }
            return JsonResponse(response_data, status=400)


@api_view(['GET', 'POST'])
def save_data(request):
    if request.method == 'POST':
        longitude = request.data.get('longitude')
        latitude = request.data.get('latitude')
        query_type = request.data.get('type')

        # Check if data is exists
        existing_query = Queries.objects.filter(
            longitude=longitude,
            latitude=latitude,
            type=query_type,
            number_of_data=int(request.data['number_of_data'])
        ).first()

        if existing_query:
            # Data already exists
            google_data_list = Google_data.objects.filter(query_id=existing_query)
            serializer = GoogleDataSerializer(google_data_list, many=True)
            return Response(serializer.data)

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
            # s=threading.Thread(target=scrape_google_maps,args=(content_type,number_of_results,latitude,longitude,query))
            # s.start()
            print("scraper started")
            scrape_google_maps(content_type, number_of_results, latitude, longitude, query)
            google_data_list = Google_data.objects.filter(query_id=query)
            serializer = GoogleDataSerializer(google_data_list, many=True)
            return Response(serializer.data)


        # response_data = {'status': 'Data saved successfully!'}

        return Response(response_data)
    if request.method == 'GET':
        print("get request")
        print(request.GET)
        longitude = request.GET.get('longitude')
        latitude = request.GET.get('latitude')
        query_type = request.GET.get('type')

        # Check if data is exists
        existing_query = Queries.objects.filter(
            longitude=longitude,
            latitude=latitude,
            type=query_type,
            number_of_data=int(request.GET['number_of_data'])
        ).first()
        print(existing_query)

        if existing_query:
            # Data already exists
            google_data_list = Google_data.objects.filter(query_id=existing_query)
            serializer = GoogleDataSerializer(google_data_list, many=True)
            return Response(serializer.data)

        else:
            #  save the new data
            query = Queries(
                longitude=longitude,
                latitude=latitude,
                number_of_data=int(request.GET['number_of_data']),
                type=query_type,
                status="pending"
            )
            query.save()
            longitude = longitude
            latitude = latitude
            content_type = query_type
            number_of_results = int(request.GET['number_of_data'])
            # s=threading.Thread(target=scrape_google_maps,args=(content_type,number_of_results,latitude,longitude,query))
            # s.start()
            print("scraper started")
            scrape_google_maps(content_type, number_of_results, latitude, longitude, query)
            google_data_list = Google_data.objects.filter(query_id=query)
            serializer = GoogleDataSerializer(google_data_list, many=True)
            return Response(serializer.data)


        # response_data = {'status': 'Data saved successfully!'}

        return Response(response_data)

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
