from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from .views import ListItem, DetailItemView, CreateItem, DestroyItem, UpdateItem,\
    CreateUserAPI, LoginUserAPIView, CreateRetreiveApiView, UploadImageApiView

urlpatterns = [
    path('', ListItem.as_view(), name="list"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('register/', CreateUserAPI.as_view(), name='register'),
    # path('login/', LoginUserAPIView.as_view(), name='login'),
    path('create/', CreateItem.as_view(), name="create"),
    
    path('category/<int:pk>/', CreateRetreiveApiView.as_view(), name="retrieve"),
    path('<int:pk>/', include([
        path('detail/', DetailItemView.as_view(), name="detail"),
        path('update/', UpdateItem.as_view(), name='update'),
        path('delete/', DestroyItem.as_view(), name="delete"),
        path('upload_image/', UploadImageApiView.as_view(), name="upload_image"),
    ]))
    
]