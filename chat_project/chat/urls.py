from django.urls import path, re_path
from . import views, consumers

urlpatterns = [
    # Home redirects to the login page
    path('', views.login_view, name='home'),

    # Signup view
    path('signup/', views.signup_view, name='signup'),

    # Login view
    path('login/', views.login_view, name='login'),

    # Chat view (main chat page)
    path('chat/', views.chat_view, name='chat'),

    # Individual chat window between two users
    path('chat/<int:user_id>/', views.chat_window, name='chat_window'),

    # Load old messages (AJAX/Fetch request)
    path('chat/load_old_messages/<int:user_id>/', views.load_old_messages, name='load_old_messages'),
]
websocket_urlpatterns = [
    re_path(r'ws/chat(?P<receiver_id>\w+)/$',consumers.ChatConsumer.as_asgi()),
]