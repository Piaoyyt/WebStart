from django.urls import path, include
from mgr import customer, medicine
from mgr import signInOut
from mgr import order
urlpatterns = [
    path('customers', customer.dispatcher),
    path('signin', signInOut.signin),
    path('signout',signInOut.signout),
    path('medicines', medicine.dispatcher),
    path('orders', order.dispatcher),
]