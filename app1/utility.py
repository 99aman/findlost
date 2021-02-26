from rest_framework.permissions import BasePermission
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django.http import HttpResponseRedirect

class IsOwner(BasePermission):
    message = 'You are not owner'
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.name)

class IfAuthenticatedDoNothing(BasePermission):
    message = 'You already authenticated'
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 4

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 4