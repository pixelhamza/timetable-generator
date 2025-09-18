from django.urls import path
from .views import upload_data,home


urlpatterns = [
   
    path('upload/', upload_data, name="upload-data"),

]
