from django.urls import path
from .views import place_order, cancel_order, replay_state

urlpatterns = [
    path('api/place_order/', place_order),
    path('api/cancel_order/', cancel_order),
    path('api/state/', replay_state),
]