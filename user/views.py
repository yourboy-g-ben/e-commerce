from django.shortcuts import render
from rest_framework import views, generics, permissions
from rest_framework.response import Response
from utils.pagination import CustomPagination
from authenticate.models import User
from user.serializers import UserSerializer
# Create your views here.

class HelloView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(data={"message": "Helloworld"}, status=200)
    
class UserListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination
    serializer_class = UserSerializer
    queryset = User.objects.all()
