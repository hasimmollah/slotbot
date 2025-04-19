from django.urls import path
from django.views.generic import TemplateView

from backend.views import slot, chat

urlpatterns = [
    path("api/chat/", chat.ChatView.as_view(), name="chat"),
    path("api/slots", slot.SlotListView.as_view(), name="slot"),
    path('api/slots/<int:slot_id>/', slot.SlotDetailView.as_view()),
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
]
