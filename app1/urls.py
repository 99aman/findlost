from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ListItem, DetailItemView, CreateItem, DestroyItem, UpdateItem,\
    CreateUserAPI

urlpatterns = [
    path('', ListItem.as_view(), name="list"),
    path('token/auth/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', CreateUserAPI.as_view(), name='register'),
    path('create/', CreateItem.as_view(), name="create"),
    path('<int:pk>/', include([
        path('detail/', DetailItemView.as_view(), name="detail"),
        path('update/', UpdateItem.as_view(), name='update'),
        path('delete/', DestroyItem.as_view(), name="delete")
    ]))
    
]