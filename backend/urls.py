from django.urls import path
from .views import chat_view, home_view, slots_view

urlpatterns = [
    path("api/chat/", chat_view, name="chat"),
    path("api/slots", slots_view, name="slot"),
    path('', home_view, name='home'),
]
