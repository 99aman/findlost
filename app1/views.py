from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.mixins import CreateModelMixin
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
    NotificationSerializer,
    RetreiveCategorySerializer,
    UploadImageSerializer,
    UserCreateSerializer,
    UserLoginSerializer
)
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from .models import LostOrFound, Category, Subcategory, UploadImage, Notification

# Create your views here.

User = get_user_model()

class ClaimedApiView(CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            message = serializer.validated_data['message']
            item_id = request.GET.get('claimed_on_id')
            report = request.GET.get('report', False)
            lf = LostOrFound.objects.filter(id=item_id).first()
            lf.do_claim
            if lf.claimed:
                nf = Notification.objects.create(claimed_by=request.user, message=message, claimed_on=lf, report=report)
                nf.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class NotificationApiView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    def get_queryset(self, *args, **kwargs):
        lf = LostOrFound.objects.filter(name=self.request.user)
        qs = Notification.objects.filter(claimed_on__in=lf)
        return qs

class MasterDataApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = RetreiveCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        item = Category.objects.filter(id=1)
        return item

class ListItemApiView(ListAPIView):
    serializer_class = LostOrFoundListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['item_name', 'description', 'pin_code']
    pagination_class = CustomPageNumberPagination
    def get_queryset(self, *args, **kwargs):
        item = LostOrFound.objects.order_by('-id').select_related('name')
        query = self.request.GET.get('search')
        if query:
            item = item.filter(Q(item_name__icontains=query) | Q(description__icontains=query) | Q(pin_code__icontains=query), select='Found').distinct()
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

class UploadImageApiView(CreateAPIView, ListAPIView):
    serializer_class = UploadImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        obj = LostOrFound.objects.filter(id=self.kwargs['pk']).first()
        return obj.uploadimage_set.all()

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(lostfound=LostOrFound.objects.filter(id=self.kwargs['pk']).first())

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
            return Response(serializer.data, status=HTTP_200_OK)
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