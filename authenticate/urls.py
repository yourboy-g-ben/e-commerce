from django.urls import path 
from authenticate.views import SignUpView, LoginVew
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signal/', SignUpView.as_view()),
    path('login/', LoginVew.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]