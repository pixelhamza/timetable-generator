
from django.contrib import admin
from django.urls import path,include
from baseApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('api/', include('baseApp.urls')), 
    
    
]
