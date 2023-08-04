
from django.contrib import admin
from django.urls import path
from polls.views import home,scrape_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('scrape_data/', scrape_data, name='scrape_data'),
]
