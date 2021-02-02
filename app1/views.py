from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView
)
from django.contrib.auth import get_user_model
from .utility import IsOwner, CustomLimitOffsetPagination, CustomPageNumberPagination, IfAuthenticatedDoNothing
from .serializers import (
    LostOrFoundListSerializer,
    LostOrFoundDetailSerializer,
    LostOrFoundCreateSerializer,
    LostOrFoundUpdateSerializer,
    UserCreateSerializer,
    UserLoginSerializer
)
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from .models import LostOrFound

# Create your views here.

User = get_user_model()

class ListItem(ListAPIView):
    serializer_class = LostOrFoundListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['item_name', 'description', 'pin_number']
    pagination_class = CustomPageNumberPagination
    def get_queryset(self, *args, **kwargs):
        item = LostOrFound.objects.order_by('-id').select_related('name').filter(select='Found')
        query = self.request.GET.get('q')
        if query:
            item = item.filter(Q(item_name__icontains=query) | Q(description__icontains=query) | Q(pin_number__icontains=query)).distinct()
        return item

class DetailItemView(RetrieveAPIView):
    queryset = LostOrFound.objects.all()
    serializer_class = LostOrFoundDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class CreateItem(CreateAPIView):
    queryset = LostOrFound.objects.all()
    serializer_class = LostOrFoundCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(name=self.request.user)

class DestroyItem(RetrieveDestroyAPIView):
    queryset = LostOrFound.objects.all()
    serializer_class = LostOrFoundListSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsOwner]


class UpdateItem(RetrieveUpdateAPIView):
    queryset = LostOrFound.objects.all()
    serializer_class = LostOrFoundUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsOwner]

class CreateUserAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IfAuthenticatedDoNothing]
    

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserCreateSerializer(data=data)
        # from urllib.parse import urlparse
        # path = request.build_absolute_uri()
        # current_scheme, current_netloc = urlparse(path)[:2]
        # print(current_netloc, current_scheme)
        host_name = request.get_host()
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            user = User(username=user, first_name=first_name,last_name=last_name,email=email)
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(redirect_to=f'http://{host_name}/api/login/')
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginUserAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serialize_data = UserLoginSerializer(data=data)
        if serialize_data.is_valid(raise_exception=True):
            new_data = serialize_data.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serialize_data.errors, status=HTTP_400_BAD_REQUEST)