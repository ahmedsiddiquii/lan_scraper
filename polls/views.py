from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scrapper import scrape_data_from_google_maps
from .google_scrape import scrpe

def home(request):
    return render(request,'index.html')
    
def scrape_data(request):
    if request.method == 'GET':
        data = request.GET.get('query')
        print(data)

        if data:
            if data.lower().startswith('https://www.google.com/maps/search'):
                # If the user input is a Google Map URL
                scraped_data = scrape_data_from_google_maps(data)
            else:
                # If the user input is a Google keyword
                scraped_data = scrpe(data)

            return JsonResponse(scraped_data, safe=False)

    return JsonResponse({'error': 'Invalid input or method'}, status=400)


# @csrf_exempt
# def scrape_data_view(request):
#     url='https://www.google.com/maps/search/lulu/@41.5587382,-133.3127447,5z/data=!3m1!4b1?entry=ttu'
#     scraped_data = scrape_data_from_google_maps(url)

#     return JsonResponse(scraped_data, safe=False)

# @csrf_exempt
# def scrap_google(request):
#     search_name = 'state'  
#     scraped_data = scrpe(search_name)
#     return JsonResponse(scraped_data, safe=False)