from django.urls import path
from . import views

app_name = 'ChatBot'

urlpatterns = [
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('api/chat/', views.chat_api, name='chat_api'),
]
