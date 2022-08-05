

from django.contrib import admin
from django.urls import path, include
from sales.views import listcustomers
urlpatterns = [
    path('customers/', listcustomers)
]