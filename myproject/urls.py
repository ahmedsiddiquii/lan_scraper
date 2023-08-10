
from django.contrib import admin
from django.urls import path
from polls.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('google_locations/get_data/', save_data, name='get_data'),
    path('get_newsdata/',get_newsdata,name='get_data')  

]