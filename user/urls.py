from django.urls import path 
from user.views import HelloView, UserListView

urlpatterns = [
    path("", HelloView.as_view()),
    path('users/', UserListView.as_view()),
]