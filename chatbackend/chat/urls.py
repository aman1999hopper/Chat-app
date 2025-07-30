from django.urls import path
from .views import get_messages

urlpatterns = [
    path('messages/<str:room_name>/', get_messages),
]
